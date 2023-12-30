from typing import Literal

from injector import SingletonScope, inject
from pydantic import BaseModel, Field

from ...components import EmbeddingComponent


class Embedding(BaseModel):
    """
    Represents an embedding object.

    Attributes:
        index (int): The index of the embedding.
        object (Literal["embedding"]): The type of object, which should always be "embedding".
        embedding (list[float]): The embedding values.
    """

    index: int
    object: Literal["embedding"]
    embedding: list[float] = Field(examples=[[0.002306423, -0.424814]])


@SingletonScope
class EmbeddingService:
    """
    A service class for generating embeddings from texts using an embedding component.

    Args:
        embedding_component (EmbeddingComponent): The embedding component used for generating embeddings.
    """

    @inject
    def __init__(self, embedding_component: EmbeddingComponent) -> None:
        self.embedding_component = embedding_component.embedding_model

    def texts_embeddings(self, texts: list[str]) -> list[Embedding]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts (list[str]): The texts for which embeddings need to be generated.

        Returns:
            list[Embedding]: A list of Embedding objects containing the index, object type, and embedding for each text.
        """
        texts_embeddings = self.embedding_component.get_text_embedding_batch(texts)
        return [
            Embedding(
                index=texts_embeddings.index(embedding),
                object="embedding",
                embedding=embedding,
            )
            for embedding in texts_embeddings
        ]
