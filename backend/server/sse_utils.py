"""
Utilities for Server-Sent Events (SSE).
"""

import json
from typing import Any, AsyncIterator


def sse_event(event) -> str:
    """
    Generate a Server-Sent Event (SSE) event.

    :param event: Event to be sent.
    :return: The SSE event as a string.
    """
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


async def sse_from_async_iter(it: AsyncIterator[str]):
    """
    Generate a Server-Sent Event (SSE) from an async iterator.

    :param it: The async iterator to generate events from.
    :return: An async iterator of SSE events.
    """
    async for chunk in it:
        yield chunk
