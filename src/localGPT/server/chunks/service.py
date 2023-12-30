from typing import TYPE_CHECKING, Literal

from injector import inject, singleton
from llama_index import ServiceContext, StorageContext, VectorStoreIndex
from llama_index.schema import NodeWithScore
from pydantic import BaseModel, Field

from ...components import (
    EmbeddingComponent,
    LLMComponent,
    NodeStoreComponent,
    VectorStoreComponent,
)
from ...open_ai import ContextFilter
from ...server.ingest import IngestedDoc

if TYPE_CHECKING:
    from llama_index.schema import RelatedNodeInfo


class Chunk(BaseModel):
    """
    Represents a chunk of text.

    Attributes:
        object (Literal["context.chunk"]): The object type of the chunk.
        score (float): The score of the chunk.
        document (IngestedDoc): The ingested document associated with the chunk.
        text (str): The text content of the chunk.
        previous_texts (list[str] | None): The list of previous texts, if any.
        next_texts (list[str] | None): The list of next texts, if any.
    """

    object: Literal["context.chunk"]
    score: float = Field(examples=[0.023])
    document: IngestedDoc
    text: str = Field(examples=["This is a chunk of text."])
    previous_texts: list[str] | None = Field(
        examples=[["This is a chunk of text.", "This is another chunk of text."]],
        default=None,
    )
    next_texts: list[str] | None = Field(
        default=None,
        examples=[["This is a chunk of text.", "This is another chunk of text."]],
    )

    @classmethod
    def from_node(cls: type["Chunk"], node: NodeWithScore) -> "Chunk":
        """
        Create a Chunk instance from a NodeWithScore.

        Args:
            node (NodeWithScore): The NodeWithScore object to create the chunk from.

        Returns:
            Chunk: The created Chunk instance.
        """
        doc_id = node.node.ref_doc_id if node.node.ref_doc_id is not None else "-"
        return cls(
            object="context.chunk",
            score=node.score or 0.0,
            document=IngestedDoc(
                object="ingest.document", doc_id=doc_id, doc_metadata=node.node.metadata
            ),
            text=node.get_content(),
        )


@singleton
class ChunksService:
    """
    Service class for handling chunks of text.

    Args:
        llm_component (LLMComponent): The LLM component.
        vector_store_component (VectorStoreComponent): The vector store component.
        embedding_component (EmbeddingComponent): The embedding component.
        node_store_component (NodeStoreComponent): The node store component.
    """

    @inject
    def __init__(
        self,
        llm_component: LLMComponent,
        vector_store_component: VectorStoreComponent,
        embedding_component: EmbeddingComponent,
        node_store_component: NodeStoreComponent,
    ) -> None:
        self.vector_store_component = vector_store_component
        self.storage_context = StorageContext.from_defaults(
            vector_store=vector_store_component.vector_store,
            docstore=node_store_component.doc_store,
            index_store=node_store_component.index_store,
        )
        self.query_service_context = ServiceContext.from_defaults(
            llm=llm_component.llm, embed_model=embedding_component.embedding_model
        )

    def _get_sibling_nodes_text(
        self, node_with_score: NodeWithScore, related_number: int, forward: bool = True
    ) -> list[str]:
        """
        Retrieves the texts of sibling nodes of a given node.

        Args:
            node_with_score (NodeWithScore): The node with score.
            related_number (int): The number of sibling nodes to retrieve.
            forward (bool, optional): Whether to retrieve sibling nodes in the forward direction. Defaults to True.

        Returns:
            list[str]: The texts of the sibling nodes.
        """
        explored_nodes_texts = []
        current_node = node_with_score.node
        for _ in range(related_number):
            explored_node_info: RelatedNodeInfo | None = (
                current_node.next_node if forward else current_node.prev_node
            )
            if explored_node_info is None:
                break
            explored_node = self.storage_context.docstore.get_node(
                explored_node_info.node_id
            )

            explored_nodes_texts.append(explored_node.get_content())
            current_node = explored_node

        return explored_nodes_texts

    def retrieve_relevant(
        self,
        text: str,
        context_filter: ContextFilter | None = None,
        limit: int = 10,
        prev_next_chunks: int = 0,
    ) -> list[Chunk]:
        """
        Retrieves relevant chunks of text based on the given input text.

        Args:
            text (str): The input text.
            context_filter (ContextFilter | None, optional): The context filter. Defaults to None.
            limit (int, optional): The maximum number of chunks to retrieve. Defaults to 10.
            prev_next_chunks (int, optional): The number of previous and next chunks to include. Defaults to 0.

        Returns:
            list[Chunk]: The retrieved chunks of text.
        """
        index = VectorStoreIndex.from_vector_store(
            vector_store=self.vector_store_component.vector_store,
            storage_context=self.storage_context,
            service_context=self.query_service_context,
            show_progress=True,
        )
        vector_index_retriever = self.vector_store_component.get_retriever(
            index=index, context_filter=context_filter, similarity_top_k=limit
        )
        nodes = vector_index_retriever.retrieve(text)
        nodes.sort(key=lambda node: node.score, reverse=True)

        retrieved_nodes = []
        for node in nodes:
            chunk = Chunk.from_node(node)
            chunk.previous_texts = self._get_sibling_nodes_text(
                node, prev_next_chunks, forward=False
            )
            chunk.next_texts = self._get_sibling_nodes_text(
                node, prev_next_chunks, forward=True
            )
            retrieved_nodes.append(chunk)
        return retrieved_nodes
