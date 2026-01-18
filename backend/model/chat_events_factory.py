"""
This module exposes factory functiongs generating schemas for events 
that can be emitted by the chat.

Enums:
    ChatEventType: The type of the event.

Functions:
    chat_event: Generates a chat event.
    chat_event_for_message: Generates a chat event from the given message.
    chat_event_from_agent: Generates a chat event from an agent output.
    placeholder_event: Generates a placeholder event.
    error_event: Generates an error event.
    state_event: Generates a state event.
    done_event: Generates a done event.
"""
from enum import Enum
from dataclasses import dataclass, asdict
from typing import Optional, Dict
from backend.model.message import Message


class ChatEventType(Enum):
    """
    The type of the event.
    """
    PLACEHOLDER = "placeholder"
    TEXT_DELTA = "text_delta"
    TEXT_DONE = "text_done"
    STATUS = "status"
    DONE = "done"
    TOOLS_OUTPUT_STATE = "tool_output_state"
    TOOL_CALL_GENERATED = "tool_call_generated"
    TOOL_OUTPUT_GENERATED = "tool_output_generated"
    ERROR = "error"


@dataclass
class ChatEvent:
    type: ChatEventType
    data: Dict[str, str]


def chat_event(event_type: ChatEventType,  role: str, text: str) -> ChatEvent:
    """
    Generates a chat event with the given arguments.

    :param event_type: The type of the event.
    :param role: The role of the event.
    :param text: The text of the event.
    :return: The chat event.
    """
    return ChatEvent(event_type, {"role": role, "content": text})


def chat_event_for_message(event_type: ChatEventType, message: Message) -> ChatEvent:
    """
    Generates a chat event from the given message.

    :param event_type: The type of the event.
    :param message: The message who represent the data of this event.
    :return: The chat event.
    """
    return ChatEvent(event_type, asdict(message))


def chat_event_from_agent(event_type: ChatEventType, agent_output: str) -> ChatEvent:
    """
    Generates a chat event from an agent output.

    :param event_type: The type of the event.
    :param agent_output: The output from the agent.
    :return: The chat event.
    """
    return chat_event(event_type, "assistant", agent_output)


def placeholder_event(text: str, model_name="assistant") -> ChatEvent:
    """
    Generates a placeholder event with the given arguments.

    :param text: The text of the event.
    :return: The placeholder event.
    """
    return chat_event(ChatEventType.PLACEHOLDER, model_name, text)


def error_event(code: str, error: str) -> ChatEvent:
    """
    Generates an error event with the given arguments.

    :param code: The code of the error.
    :param error: The error message.
    :return: The error event.
    """
    return ChatEvent(ChatEventType.ERROR, {"code": code, "message": error})


def state_event(event_type: ChatEventType, state: str) -> ChatEvent:
    """
    Generates a state event with the given arguments.

    :param event_type: The type of the event.
    :param state: The state of the event.
    :return: The state event.
    """
    return ChatEvent(event_type, {"state": state})


def done_event() -> ChatEvent:
    """
    Generates a done event.

    :return: The done event.
    """
    return ChatEvent(ChatEventType.DONE, {})
