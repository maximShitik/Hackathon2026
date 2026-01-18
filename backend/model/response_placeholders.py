"""
This module exposes generic response placeholders for different phases of the
chat, in all supported languages.

Functions:
    on_initial_prompt: Returns a placeholder response for the initial prompt.
    on_tool_invocation: Returns a placeholder response for the tool invocation.
    on_invalid_prompt_length: Returns a placeholder response for text who exceeded the maximal
        amount of tokens.
"""
from backend.language_utils import *

# Generic placeholder messages for tool invocation in english.
TOOL_WAITING_MESSAGES = {
    "get_medication_by_name": (
        "Looking up medication information…"
    ),
    "find_medications_by_ingredient": (
        "Searching for medications that contain this ingredient…"
    ),
    "check_inventory": (
        "Checking availability in the selected location…"
    ),
    "list_locations": (
        "Retrieving available pharmacy locations…"
    ),
    "create_support_ticket": (
        "Creating a support request…"
    ),
    "request_reservation": (
        "Verifying prescription details and reserving inventory…"
    ),
    "get_ticket": (
        "Retrieving support ticket…"
    ),
    "get_reservation": (
        "Retrieving reservation…"
    ),
}

# Generic placeholder messages for tool invocation in hebrew.
TOOL_WAITING_MESSAGES_HE = {
    "get_medication_by_name": (
        "מחפש מידע על התרופה…"
    ),
    "find_medications_by_ingredient": (
        "מחפש תרופות המכילות את החומר הפעיל…"
    ),
    "check_inventory": (
        "בודק זמינות במלאי בסניף שנבחר…"
    ),
    "list_locations": (
        "טוען את רשימת הסניפים הזמינים…"
    ),
    "create_support_ticket": (
        "יוצר פנייה לשירות הלקוחות…"
    ),
    "request_reservation": (
        "מאמת פרטי מרשם ושומר את התרופה במלאי…"
    ),
    "get_ticket": (
        "מחפש פנייה לשירות הלקוחות…"
    ),
    "get_reservation": (
        "מחפש מרשם…"
    ),
}


def on_initial_prompt(text: str) -> str:
    """
    Returns a placeholder response for the initial prompt, in the given text language.

    :param text: The text to detect the language from.
    :return: The string containing the response.
    """
    language = detect_supported_language(text)
    return "חושב..." if language == SupportedLanguages.HEBREW else "Thinking..."


def on_tool_invocation(tool_name: str, text: str) -> str:
    """
    Returns a placeholder response for the tool invocation, in the given text language.

    :param tool_name: The name of the tool to use.
    :param text: The text to detect the language from.
    :return: The string containing the response.
    """
    language = detect_supported_language(text)
    return TOOL_WAITING_MESSAGES_HE[tool_name] if language == SupportedLanguages.HEBREW \
        else TOOL_WAITING_MESSAGES[tool_name]


def on_invalid_prompt_length(text: str) -> str:
    """
    Returns a placeholder response for text who exceeded the maximal amount of tokens, in the
    given text language.
    :param text: The text to detect the language from.
    :return: The string containing the response.
    """
    language = detect_supported_language(text)
    heb_str = "מצטער, אך אינני יכול לעבד הודעה באורך כזה, אנא קצר את ההודעה או שלח אותה בחלקים."
    eng_str = "Sorry, but I cannot process a message of this length. Please shorten the message" \
              " or send it in parts."
    return heb_str if language == SupportedLanguages.HEBREW else eng_str