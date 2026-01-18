from abc import ABC, abstractmethod
from typing import AsyncGenerator, List
from backend.model.message import Message
from backend.model.chat_events_factory import ChatEvent


class ResponseProvider(ABC):
    """
    Interface implemented by objects that can provide responses from model.
    """

    @abstractmethod
    async def get_response(self, messages: List[Message],
                           instructions: str) -> AsyncGenerator[ChatEvent, None]:
        """
        Creates an async generator that yields responses for the given messages.

        :param messages: The messages to generate a response for.
        :param instructions:  Instructions for the model.
        :return: An async generator that yields responses for the given messages.
        """
        if False:
            yield {}  # This signals to the IDE that this is an AsyncGenerator, silencing
            # warnings about this method being a coroutine.
        ...
