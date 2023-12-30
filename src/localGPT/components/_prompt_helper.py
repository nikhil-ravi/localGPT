import abc
import logging
from collections.abc import Sequence
from typing import Any

from llama_index.llms import ChatMessage
from llama_index.llms.llama_utils import completion_to_prompt, messages_to_prompt

logger = logging.getLogger(__name__)


class AbstractPromptStyle(abc.ABC):
    """Abstract class for prompt styles.

    The prompt style is used to convert a list of messages or a completion into a prompt that can be understood by the model.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        logger.debug(f"Initializing prompt_style={self.__class__.__name__}")

    @abc.abstractmethod
    def _messages_to_prompt(self, messages: Sequence[ChatMessage]) -> str:
        """Converts a list of messages into a prompt.

        Args:
            messages (Sequence[ChatMessage]): The list of messages.

        Returns:
            str: The formatted prompt.
        """
        pass

    @abc.abstractmethod
    def _completion_to_prompt(self, completion: str) -> str:
        """Converts a completion into a prompt.

        Args:
            completion (str): The completion.

        Returns:
            str: The formatted prompt.
        """
        pass

    def messages_to_prompt(self, messages: Sequence[ChatMessage]) -> str:
        """Converts a list of messages into a prompt.

        Args:
            messages (Sequence[ChatMessage]): The list of messages.

        Returns:
            str: The formatted prompt.
        """
        prompt = self._messages_to_prompt(messages)
        logger.debug(f"Got for messages={messages} the prompt={prompt}")
        return prompt

    def completion_to_prompt(self, completion: str) -> str:
        """Converts a completion into a prompt.

        Args:
            completion (str): The completion.

        Returns:
            str: The formatted prompt.
        """
        prompt = self._completion_to_prompt(completion)
        logger.debug(f"Got for completion={completion} the prompt={prompt}")
        return prompt


class Llama2PromptStyle(AbstractPromptStyle):
    """The prompt style used by Llama2 found in llama_utils. It transforms a list of messages or a completion into the following format:

    ```text
    <s> [INST] <<SYS>> your system prompt here. <</SYS>>

    user message here [/INST] assistant (model) response here </s>
    ```
    """

    def _messages_to_prompt(self, messages: Sequence[ChatMessage]) -> str:
        """Converts a list of messages into a prompt.

        Args:
            messages (Sequence[ChatMessage]): The list of messages.

        Returns:
            str: The formatted prompt.
        """
        return messages_to_prompt(messages)

    def _completion_to_prompt(self, completion: str) -> str:
        """Converts a completion into a prompt.

        Args:
            completion (str): The completion.

        Returns:
            str: The formatted prompt.
        """
        return completion_to_prompt(completion)
