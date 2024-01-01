from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel

from .service import Embedding, EmbeddingService

embeddings_router = APIRouter(
    prefix="/api",
)


class EmbeddingsBody(BaseModel):
    """
    Represents the request body for embeddings.

    Attributes:
        input (Union[str, List[str]]): The input text or list of input texts.
    """

    input: str | list[str]


class EmbeddingsResponse(BaseModel):
    """
    Represents the response object for embeddings.

    Attributes:
        object (Literal["list"]): The type of the object, which should always be "list".
        model (Literal["local-gpt"]): The name of the model, which should always be "local-gpt".
        data (list[Embedding]): The list of embeddings.
    """

    object: Literal["list"]
    model: Literal["local-gpt"]
    data: list[Embedding]


@embeddings_router.post("/embeddings", tags=["embeddings"])
def embeddings_generation(request: Request, body: EmbeddingsBody) -> EmbeddingsResponse:
    """Get a vector representation of a given input.

    That vector representation can be easily consumed by machine learning models and algorithms.

    Args:
        request (Request): The HTTP request object.
        body (EmbeddingsBody): The request body containing the input texts.

    Returns:
        EmbeddingsResponse: The response object containing the generated embeddings.
    """
    service = request.state.injector.get(EmbeddingService)
    input_texts = body.input if isinstance(body.input, list) else [body.input]
    embeddings = service.texts_embeddings(input_texts)
    return EmbeddingsResponse(
        object="list",
        model="local-gpt",
        data=embeddings,
    )
