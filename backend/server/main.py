"""
Server running the chat.
"""
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import traceback
from backend.model.message import Message
from backend.model.response_provider import ResponseProvider
from backend.server.lifespan import lifespan
from backend.server.sse_factory import *
from backend.model.chat_events_factory import ChatEventType
from backend.server.novisign_provider import push_to_novisign_async

# The application server.
app = FastAPI(lifespan=lifespan)

# General instructions to provide the agent.
SYSTEM_INSTRUCTIONS = """
You job is to assist people at the mall. They may approach in any language, answer them in their 
own language. They may ask you for directions, what stores are there in 
the mall and what products do they sell. Use tools to answer these queries, do not invent or guess 
any data about any store, stick to the tools output.
Always be courteous and kind, but stick to providing answers about the mall, do not answer any 
other topic. Some products and stores have a coupon, suggest to look for a coupon to the user, 
based on the store or product they are seeking.
"""


@app.get("/model_name")
async def get_config():
    return {"name": "assistant" if app.state.use_openAI else "model"}


def handle_tool_event(event):
    if event.data["name"] == "search_product":
        data = event.data["output"]["data"]
        print(data)
        app.state.novisign_provider.force_next_ad(data[0])
    if event.data["name"] == "set_navigation_for_store":
        store_id = event.data["output"]["data"]["id"]
        data = app.state.novisign_provider.get_data_for_navigation_asset(store_id)
        push_to_novisign_async(data_items=data)



@app.post("/chat/stream")
async def chat_stream(req: Request):
    """
    Handles the chat stream post with the given request.

    :param req: The HTTP Request.
    """
    body = await req.json()
    conversation = body.get("conversation", [])
    messages = app.state.messages
    # model_name_in_messages = "assistant" if app.state.use_openAI else "model"
    model_name_in_messages = "assistant"

    async def run():
        response_provider: ResponseProvider = app.state.response_provider
        try:
            placeholder_id = f"placeholder-{len(conversation)}"
            message_id = f"msg-{len(conversation)}"
            user_message = Message(**conversation[-1])
            messages.append(user_message)
            first_delta = True
            async for event in response_provider.get_response(messages, SYSTEM_INSTRUCTIONS):
                event_type = event.type
                if event_type == ChatEventType.TOOL_CALL_GENERATED:
                    yield tool_call_generated_event(event.data["name"], event.data["args"])
                if event_type == ChatEventType.TOOL_OUTPUT_GENERATED:
                    handle_tool_event(event)
                    yield tool_output_generated_event(event.data["name"], event.data["output"])
                if event_type == ChatEventType.PLACEHOLDER:
                    replace_id = placeholder_id if first_delta else None
                    yield UI_update_event(SSEEventTypes.RENDER, placeholder_id, "message",
                                          model_name_in_messages,
                                          text=event.data["content"], replace_id=replace_id)
                elif event_type == ChatEventType.TEXT_DELTA:
                    if first_delta:
                        yield UI_update_event(SSEEventTypes.RENDER, message_id, "message",
                                              model_name_in_messages,
                                              replace_id=placeholder_id, text=event.data["content"])
                        first_delta = False
                    else:
                        yield UI_update_event(SSEEventTypes.PATCH, message_id, "message",
                                              model_name_in_messages,
                                              op="append_text", text=event.data["content"])
                elif event_type == ChatEventType.TEXT_DONE:
                    messages.append(Message(role=event.data.get("role"),
                                            content=event.data.get("content")))
                    if first_delta:
                        yield UI_update_event(SSEEventTypes.RENDER, message_id, "message",
                                              model_name_in_messages,
                                              replace_id=placeholder_id,
                                              text=event.data.get("content"))
                        first_delta = False

            yield done_event()
        except Exception as e:
            print(traceback.format_exc())
            yield error_event(e)
            yield done_event()

    return StreamingResponse(run(), media_type="text/event-stream")


app.mount("/", StaticFiles(directory="frontend", html=True), name="static")
