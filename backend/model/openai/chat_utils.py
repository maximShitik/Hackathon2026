"""
This module exposes utility functions for openAI chat operations.

Functions:
    count_tokens: Estimates the number of tokens in the given text as perceive by the given model
"""
import tiktoken


def count_tokens(text: str, model="gpt-5"):
    """
    Estimates the number of tokens in the given text as perceive by the given model

    :param text: Text whose token amount is to be estimated.
    :param model: Model to be used.
    :return: Estimated token amount.
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))
