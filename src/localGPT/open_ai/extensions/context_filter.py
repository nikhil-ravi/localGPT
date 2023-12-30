from pydantic import BaseModel, Field


class ContextFilter(BaseModel):
    """
    Represents a context filter.

    Attributes:
        docs_ids (list[str] | None): List of document IDs or None.
    """

    docs_ids: list[str] | None = Field(
        examples=[["c202d5e6-7b69-4869-81cc-dd574ee8ee11"]]
    )
