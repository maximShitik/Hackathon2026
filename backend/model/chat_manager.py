import json
from typing import List, Dict, AsyncGenerator, Optional, Callable, Tuple
from backend.model.response_provider import ResponseProvider
from backend.model.chat_events_factory import ChatEventType, ChatEvent, placeholder_event
from backend.model.message import Message, MessageMetadata
from backend.model.chat_events_factory import chat_event, chat_event_for_message
from backend.model.response_placeholders import on_invalid_prompt_length, on_initial_prompt


class ChatManager(ResponseProvider):
    """
    Object implementing the ResponseProvider interface by wrapping another 
    ResponseProvider and adding chat history and summarization upon exceeding the provided token
    limit or messages length limit.
    """
    def __init__(self, main_provider: ResponseProvider, summary_provider: ResponseProvider,
                 summary_format_provider: Callable,
                 messages_limit: int = 10, keep_count: int = 5, token_limit: int = 10000,
                 token_keep_count: int = 5000, add_summary_to_instructions: bool = True,
                 token_counter: Optional[Callable[[str], int]] = None, model_name="assistant"):
        """
        Initialize the object with the given parameters.

        :param main_provider: The main provider to use for generating responses.
        :param summary_provider: The provider to use for generating summaries.
        :param summary_format_provider: Converts the tool_outputs, previous messages and previous
            summary into a message and instructions format accepted by the model.
        :param messages_limit: The maximum number of messages to send to the chat.
        :param keep_count: The number of messages to keep in the chat history after summarizing
            the rest.
        :param token_limit: The maximum number of tokens to use for generating responses. 
            Ignored if no token_counter was provided.
        :param token_keep_count: The maximal amount of tokens to keep after passing the limit,
            including the latest message.
        :param add_summary_to_instructions: Whether to add the summary to the instructions.
        :param token_counter: Optional function to use for counting tokens. 
        """
        self.main_provider = main_provider
        self.summary_provider = summary_provider
        self.messages_length_limit = messages_limit
        self.keep_count = keep_count
        self.token_limit = token_limit
        self.token_keep_count = token_keep_count
        self.token_counter = token_counter
        self.previous_summary: Optional[str] = None
        self.tools_used: List[Dict[str, str]] = []
        self.summary_format_provider = summary_format_provider
        self.add_summary_to_instructions = add_summary_to_instructions
        self.model_name = model_name
        # Stores the index of the last kept message, such that any index before that 
        # had already been summarized.
        self.last_kept_index: int = 0

    async def get_response(self, messages: List[Message],
                           instructions: str) -> AsyncGenerator[ChatEvent, None]:
        """
        Generate a response for the given messages.

        :param messages: The messages to generate a response for.
        :param instructions: The instructions to use for generating the response.
        :return: An async generator of events.
        """

        message_text = messages[-1].content
        yield placeholder_event(on_initial_prompt(message_text))
        async for ev in self.summary_provider.get_response([Message("user", "Hi there! how are "
                                                                          "you?")], "Don't be "
                                                                                       "kind, "
                                                                                       "be mean "
                                                                                       ):
            yield ev
        await self.manage_messages_by_length(messages)
        try:
            await self._manage_token_amount(messages)
        except ValueError:
            yield chat_event(ChatEventType.TEXT_DONE, self.model_name,
                             on_invalid_prompt_length(messages[-1].content))
            return
        messages = messages[self.last_kept_index:]
        if self.previous_summary is not None:
            if self.add_summary_to_instructions:
                instructions = instructions + "\n" + self._create_summary_scheme_for_instructions()
            else:
                messages = [Message("user", "Summary of previous context: " +
                                    self.previous_summary)] + messages
        else:
            instructions = instructions + "\n" + self._create_summary_scheme_for_instructions()
        async for event in self.main_provider.get_response(messages, instructions):
            event_type = event.type
            if event_type == ChatEventType.TOOLS_OUTPUT_STATE:
                self.tools_used += json.loads(event.data.get("state", []))
            elif event_type == ChatEventType.TEXT_DONE and self.token_counter is not None:
                msg = Message(**event.data)
                reply_tokens = self.token_counter(msg.content)
                msg.metadata = MessageMetadata(reply_tokens)
                yield chat_event_for_message(event_type, msg)
            else:
                yield event

    async def manage_messages_by_length(self, messages: List[Message]):
        """
        Manages the length of the messages array by using this objects limits.

        :param messages: The messages to manage the length for.
        """
        if len(messages[self.last_kept_index:]) > self.messages_length_limit:
            await self._summarize_from_index(messages, self.keep_count)

    async def _manage_token_amount(self, messages: List[Message]):
        """
        Manages the token amount in the given messages by using this objects limits.

        :param messages: The messages to manage the token amount for.
        """
        if self.token_counter is None:
            return
        latest_count = self.token_counter(messages[-1].content)
        if latest_count > self.token_limit:
            raise ValueError("Latest message token count exceeded the allowed limit.")
        messages[-1].metadata = MessageMetadata(latest_count)
        total_count = 0
        ind_where_passed_keep_limit = None
        for i in range(len(messages) - 1, self.last_kept_index - 1, -1):
            msg = messages[i]
            if msg.metadata is None:
                raise RuntimeError(f"Message from role {msg.role} and content {msg.content} had no"
                                   f"metadata object attached.")
            total_count += msg.metadata.tokens
            if total_count > self.token_keep_count and ind_where_passed_keep_limit is None:
                ind_where_passed_keep_limit = i
            if total_count > self.token_limit:
                await self._summarize_from_index(messages, ind_where_passed_keep_limit)
                break

    async def _summarize_from_index(self, messages: List[Message], index: int):
        """
        Truncates the messages array from the given index and summarizes 
        the truncated messages, setting this objects last_kept_index and 
        previous_summary.

        :param messages: The messages to truncate and summarize.
        :param index: The index from which to truncate the messages.
        """
        to_summarize = messages[self.last_kept_index:-index]
        self.last_kept_index = len(messages) - index
        summary = await self._get_summary(to_summarize)
        self.previous_summary = summary

    async def _get_summary(self, messages: List[Message]) -> str:
        """
        Generates a summary for the given messages. Includes all the tool outputs.

        :param messages: The messages to generate a summary for.
        :return: The summary.
        """
        summary_messages, summary_instruction = self.summary_format_provider(self.tools_used,
                                                                             messages,
                                                                             self.previous_summary)
        async for event in self.summary_provider.get_response(summary_messages,
                                                              summary_instruction):

            if event.type == ChatEventType.TEXT_DONE:
                return event.data["content"]
        raise RuntimeError("Text done event was not sent on previous messages summarization.")

    def _create_summary_scheme_for_instructions(self):
        """
        Wraps the previous summary in a scheme that the model can understand.
        """
        return "This is a summary of previous messages from the same conversation, " \
               "acknowledge the data provided here as well" + "[SUMMARY_START] " + \
            f"{self.previous_summary} [SUMMARY_ENDS]"
