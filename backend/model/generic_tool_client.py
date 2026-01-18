import json
from typing import List, Dict, Any
from typing import Callable, AsyncGenerator
from backend.model.chat_events_factory import *
from backend.model.response_placeholders import on_initial_prompt, on_tool_invocation
from backend.model.message import Message


class GenericToolClient:
    """
    Generic tool client managing the logic of iteratively running tool calls from a stream generator
     and yielding the results..

    :param iterate_on_stream: The stream generator to use. Expected to receive an async generator
    of events specific to the API used, and return an async generator of chat events.
    :param create_tool_output: The tool output generator to use. Expected to receive a list of tool
     calls (names, args and call_id) and return a list of tool calls and outputs as expected by the
      API used.
    :param tool_call_limit: The maximum number of tool calls to allow.
    """

    def __init__(self, iterate_on_stream: Callable,
                 create_tool_output: Callable[[str, str, str], List[Dict[str, Any]]],
                 tool_call_limit: int = 100):
        self.iterate_on_stream = iterate_on_stream
        self.create_tool_output = create_tool_output
        self.tool_call_limit = tool_call_limit

    async def run_tool_calls_from_stream(self, stream_generator: Callable,
                                         messages: List[Message]) -> AsyncGenerator[ChatEvent, None]:
        """
        Run tool calls from the given stream generator.

        :param stream_generator: The stream generator to use. Expected to receive a list of tool
        outputs and return an async generator of chat events.
        :param messages: List of messages.
        :return: An async generator of chat events.
        """
        pending_tool_calls = []
        tool_outputs = []
        while True:
            if len(tool_outputs) > self.tool_call_limit * 2:  # Each tool call generated 2 entries.
                raise ValueError("The given query caused an excessive tool usage, aborting.")
            for value in pending_tool_calls:
                yield value
                name = value.data["name"]
                args_json = value.data["args"]
                item_id = value.data["call_id"]
                yield placeholder_event(on_tool_invocation(name, messages[-1].content))
                tool_outputs.extend(self.create_tool_output(name, args_json, item_id))
                tool_output = tool_outputs[-1] | {"name": name}
                yield ChatEvent(ChatEventType.TOOL_OUTPUT_GENERATED, tool_output)
            pending_tool_calls = []
            stream = await stream_generator(tool_outputs, messages)
            print("STEAM CREATED")
            async for value in self.iterate_on_stream(stream):
                if value.type == ChatEventType.TOOL_CALL_GENERATED:
                    pending_tool_calls.append(value)
                else:
                    yield value
                    if value.type == ChatEventType.ERROR:
                        return
            if len(pending_tool_calls) == 0:
                break
        if len(tool_outputs) > 0:
            yield state_event(ChatEventType.TOOLS_OUTPUT_STATE, json.dumps(tool_outputs))
        yield done_event()
