import logging
import typing

from injector import inject, singleton
from llama_index import VectorStoreIndex
from llama_index.indices.vector_store import VectorIndexRetriever
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.vector_stores.types import VectorStore
from qdrant_client import QdrantClient

from ..open_ai import ContextFilter
from ..settings import Settings

logger = logging.getLogger(__name__)


@singleton
class VectorStoreComponent:
    """
    A component that manages the vector store for the localGPT application.

    Args:
        settings (Settings): The application settings.

    Raises:
        ConnectionError: If connection to Qdrant fails.
    """

    vector_store: VectorStore

    @inject
    def __init__(self, settings: Settings) -> None:
        if settings.qdrant is None:
            logger.info(
                "Qdrant is not found. Using default settings. Trying to connect to Qdrant at localhost:6333"
            )
            client = QdrantClient()
        else:
            client = QdrantClient(**settings.qdrant.model_dump(exclude_none=True))
        self.vector_store = typing.cast(
            VectorStore,
            QdrantVectorStore(
                client=client,
                collection_name="gpt",
            ),
        )

    @staticmethod
    def get_retriever(
        index: VectorStoreIndex,
        context_filter: ContextFilter | None = None,
        similarity_top_k: int = 2,
    ) -> VectorIndexRetriever:
        """
        Creates a VectorIndexRetriever for the given index.

        Args:
            index (VectorStoreIndex): The vector store index.
            context_filter (ContextFilter | None, optional): The context filter. Defaults to None.
            similarity_top_k (int, optional): The number of similar vectors to retrieve. Defaults to 2.

        Returns:
            VectorIndexRetriever: The vector index retriever.
        """
        return VectorIndexRetriever(
            index=index,
            similarity_top_k=similarity_top_k,
            doc_ids=context_filter.docs_ids if context_filter else None,
        )

    def close(self) -> None:
        """
        Closes the vector store client connection, if available.
        """
        if hasattr(self.vector_store.client, "close"):
            self.vector_store.client.close()
