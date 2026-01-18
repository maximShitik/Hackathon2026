from enum import Enum


class OpenAIEventType(Enum):
    """
    Event types as per openAI API documentation.
    """
    RESPONSE_OUTPUT_TEXT_DELTA = "response.output_text.delta"
    RESPONSE_OUTPUT_TEXT_DONE = "response.output_text.done"
    RESPONSE_CREATED = "response.created"
    RESPONSE_COMPLETED = "response.completed"
    RESPONSE_OUTPUT_DONE = "response.output.done"
    RESPONSE_ITEM_ADDED = "response.output_item.added"
    RESPONSE_FUNCTION_CALL_ARGUMENTS_DONE = "response.function_call_arguments.done"
    ERROR = "error"
