from fastapi import APIRouter, Request
from llama_index.llms import ChatMessage, MessageRole
from pydantic import BaseModel
from starlette.responses import StreamingResponse

from ...open_ai import (
    ContextFilter,
    OpenAICompletion,
    OpenAIMessage,
    to_openai_response,
    to_openai_sse_stream,
)
from .service import ChatService

chat_router = APIRouter(prefix="/api")


class ChatBody(BaseModel):
    """
    Represents the body of a chat request.

    Attributes:
        messages (list[OpenAIMessage]): List of messages in the chat.
        use_context (bool, optional): Flag indicating whether to use context. Defaults to False.
        context_filter (ContextFilter | None, optional): Context filter. Defaults to None.
        include_sources (bool, optional): Flag indicating whether to include sources. Defaults to True.
        stream (bool, optional): Flag indicating whether to stream the chat. Defaults to False.
    """

    messages: list[OpenAIMessage]
    use_context: bool = False
    context_filter: ContextFilter | None = None
    include_sources: bool = True
    stream: bool = False

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a rapper. Always answer with a rap.",
                        },
                        {
                            "role": "user",
                            "content": "How do you fry an egg?",
                        },
                    ],
                    "stream": False,
                    "use_context": True,
                    "include_sources": True,
                    "context_filter": {
                        "docs_ids": ["928c8264-9411-45b9-852a-250bd99c567d"]
                    },
                }
            ]
        }
    }


@chat_router.post(
    "/chat/completions",
    response_model=None,
    responses={200: {"model": OpenAICompletion}},
    tags=["contextual_completions"],
)
def chat_completion(
    request: Request, body: ChatBody
) -> OpenAICompletion | StreamingResponse:
    """
    Handles the chat completion API endpoint.

    Args:
        request (Request): The FastAPI request object.
        body (ChatBody): The request body containing chat messages and configuration.

    Returns:
        Union[OpenAICompletion, StreamingResponse]: The completion response or a streaming response.
    """
    service: ChatService = request.state.injector.get(ChatService)
    all_messages = [
        ChatMessage(content=m.content, role=MessageRole(m.role)) for m in body.messages
    ]
    if body.stream:
        completion_gen = service.stream_chat(
            messages=all_messages,
            use_context=body.use_context,
            context_filter=body.context_filter,
        )
        return StreamingResponse(
            to_openai_sse_stream(
                response_generator=completion_gen.response,
                sources=completion_gen.sources if body.include_sources else None,
            ),
            media_type="text/event-stream",
        )
    else:
        completion = service.chat(
            messages=all_messages,
            use_context=body.use_context,
            context_filter=body.context_filter,
        )
        return to_openai_response(
            response=completion.response,
            sources=completion.sources if body.include_sources else None,
        )
