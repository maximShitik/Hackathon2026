"""
This module exposes dataclasses that represent messages.

Classes:
    MessageMetadata: Data class holding message metadata.
    Message: Data class representing a message.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class MessageMetadata:
    """
    Data class holding message metadata.
    """
    tokens: int


@dataclass
class Message:
    """
    Data class representing a message.
    """
    role: str
    content: str
    metadata: Optional[MessageMetadata] = None

    def to_open_ai_input_dict(self):
        """
        Converts the message class into a dict of the form that is expected by OpenAI API.

        :return: a dict in the input form expected by OpenAI APIs.
        """
        return {"role": self.role, "content": self.content}

    def to_gemini_input_dict(self):
        """
        Converts the message class into a dict of the form that is expected by Gemini API.

        :return: a dict in the input form expected by Gemini API.
        """
        return {"role": self.role, "parts": [{"text": self.content}]}
