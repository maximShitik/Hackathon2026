"""
This module exposes utility functions and classes for language handling.

Enums:
    SupportedLanguages: Enumeration of the supported languages

Functions:
    detect_supported_language: Detects the supported language of the given text
"""
from enum import Enum


class SupportedLanguages(Enum):
    """
    Enum representing the supported languages by this application.
    """
    HEBREW = 1
    ENGLISH = 2


def detect_supported_language(text: str) -> SupportedLanguages:
    """
    A very simple heuristic to determine whatever the given text is in hebrew or not.
    The underlying assumption is that a word containing latin alphabet is more likely to appear
    in a hebrew text than the opposite.
    This method assumes that if any chars from any other language exists in the chat it's english.

     e.g.: יש Optalgin?
    This sentence is clearly in hebrew, but most metric based system comparing english and hebrew
    would fail on this sentence. This naive language detector assumes that the existence of
    hebrew in the sentence at a rate larger than 10% of the total number of chars implies this is
    a hebrew sentence.

    :param text: The text whose language is to be detected
    :return: The detected language.
    """
    if not text:
        return SupportedLanguages.ENGLISH

    he = 0
    en = 0
    for ch in text:
        o = ord(ch)

        if ord('א') <= o <= ord('ת'):
            he += 1
        if ord('a') <= o <= ord('z') or ord("A") <= o <= ord("Z"):
            en += 1

    total = en + he
    he_ratio = he / total

    if he >= 1 and he_ratio >= 0.1:
        return SupportedLanguages.HEBREW
    return SupportedLanguages.ENGLISH
