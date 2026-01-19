"""
This module exposes specialized response providers configured to handle the openAI API.

Classes:
    OpenAISimpleResponseProvider: Responds only to OpenAIEventType.RESPONSE_OUTPUT_TEXT_DONE,
        and sends the text.
    OpenAIToolResponseProvider: Provides the API with tools, manages tool calls and stream all
        tool and text events, using the agents reply or premade placeholders..
"""
from openai import AsyncOpenAI

from backend.model.generic_tool_client import GenericToolClient
from backend.model.message import Message
from backend.model.response_provider import ResponseProvider
from backend.model.openai.tool_schema import OPEN_AI_TOOL_SCHEMA
from backend.model.tool_manager import ToolManager
from backend.model.openai.event_types import OpenAIEventType
from backend.model.response_placeholders import on_initial_prompt, on_tool_invocation
from typing import Any, AsyncGenerator, List
from backend.model.chat_events_factory import *
from collections import defaultdict
import json


class OpenAISimpleResponseProvider(ResponseProvider):
    """
    Object implementing the ResponseProvider interface for OpenAI API response creations.
    """

    def __init__(self, api_key: str, model_name: str = "gpt-5-nano"):
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model_name

    async def get_response(self, messages: List[Message],
                           instructions: str) -> AsyncGenerator[ChatEvent, None]:
        input_messages = [m.to_open_ai_input_dict() for m in messages]
        stream = await self.client.responses.create(model=self.model,
                                                    instructions=instructions,
                                                    input=input_messages,
                                                    stream=True)
        async for event in stream:
            if event.type == OpenAIEventType.RESPONSE_OUTPUT_TEXT_DONE.value:
                yield chat_event_from_agent(ChatEventType.TEXT_DONE, event.text)
                return


class OpenAIToolResponseProvider(ResponseProvider):
    """
    Object implementing the ResponseProvider interface for OpenAI API response creations and tool
    usage.
    """

    def __init__(self, tool_manager: ToolManager, api_key: str, model_name: str = "gpt-5-nano",
                 tool_call_limit: int = 100):
        """
        Initialize the object with the given arguments.

        :param tool_manager: Object that manage tool calls and return an output.
        :param api_key: API Key used to create the AsyncOpenAI object used to make API calls.
        :param model_name: Name of the LLM model to use.
        :param tool_call_limit: Limit on the number of tool calls that can be made for a single
            user prompt. Needed to prevent queries that could make the token usage explode.
        """
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = model_name
        self.tool_manager = tool_manager
        self.tool_client = GenericToolClient(self._iterate_on_stream, self._create_tool_output,
                                             tool_call_limit)

    async def get_response(self, messages: List[Message],
                           instructions: str) -> AsyncGenerator[ChatEvent, None]:
        input_messages = [m.to_open_ai_input_dict() for m in messages]

        def stream_generator(tool_outputs: List[Dict[str, Any]]):
            return self.client.responses.create(model=self.model, instructions=instructions,
                                                        input=input_messages + tool_outputs,
                                                        tools=OPEN_AI_TOOL_SCHEMA, stream=True)
        async for value in self.tool_client.run_tool_calls_from_stream(stream_generator,
                                                                       input_messages):
            yield value

    def _create_tool_output(self, name, args_json, item_id) -> List[Dict[str, Any]]:
        """
        Creates a tool output array according to openAI schema for the given tool 
        call as outputed by the model.

        :param name: The name of the tool.
        :param args_json: The arguments of the tool.
        :param item_id: The id of the item.
        :return: The tool output array.
        """
        result = self.tool_manager.call_tool(name, args_json)
        return [{
            "type": "function_call",
            "call_id": item_id,
            "name": name,
            "arguments": args_json,
        }, {
            "type": "function_call_output",
            "call_id": item_id,
            "output": json.dumps(result, ensure_ascii=False),
        }]

    async def _iterate_on_stream(self, stream) -> AsyncGenerator[ChatEvent, None]:
        """
        Iterate over the stream, capturing openAI events and yield ChatEvents

        :param stream: The stream to iterate over.
        """
        ongoing_tool_calls = defaultdict(lambda: dict())
        async for event in stream:
            if event.type == OpenAIEventType.RESPONSE_OUTPUT_TEXT_DELTA.value:
                if event.delta:
                    yield chat_event_from_agent(ChatEventType.TEXT_DELTA, event.delta)
            if event.type == OpenAIEventType.RESPONSE_OUTPUT_TEXT_DONE.value:
                yield chat_event_from_agent(ChatEventType.TEXT_DONE, event.text)
            if event.type == OpenAIEventType.RESPONSE_ITEM_ADDED.value:
                item = event.item
                if getattr(item, "type", None) == "function_call":
                    if getattr(item, 'id', None) is not None:
                        ongoing_tool_calls[item.id]['item_id'] = item.id
                        if getattr(item, "name", None) is not None:
                            ongoing_tool_calls[item.id]['name'] = item.name
                        if getattr(item, "arguments", None) is not None:
                            ongoing_tool_calls[item.id]['arguments'] = item.arguments
                        if getattr(item, "call_id", None) is not None:
                            ongoing_tool_calls[item.id]['call_id'] = item.call_id
            if event.type == OpenAIEventType.RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE.value:
                item_id = event.item_id
                name = event.name if event.name is not None else ongoing_tool_calls[item_id]['name']
                args_json = event.arguments if event.arguments is not None else \
                    ongoing_tool_calls[item_id]['arguments']
                call_id = ongoing_tool_calls[item_id]['call_id']
                yield ChatEvent(ChatEventType.TOOL_CALL_GENERATED, {"name": name,
                                                                    "args": args_json,
                                                                    'call_id': call_id})
            if event.type == OpenAIEventType.RESPONSE_COMPLETED.value:
                yield state_event(ChatEventType.STATUS, "model_completed")
            if event.type == OpenAIEventType.ERROR.value:
                yield error_event(event.get("code"), event.get("message"))
