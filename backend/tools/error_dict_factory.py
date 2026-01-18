"""
This module exposes factory function for the creation of error from tools.

Functions:
    error_output_with_message: Returns a dictionary with the error message.
"""
from backend.tools.models import CallOutput


def error_output_with_message(message: str) -> CallOutput:
    """
    Returns a dictionary with the error message.
    
    :param message: The error message.
    :return: A dictionary with the error message.
    """
    return CallOutput(status="error", data={"message": message})
