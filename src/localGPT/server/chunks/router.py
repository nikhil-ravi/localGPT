from typing import Literal

from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

from ...open_ai import ContextFilter
from .service import Chunk, ChunksService

chunks_router = APIRouter(prefix="/api")


class ChunksBody(BaseModel):
    """
    Represents the body of a request for retrieving chunks of text.

    Attributes:
        text (str): The input text.
        context_filter (ContextFilter | None): The context filter for the text.
        limit (int): The maximum number of chunks to retrieve.
        prev_next_chunks (int): The number of previous and next chunks to include.
    """

    text: str = Field(examples=["This is a chunk of text."])
    context_filter: ContextFilter | None = None
    limit: int = 10
    prev_next_chunks: int = Field(default=0, examples=[2])


class ChunksResponse(BaseModel):
    """
    Represents the response for chunks.

    Attributes:
        object (Literal["list"]): The type of object returned, which is always "list".
        model (Literal["local-gpt"]): The model used for generating the chunks, which is always "local-gpt".
        data (list[Chunk]): The list of chunks.
    """

    object: Literal["list"]
    model: Literal["local-gpt"]
    data: list[Chunk]


@chunks_router.post("/chunks", tags=["context chunks"])
def chunks_retrieval(request: Request, body: ChunksBody) -> ChunksResponse:
    """Given a `text`, returns the most relevant chunks from the ingested documents.

    The returned information can be used to generate prompts that can be
    passed to `/completions` or `/chat/completions` APIs. Note: it is usually a very fast API, because only the Embeddings model is involved, not the LLM. The returned information contains the relevant chunk `text` together with the source `document` it is coming from. It also contains a score that can be used to compare different results.

    The max number of chunks to be returned is set using the `limit` param.

    Previous and next chunks (pieces of text that appear right before or after in the document) can be fetched by using the `prev_next_chunks` field.

    The documents being used can be filtered using the `context_filter` and passing the document IDs to be used. Ingested documents IDs can be found using `/ingest/list` endpoint. If you want all ingested documents to be used, remove `context_filter` altogether.

    Args:
        request (Request): The incoming request object.
        body (ChunksBody): The request body containing the text and context filter.

    Returns:
        ChunksResponse: The response object containing the retrieved chunks.
    """
    service = request.state.injector.get(ChunksService)
    results = service.retrieve_relevant(
        text=body.text,
        context_filter=body.context_filter,
        limit=body.limit,
        prev_next_chunks=body.prev_next_chunks,
    )
    return ChunksResponse(
        object="list",
        model="local-gpt",
        data=results,
    )
