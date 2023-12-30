import abc
import itertools
import logging
import multiprocessing
import multiprocessing.pool
import os
import threading
from pathlib import Path
from typing import Any

from llama_index import (
    Document,
    ServiceContext,
    StorageContext,
    VectorStoreIndex,
    load_index_from_storage,
)
from llama_index.data_structs import IndexDict
from llama_index.indices.base import BaseIndex
from llama_index.ingestion import run_transformations

from .._paths import local_data_path
from ..settings import Settings
from ._ingest_helper import IngestionHelper

logger = logging.getLogger(__name__)


class BaseIngestComponent(abc.ABC):
    """
    Base class for ingest components.

    Args:
        storage_context (StorageContext): The storage context.
        service_context (ServiceContext): The service context.
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.
    """

    def __init__(
        self,
        storage_context: StorageContext,
        service_context: ServiceContext,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        logger.debug(f"Initializing base ingest component {type(self).__name__}")
        self.storage_context = storage_context
        self.service_context = service_context

    @abc.abstractmethod
    def ingest(self, file_name: str, file_data: Path) -> list[Document]:
        """
        Ingests a single file.

        Args:
            file_name (str): The name of the file.
            file_data (Path): The path to the file.

        Returns:
            list[Document]: The list of ingested documents.
        """
        pass

    @abc.abstractmethod
    def bulk_ingest(self, files: list[tuple[str, Path]]) -> list[Document]:
        """
        Ingests multiple files in bulk.

        Args:
            files (list[tuple[str, Path]]): The list of file name and file path tuples.

        Returns:
            list[Document]: The list of ingested documents.
        """
        pass

    @abc.abstractmethod
    def delete(self, doc_id: str) -> None:
        """
        Deletes a document.

        Args:
            doc_id (str): The ID of the document to delete.
        """
        pass


class BaseIngestComponentWithIndex(BaseIngestComponent, abc.ABC):
    """
    Base class for ingest components with an index.

    This class provides a base implementation for ingest components that require an index.
    It initializes the index, saves the index, and provides a method to delete documents from the index.

    Args:
        storage_context (StorageContext): The storage context for accessing the index.
        service_context (ServiceContext): The service context for accessing the index.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
    """

    def __init__(
        self,
        storage_context: StorageContext,
        service_context: ServiceContext,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(storage_context, service_context, *args, **kwargs)

        self.show_progress = True
        self._index_thread_lock = (
            threading.Lock()
        )  # Thread lock and not multiprocessing lock
        self._index = self._initialize_index()

    def _initialize_index(self) -> BaseIndex[IndexDict]:
        """
        Initialize the index.

        This method initializes the index by loading it from storage or creating a new index if it doesn't exist.

        Returns:
            BaseIndex[IndexDict]: The initialized index.
        """
        try:
            # Load the index with store_nodes_override=True to be able to delete nodes
            index = load_index_from_storage(
                storage_context=self.storage_context,
                service_context=self.service_context,
                store_nodes_override=True,
                show_progress=self.show_progress,
            )
        except ValueError:
            logger.info("Index not found, creating new index")
            index = VectorStoreIndex.from_documents(
                documents=[],
                storage_context=self.storage_context,
                service_context=self.service_context,
                show_progress=self.show_progress,
                store_nodes_override=True,
            )
            index.storage_context.persist(persist_dir=local_data_path)
        return index

    def _save_index(self) -> None:
        """
        Save the index.

        This method saves the index to storage.
        """
        self._index.storage_context.persist(persist_dir=local_data_path)

    def delete(self, doc_id: str) -> None:
        """
        Delete a document from the index.

        This method deletes a document from the index and saves the updated index.

        Args:
            doc_id (str): The ID of the document to delete.
        """
        with self._index_thread_lock:
            self._index.delete_ref_doc(doc_id, delete_from_docstore=True)
            self._save_index()


class SimpleIngestComponent(BaseIngestComponentWithIndex):
    """
    A simple ingest component that transforms files into documents and saves them in an index and document store.

    Args:
        storage_context (StorageContext): The storage context.
        service_context (ServiceContext): The service context.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Attributes:
        _index_thread_lock (threading.Lock): A lock to ensure thread safety when accessing the index.

    """

    def __init__(
        self,
        storage_context: StorageContext,
        service_context: ServiceContext,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(storage_context, service_context, *args, **kwargs)

    def ingest(self, file_name: str, file_data: Path) -> list[Document]:
        """
        Ingests a file by transforming it into documents and saving them in the index and document store.

        Args:
            file_name (str): The name of the file.
            file_data (Path): The path to the file.

        Returns:
            list[Document]: The list of ingested documents.
        """
        logger.info(f"Ingesting {file_name=}")
        documents = IngestionHelper.transform_file_to_documents(file_name, file_data)
        logger.info(f"Transformed {file_name=} to {len(documents)=} documents")
        logger.debug("Saving the documents in the index and doc store")
        return self._save_docs(documents)

    def bulk_ingest(self, files: list[tuple[str, Path]]) -> list[Document]:
        """
        Ingests multiple files by transforming them into documents and saving them in the index and document store.

        Args:
            files (list[tuple[str, Path]]): The list of file name and file data tuples.

        Returns:
            list[Document]: The list of ingested documents.
        """
        saved_documents = []
        for file_name, file_data in files:
            documents = IngestionHelper.transform_file_to_documents(
                file_name, file_data
            )
            saved_documents.extend(self._save_docs(documents))
        return saved_documents

    def _save_docs(self, documents: list[Document]) -> list[Document]:
        """
        Saves the given documents in the index and document store.

        Args:
            documents (list[Document]): The list of documents to save.

        Returns:
            list[Document]: The list of saved documents.
        """
        logger.debug(f"Transforming {len(documents)} documents into nodes")
        with self._index_thread_lock:
            for document in documents:
                self._index.insert(document, show_progress=True)
            logger.debug("Persisting the index and nodes")
            self._save_index()
            logger.debug("Finished persisting the index and nodes")
        return documents


class BatchIngestComponent(BaseIngestComponentWithIndex):
    """Parallelize the file reading and parsing on multiple CPU cores.

    This component is responsible for ingesting files and transforming them into documents.
    It supports parallel processing by utilizing multiple CPU cores and batching the computation
    of embeddings on either GPU or CPU.

    Args:
        storage_context (StorageContext): The storage context for accessing file data.
        service_context (ServiceContext): The service context containing transformations.
        count_workers (int): The number of worker processes to use for parallel processing.
    """

    def __init__(
        self,
        storage_context: StorageContext,
        service_context: ServiceContext,
        count_workers: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(storage_context, service_context, *args, **kwargs)

        assert (
            len(self.service_context.transformations) >= 2
        ), "Embeddings must be in the transformations"
        assert count_workers > 0, "count_workers must be greater than 0"
        self.count_workers = count_workers

        self._file_to_documents_work_pool = multiprocessing.Pool(
            processes=self.count_workers
        )

    def ingest(self, file_name: str, file_data: Path) -> list[Document]:
        """Ingest a single file and transform it into documents.

        Args:
            file_name (str): The name of the file.
            file_data (Path): The path to the file data.

        Returns:
            list[Document]: The list of transformed documents.
        """
        logger.info(f"Ingesting {file_name=}")
        documents = IngestionHelper.transform_file_to_documents(file_name, file_data)
        logger.info(f"Transformed {file_name=} to {len(documents)=} documents")
        logger.debug("Saving the documents in the index and doc store")
        return self._save_docs(documents)

    def bulk_ingest(self, files: list[tuple[str, Path]]) -> list[Document]:
        """Ingest multiple files and transform them into documents.

        Args:
            files (list[tuple[str, Path]]): The list of file name and file data tuples.

        Returns:
            list[Document]: The list of transformed documents.
        """
        documents = list(
            itertools.chain.from_iterable(
                self._file_to_documents_work_pool.starmap(
                    IngestionHelper.transform_file_to_documents, files
                )
            )
        )
        logger.info(f"Transformed {len(files)} files to {len(documents)} documents")
        return self._save_docs(documents)

    def _save_docs(self, documents: list[Document]) -> list[Document]:
        """Save the documents in the index and doc store.

        Args:
            documents (list[Document]): The list of documents to save.

        Returns:
            list[Document]: The list of saved documents.
        """
        logger.debug(f"Transforming {len(documents)} documents into nodes")
        nodes = run_transformations(
            documents,
            self.service_context.transformations,
            show_progress=self.show_progress,
        )
        with self._index_thread_lock:
            logger.info(f"Inserting {len(nodes)} nodes into the index")
            self._index.insert_nodes(nodes, show_progress=True)
            for document in documents:
                self._index.docstore.set_document_hash(
                    document.get_doc_id(), document.hash
                )
            logger.debug("Persisting the index and nodes")
            self._save_index()
            logger.debug("Finished persisting the index and nodes")
        return documents


class ParallelizedIngestComponent(BaseIngestComponentWithIndex):
    """Parallelize the file reading, embedding, and index inserting).

    This class is responsible for parallelizing the process of reading files, embedding them, and inserting them into the index.
    It utilizes both CPU and GPU in parallel, and reduces memory usage by not loading all files into memory at the same time.

    Args:
        storage_context (StorageContext): The storage context object.
        service_context (ServiceContext): The service context object.
        count_workers (int): The number of workers to use for parallel processing.
    """

    def __init__(
        self,
        storage_context: StorageContext,
        service_context: ServiceContext,
        count_workers: int,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        super().__init__(storage_context, service_context, *args, **kwargs)

        assert (
            len(self.service_context.transformations) >= 2
        ), "Embeddings must be in the transformations"
        assert count_workers > 0, "count_workers must be greater than 0"
        self.count_workers = count_workers

        # We are doing our own parallelization, to avoid the tokenizers parallelization by huggingface, we disable it
        os.environ["TOKENIZERS_PARALLELISM"] = "false"

        self._ingest_work_pool = multiprocessing.pool.ThreadPool(
            processes=self.count_workers
        )
        self._file_to_documents_work_pool = multiprocessing.Pool(
            processes=self.count_workers
        )

    def ingest(self, file_name: str, file_data: Path) -> list[Document]:
        """
        Ingests a single file and returns a list of documents.

        Args:
            file_name (str): The name of the file.
            file_data (Path): The path to the file.

        Returns:
            list[Document]: A list of documents.
        """
        logger.info(f"Ingesting {file_name=}")

        # Running in a single process to release the current thread, and take a dedicated CPU core for computation
        documents = self._file_to_documents_work_pool.apply(
            IngestionHelper.transform_file_to_documents, (file_name, file_data)
        )
        logger.info(f"Transformed {file_name=} to {len(documents)=} documents")
        logger.debug("Saving the documents in the index and doc store")
        return self._save_docs(documents)

    def bulk_ingest(self, files: list[tuple[str, Path]]) -> list[Document]:
        """
        Ingests multiple files in parallel and returns a list of documents.

        Args:
            files (list[tuple[str, Path]]): A list of tuples containing the file name and file path.

        Returns:
            list[Document]: A list of documents.
        """
        documents = list(
            itertools.chain.from_iterable(
                self._ingest_work_pool.starmap(self.ingest, files)
            )
        )
        return documents

    def _save_docs(self, documents: list[Document]) -> list[Document]:
        """
        Saves the documents in the index and doc store.

        Args:
            documents (list[Document]): A list of documents.

        Returns:
            list[Document]: The input list of documents.
        """
        logger.debug(f"Transforming {len(documents)} documents into nodes")
        nodes = run_transformations(
            documents,
            self.service_context.transformations,
            show_progress=self.show_progress,
        )
        with self._index_thread_lock:
            logger.info(f"Inserting {len(nodes)} nodes into the index")
            self._index.insert_nodes(nodes, show_progress=True)
            for document in documents:
                self._index.docstore.set_document_hash(
                    document.get_doc_id(), document.hash
                )
            logger.debug("Persisting the index and nodes")
            self._save_index()
            logger.debug("Finished persisting the index and nodes")
        return documents

    def __del__(self):
        logging.debug("Closing the ingest work pool")
        self._ingest_work_pool.close()
        self._ingest_work_pool.join()
        self._ingest_work_pool.terminate()
        logging.debug("Closing the file to documents work pool")
        self._file_to_documents_work_pool.close()
        self._file_to_documents_work_pool.join()
        self._file_to_documents_work_pool.terminate()


def get_ingestion_component(
    storage_context: StorageContext, service_context: ServiceContext, settings: Settings
) -> BaseIngestComponent:
    """
    Returns the appropriate ingestion component based on the ingest_mode specified in the settings.

    Args:
        storage_context (StorageContext): The storage context.
        service_context (ServiceContext): The service context.
        settings (Settings): The settings object.

    Returns:
        BaseIngestComponent: The appropriate ingestion component.

    Raises:
        ValueError: If the ingest_mode is unknown.
    """
    ingest_mode = settings.embedding.ingest_mode
    match ingest_mode:
        case "simple":
            return SimpleIngestComponent(storage_context, service_context)
        case "batch":
            return BatchIngestComponent(
                storage_context,
                service_context,
                count_workers=settings.embedding.count_workers,
            )
        case "parallel":
            return ParallelizedIngestComponent(
                storage_context,
                service_context,
                count_workers=settings.embedding.count_workers,
            )
        case _:
            raise ValueError(f"Unknown ingest_mode {ingest_mode}")
