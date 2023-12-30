import logging
import tempfile
from pathlib import Path
from typing import AnyStr, BinaryIO

from injector import inject, singleton
from llama_index import ServiceContext, StorageContext
from llama_index.node_parser import SentenceWindowNodeParser

from ...components import (
    EmbeddingComponent,
    LLMComponent,
    NodeStoreComponent,
    VectorStoreComponent,
    get_ingestion_component,
)
from ...settings import settings
from .model import IngestedDoc

logger = logging.getLogger(__name__)


@singleton
class IngestService:
    """
    Service class for ingesting files into the system.

    Args:
        llm_component (LLMComponent): The LLMComponent instance.
        vector_store_component (VectorStoreComponent): The VectorStoreComponent instance.
        embedding_component (EmbeddingComponent): The EmbeddingComponent instance.
        node_store_component (NodeStoreComponent): The NodeStoreComponent instance.
    """

    @inject
    def __init__(
        self,
        llm_component: LLMComponent,
        vector_store_component: VectorStoreComponent,
        embedding_component: EmbeddingComponent,
        node_store_component: NodeStoreComponent,
    ) -> None:
        self.llm_service = llm_component
        self.storage_context = StorageContext.from_defaults(
            vector_store=vector_store_component.vector_store,
            docstore=node_store_component.doc_store,
            index_store=node_store_component.index_store,
        )
        node_parser = SentenceWindowNodeParser.from_defaults()
        self.ingest_service_context = ServiceContext.from_defaults(
            llm=self.llm_service.llm,
            embed_model=embedding_component.embedding_model,
            node_parser=node_parser,
            transformations=[node_parser, embedding_component.embedding_model],
        )
        self.ingest_component = get_ingestion_component(
            self.storage_context, self.ingest_service_context, settings=settings()
        )

    def _ingest_data(self, file_name: str, file_data: AnyStr) -> list[IngestedDoc]:
        """
        Ingests the given file data into the system.

        Args:
            file_name (str): The name of the file.
            file_data (AnyStr): The data of the file.

        Returns:
            list[IngestedDoc]: The list of ingested documents.
        """
        logger.debug(f"Got file data of size {len(file_data)} to ingest.")
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            try:
                path_to_tmp = Path(tmp.name)
                if isinstance(file_data, bytes):
                    path_to_tmp.write_bytes(file_data)
                else:
                    path_to_tmp.write_text(str(file_data))
                return self.ingest_file(file_name, path_to_tmp)
            finally:
                tmp.close()
                path_to_tmp.unlink()

    def ingest_file(self, file_name: str, path_to_file: Path) -> list[IngestedDoc]:
        """
        Ingests the file at the given path into the system.

        Args:
            file_name (str): The name of the file.
            path_to_file (Path): The path to the file.

        Returns:
            list[IngestedDoc]: The list of ingested documents.
        """
        logger.info(f"Ingesting {file_name}.")
        documents = self.ingest_component.ingest(
            file_name=file_name, file_data=path_to_file
        )
        logger.info(f"Finished ingesting {file_name}.")
        return [IngestedDoc.from_document(document) for document in documents]

    def ingest_text(self, file_name: str, text: str) -> list[IngestedDoc]:
        """
        Ingests the given text data into the system.

        Args:
            file_name (str): The name of the text data.
            text (str): The text data.

        Returns:
            list[IngestedDoc]: The list of ingested documents.
        """
        logger.info(f"Ingesting text data with {file_name=}.")
        return self._ingest_data(file_name, text)

    def ingest_bin_data(
        self, file_name: str, raw_file_data: BinaryIO
    ) -> list[IngestedDoc]:
        """
        Ingests the given binary data into the system.

        Args:
            file_name (str): The name of the binary data.
            raw_file_data (BinaryIO): The binary data.

        Returns:
            list[IngestedDoc]: The list of ingested documents.
        """
        logger.info(f"Ingesting binary data with {file_name=}.")
        file_data = raw_file_data.read()
        return self._ingest_data(file_name, file_data)

    def bulk_ingest(self, files: list[tuple[str, Path]]) -> list[IngestedDoc]:
        """
        Performs bulk ingestion of multiple files into the system.

        Args:
            files (list[tuple[str, Path]]): The list of file name and path tuples.

        Returns:
            list[IngestedDoc]: The list of ingested documents.
        """
        logger.info(f"Ingesting {[file[0] for file in files]}.")
        documents = self.ingest_component.bulk_ingest(files)
        logger.info(f"Finished ingesting {[file[0] for file in files]}.")
        return [IngestedDoc.from_document(document) for document in documents]

    def list_ingested(self) -> list[IngestedDoc]:
        """
        Retrieves the list of ingested documents.

        Returns:
            list[IngestedDoc]: The list of ingested documents.
        """
        ingested_docs = []
        try:
            docstore = self.storage_context.docstore
            ingested_docs_ids: set[str] = set()

            for node in docstore.docs.values():
                if node.ref_doc_id is not None:
                    ingested_docs_ids.add(node.ref_doc_id)

            for doc_id in ingested_docs_ids:
                ref_doc_info = docstore.get_ref_doc_info(doc_id)
                doc_metadata = None
                if ref_doc_info is not None and ref_doc_info.metadata is not None:
                    doc_metadata = IngestedDoc.curate_metadata(ref_doc_info.metadata)
                ingested_docs.append(
                    IngestedDoc(
                        object="ingest.document",
                        doc_id=doc_id,
                        doc_metadata=doc_metadata,
                    )
                )
        except ValueError:
            logger.warning(
                "Got an exception while getting list of docs.", exc_info=True
            )
            pass
        logger.debug(f"Got {len(ingested_docs)} ingested docs.")
        return ingested_docs

    def delete(self, doc_id: str) -> None:
        """
        Deletes the ingested document with the given ID.

        Args:
            doc_id (str): The ID of the document to delete.
        """
        logger.info(f"Deleting {doc_id}.")
        self.ingest_component.delete(doc_id)
