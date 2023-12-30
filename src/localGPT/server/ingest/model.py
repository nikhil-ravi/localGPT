from typing import Any, Literal

from llama_index import Document
from pydantic import BaseModel, Field


class IngestedDoc(BaseModel):
    """
    Represents an ingested document.

    Attributes:
        object (Literal["ingest.document"]): The type of object.
        doc_id (str): The ID of the document.
        doc_metadata (dict[str, Any] | None): The metadata of the document.
    """

    object: Literal["ingest.document"]
    doc_id: str = Field(examples=["c202d5e6-7b69-4869-81cc-dd574ee8ee11"])
    doc_metadata: dict[str, Any] | None = Field(
        examples=[
            {
                "page_label": "2",
                "file_name": "test.pdf",
            }
        ]
    )

    @staticmethod
    def curate_metadata(metadata: dict[str, Any]) -> dict[str, Any]:
        """
        Removes specific keys from the metadata.

        Args:
            metadata (dict[str, Any]): The metadata to be curated.

        Returns:
            dict[str, Any]: The curated metadata.
        """
        for key in ["doc_id", "window", "original_text"]:
            metadata.pop(key, None)
        return metadata

    @staticmethod
    def from_document(document: Document) -> "IngestedDoc":
        """
        Creates an IngestedDoc instance from a Document object.

        Args:
            document (Document): The Document object.

        Returns:
            IngestedDoc: The created IngestedDoc instance.
        """
        return IngestedDoc(
            object="ingest.document",
            doc_id=document.doc_id,
            doc_metadata=IngestedDoc.curate_metadata(document.metadata),
        )
