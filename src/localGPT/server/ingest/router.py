from typing import Literal

from fastapi import APIRouter, HTTPException, Request, UploadFile
from pydantic import BaseModel

from .model import IngestedDoc
from .service import IngestService

ingest_router = APIRouter(prefix="/v1")


class IngestTextBody(BaseModel):
    """
    Represents the body of a text ingestion request.

    Attributes:
        file_name (str): The name of the file being ingested.
        text (str): The text content to be ingested.
    """

    file_name: str
    text: str


class IngestResponse(BaseModel):
    """
    Represents the response returned by the ingest API.

    Attributes:
        object (Literal["list"]): The type of object returned, which is always "list".
        model (Literal["local-gpt"]): The name of the model used for ingestion, which is always "local-gpt".
        data (list[IngestedDoc]): The list of ingested documents.
    """

    object: Literal["list"]
    model: Literal["local-gpt"]
    data: list[IngestedDoc]


@ingest_router.post("/ingest/file", tags=["ingest"])
def ingest_file(request: Request, file: UploadFile) -> IngestResponse:
    """
    Ingests a file and returns the response containing the ingested documents.

    Args:
        request (Request): The incoming request object.
        file (UploadFile): The file to be ingested.

    Returns:
        IngestResponse: The response containing the ingested documents.
    """
    service = request.state.injector.get(IngestService)
    if file.filename is None:
        raise HTTPException(status_code=400, detail="No file name provided")
    ingest_documents = service.ingest_bin_data(file.filename, file.file)
    return IngestResponse(object="list", model="local-gpt", data=ingest_documents)


@ingest_router.post("/ingest/text", tags=["ingest"])
def ingest_text(request: Request, body: IngestTextBody) -> IngestResponse:
    """
    Ingests text data into the system.

    Args:
        request (Request): The incoming request object.
        body (IngestTextBody): The request body containing the file name and text.

    Returns:
        IngestResponse: The response object containing the ingested documents.
    """
    service = request.state.injector.get(IngestService)
    if len(body.file_name) == 0:
        raise HTTPException(status_code=400, detail="No file name provided")
    ingest_documents = service.ingest_text(body.file_name, body.text)
    return IngestResponse(object="list", model="local-gpt", data=ingest_documents)


@ingest_router.post("/ingest/list", tags=["ingest"])
def list_ingested(request: Request) -> IngestResponse:
    """
    Retrieve a list of ingested documents.

    Args:
        request (Request): The request object.

    Returns:
        IngestResponse: The response object containing the list of ingested documents.
    """
    service: IngestService = request.state.injector.get(IngestService)
    ingest_documents = service.list_ingested()
    return IngestResponse(object="list", model="local-gpt", data=ingest_documents)


@ingest_router.delete("/ingest/{doc_id}", tags=["ingest"])
def delete_ingested(request: Request, doc_id: str) -> None:
    """
    Deletes the ingested document with the specified ID.

    Args:
        request (Request): The request object.
        doc_id (str): The ID of the document to be deleted.

    Returns:
        None
    """
    service = request.state.injector.get(IngestService)
    service.delete(doc_id)
