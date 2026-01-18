"""
This module exposes the output models for different tool calls.

Classes:
    CallOutput: Class that represents the output of a tool call.
"""
from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class CallOutput:
    """
    Base model for tool call output.
    """
    status: str
    data: Dict[str, Any]
