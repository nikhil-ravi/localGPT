from fastapi import APIRouter, Request
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from ...open_ai import ContextFilter, OpenAICompletion, OpenAIMessage
from ...server.chat import ChatBody, chat_completion

completions_router = APIRouter(prefix="/v1")


class CompletionsBody(BaseModel):
    """
    Represents the body of a completions request.

    Attributes:
        prompt (str): The prompt text.
        system_prompt (str | None): The system prompt text. Defaults to None.
        use_context (bool): Flag indicating whether to use context. Defaults to False.
        context_filter (ContextFilter | None): The context filter. Defaults to None.
        include_sources (bool): Flag indicating whether to include sources. Defaults to True.
        stream (bool): Flag indicating whether to stream the response. Defaults to False.
    """

    prompt: str
    system_prompt: str | None = None
    use_context: bool = False
    context_filter: ContextFilter | None = None
    include_sources: bool = True
    stream: bool = False

    model_config = {
        "json_schema_extra": {
            "example": {
                "prompt": "How do you fry an egg?",
                "system_prompt": "You are a rapper. Always answer with a rap.",
                "stream": False,
                "use_context": False,
                "include_sources": False,
            }
        }
    }


@completions_router.post(
    "/completions",
    response_model=None,
    summary="Completion",
    responses={200: {"model": OpenAICompletion}},
    tags=["contextual_completions"],
)
def prompt_completion(
    request: Request, body: CompletionsBody
) -> OpenAICompletion | StreamingResponse:
    """
    Handles the prompt completion request.

    Args:
        request (Request): The HTTP request object.
        body (CompletionsBody): The request body containing the completion prompt.

    Returns:
        Union[OpenAICompletion, StreamingResponse]: The completion response.
    """
    messages = [OpenAIMessage(content=body.prompt, role="user")]
    if body.system_prompt:
        messages.insert(0, OpenAIMessage(content=body.system_prompt, role="system"))

    chat_body = ChatBody(
        messages=messages,
        use_context=body.use_context,
        stream=body.stream,
        include_sources=body.include_sources,
        context_filter=body.context_filter,
    )
    return chat_completion(request, chat_body)
