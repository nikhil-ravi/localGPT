import time
import uuid
from typing import Iterator, Literal

from llama_index.llms import ChatResponse, CompletionResponse
from pydantic import BaseModel, Field

from ..server.chunks import Chunk


class OpenAIDelta(BaseModel):
    """
    Represents an OpenAI Delta object.

    Attributes:
        content (str | None): The content of the OpenAI Delta object.
    """

    content: str | None


class OpenAIMessage(BaseModel):
    """
    Represents a message in the OpenAI conversation.

    Attributes:
        content (str | None): The content of the message.
        role (Literal["assistant", "system", "user"]): The role of the message sender. Defaults to "user".
    """

    content: str | None
    role: Literal["assistant", "system", "user"] = Field(default="user")


class OpenAIChoice(BaseModel):
    """
    Represents a choice made by the OpenAI model.

    Attributes:
        finish_reason (str, optional): The reason for finishing the choice. Defaults to None.
        delta (OpenAIDelta, optional): The delta associated with the choice. Defaults to None.
        message (OpenAIMessage, optional): The message associated with the choice. Defaults to None.
        sources (list[Chunk], optional): The list of sources associated with the choice. Defaults to None.
        index (int): The index of the choice.
    """

    finish_reason: str | None = Field(examples=["stop"])
    delta: OpenAIDelta | None = None
    message: OpenAIMessage | None = None
    sources: list[Chunk] | None = None
    index: int = 0


class OpenAICompletion(BaseModel):
    """
    Represents a completion response from the OpenAI model.

    Attributes:
        id (str): The ID of the completion.
        object (Literal["completion", "completion.chunk"]): The object type. Defaults to "completion".
        created (int): The timestamp of the completion.
        model (Literal["local-gpt"]): The model used to generate the completion. Defaults to "local-gpt".
        choices (list[OpenAIChoice]): The list of choices made by the model.
    """

    id: str
    object: Literal["completion", "completion.chunk"] = Field(default="completion")
    created: int = Field(..., examples=[1623168000])
    model: Literal["local-gpt"]
    choices: list[OpenAIChoice]

    @classmethod
    def from_text(
        cls,
        text: str | None,
        finish_reason: str | None = None,
        sources: list[Chunk] | None = None,
    ) -> "OpenAICompletion":
        """
        Create an OpenAICompletion object from text.

        Args:
            text (str | None): The text content.
            finish_reason (str | None): The finish reason.
            sources (list[Chunk] | None): The list of sources.

        Returns:
            OpenAICompletion: The created OpenAICompletion object.
        """
        return OpenAICompletion(
            id=str(uuid.uuid4()),
            object="completion",
            created=int(time.time()),
            model="local-gpt",
            choices=[
                OpenAIChoice(
                    message=OpenAIMessage(role="assistant", content=text),
                    finish_reason=finish_reason,
                    sources=sources,
                )
            ],
        )

    @classmethod
    def json_from_delta(
        cls,
        *,
        text: str | None = None,
        finish_reason: str | None = None,
        sources: list[Chunk] | None = None,
    ) -> str:
        """
        Create a JSON string representation of an OpenAICompletion object.

        Args:
            text (str | None): The text content.
            finish_reason (str | None): The finish reason.
            sources (list[Chunk] | None): The list of sources.

        Returns:
            str: The JSON string representation of the OpenAICompletion object.
        """
        chunk = OpenAICompletion(
            id=str(uuid.uuid4()),
            object="completion.chunk",
            created=int(time.time()),
            model="local-gpt",
            choices=[
                OpenAIChoice(
                    delta=OpenAIDelta(content=text),
                    finish_reason=finish_reason,
                    sources=sources,
                )
            ],
        )
        return chunk.model_dump_json()


def to_openai_response(
    response: str | ChatResponse, sources: list[Chunk] | None = None
) -> OpenAICompletion:
    """
    Convert a response to an OpenAICompletion object.

    Args:
        response (str | ChatResponse): The response.
        sources (list[Chunk] | None): The list of sources.

    Returns:
        OpenAICompletion: The converted OpenAICompletion object.
    """
    if isinstance(response, ChatResponse):
        return OpenAICompletion.from_text(response.delta, finish_reason="stop")
    else:
        return OpenAICompletion.from_text(
            response, finish_reason="stop", sources=sources
        )


def to_openai_sse_stream(
    response_generator: Iterator[str | CompletionResponse | ChatResponse],
    sources: list[Chunk] | None = None,
) -> Iterator[str]:
    """
    Convert a response generator to an SSE stream.

    Args:
        response_generator (Iterator[str | CompletionResponse | ChatResponse]): The response generator.
        sources (list[Chunk] | None): The list of sources.

    Yields:
        str: The SSE stream data.
    """
    for response in response_generator:
        if isinstance(response, CompletionResponse | ChatResponse):
            yield f"data: {OpenAICompletion.json_from_delta(text=response.delta)}\n\n"
        else:
            yield f"data: {OpenAICompletion.json_from_delta(text=response, sources=sources)}\n\n"
    yield f"data: {OpenAICompletion.json_from_delta(text=None,finish_reason='stop')}\n\n"
    yield "data: [DONE]\n\n"
