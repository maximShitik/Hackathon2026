"""
This module exposes a function to parse the tool usage dictionary into a string describing
the usage.

Functions:
    parse_tool_usage: Parses the given tool usage dictionary into a string describing the usage.
"""
from typing import Dict, List, Optional, Tuple
import json

from backend.model.message import Message


def parse_tool_usage(tools_outputs: List[Dict[str, str]]) -> str:
    """
    Parses the given tool usage dictionary into a string describing the usage. Expect each tool
    call to be immediately followed by the output.

    :param tools_outputs: array containing tool output dictionaries as given to the model,
    either describing a function call or output.
    :return: A string parsing the string into a sentence explaining the call.
    """
    res = ""
    for output in tools_outputs:
        call_type = output.get("type", "")
        if call_type == "function_call":
            if len(output["arguments"]) > 0:
                arguments = ",".join([f"{k} with value {v}" for
                                      k, v in json.loads(output["arguments"]).items()])
            else:
                arguments = ""
            res += f"The agent called the tool {output['name']} with the arguments: {arguments}\n"
        elif call_type == "function_call_output":
            res += f"and got as output: {output['output']}"
        else:
            raise ValueError(f"The given tool_usage did not contain a valid type. Got {call_type} "
                             f"expected function_call or function_cal_output")
    return res


def create_summary_format(tools_used: List[Dict[str, str]], messages: List[Message],
                          previous_summary: Optional[str] = None) -> Tuple[List[Message], str]:
    """
    Creates and returns the summary format needed to create a summary for the given messages.
    For OpenAI API.

    :param tools_used: List of tool usage dictionaries as given to the model.
    :param messages: List of messages to create a summary for.
    :param previous_summary: Optional previous summary to include in the summary.
    :return: Tuple containing the summary messages and the summary instruction.
    """
    conversation_text = ""
    for msg in messages:
        conversation_text += f"{msg.role}: {msg.content}\n"
    if len(tools_used) > 0:
        conversation_text += "System: "
        conversation_text += parse_tool_usage(tools_used)
    summary_instruction = "Summarize the following conversation concisely, preserving key " \
                              "information."
    if previous_summary is not None:
        summary_instruction += f"\nThis is the previous summary, you should include key " \
                               f"information from here: [SUMMARY_START] " \
                               f"{previous_summary} [SUMMARY_ENDS]"
    summary_messages = [Message(role="user", content=conversation_text)]
    return summary_messages, summary_instruction
