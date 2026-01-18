from enum import Enum
from backend.server.sse_utils import sse_event
from typing import Dict, Any, Optional


class SSEEventTypes(Enum):
    RENDER = "render"
    PATCH = "patch"
    DONE = "done"
    ERROR = "error"
    TOOL_CALL_GENERATED = "tool_call_generated"
    TOOL_OUTPUT_GENERATED = "tool_output_generated"


def UI_update_event(event_type: SSEEventTypes, id: str, kind: str, role: str, text: str,
                    replace_id: Optional[str] = None, op: Optional[str] = None):
    """
    Creates a UI update event with the given arguments.

    :param event_type: The type of the event.
    :param kind: The kind of the event.
    :param role: The role of the event.
    :param text: The text of the event.
    :param replace_id: ID of element to replace
    :return: The UI update SSE event.
    """
    data = {
        "id": id,
        "kind": kind,
        "role": role,
        "text": text
    }
    if replace_id is not None:
        data["replace_id"] = replace_id
    if op is not None:
        data["op"] = op
    return sse_event({
        "type": event_type.value,
        "data": data
    })


def tool_call_generated_event(name: str, args: str) -> str:
    """
    Creates a tool call generated event.

    :param name: The name of the tool.
    :param args: The arguments of the tool.
    :return: The tool call generated SSE event.
    """
    data = {
        "name": name,
        "args": args
    }
    return sse_event({"type": SSEEventTypes.TOOL_CALL_GENERATED.value, "data": data})


def tool_output_generated_event(name: str, result: str) -> str:
    """
    Creates a tool output generated event.

    :param name: The name of the tool.
    :param result: The result of the tool.
    :return: The tool output generated SSE event.
    """
    data = {
        "name": name,
        "result": result
    }
    return sse_event({"type": SSEEventTypes.TOOL_OUTPUT_GENERATED.value, "data": data})


def done_event() -> str:
    """
    Creates a done event.
    """
    return sse_event({"type": "done", "data": {}})


def error_event(e: Exception) -> str:
    """
    Creates an error event.

    :param e: The exception to be included in the event.
    :return: The error SSE event.
    """
    return sse_event({"type": "error", "data": {"message": str(e)}})
