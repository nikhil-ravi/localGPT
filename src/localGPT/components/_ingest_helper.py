import logging
from pathlib import Path

from llama_index import Document
from llama_index.readers import JSONReader, StringIterableReader
from llama_index.readers.file.base import DEFAULT_FILE_READER_CLS

logger = logging.getLogger(__name__)


FILE_READER_CLS = DEFAULT_FILE_READER_CLS.copy()
FILE_READER_CLS.update({".json": JSONReader})


class IngestionHelper:
    """Helper class to transform files into documents."""

    @staticmethod
    def transform_file_to_documents(file_name: str, file_data: Path) -> list[Document]:
        """Transforms a file into a list of documents.

        Args:
            file_name (str): The name of the file.
            file_data (Path): The path to the file.

        Returns:
            list[Document]: The list of documents.
        """
        documents = IngestionHelper._load_file_to_documents(file_name, file_data)
        for document in documents:
            document.metadata["file_name"] = file_name
        IngestionHelper._exclude_metadata(documents)
        return documents

    def _load_file_to_documents(file_name: str, file_data: Path) -> list[Document]:
        """Helper method to convert a file into a list of documents.

        Args:
            file_name (str): The name of the file.
            file_data (Path): The path to the file.

        Returns:
            list[Document]: The list of documents.
        """
        logger.debug(f"Transforming {file_name=} into documents")
        extension = Path(file_name).suffix
        reader_cls = FILE_READER_CLS.get(extension)
        if reader_cls is None:
            logger.debug(
                f"No reader found for file extension {extension}, using default string reader"
            )
            string_reader = StringIterableReader()
            return string_reader.load_data([file_data.read_text()])

        logger.debug(f"Using reader {reader_cls} for file extension {extension}")
        return reader_cls().load_data(file_data)

    @staticmethod
    def _exclude_metadata(documents: list[Document]) -> None:
        """Helper method to exclude metadata from a list of documents. This is done to stop the embedding search from receiving doc_id and the LLM from receiving file_name, doc_id and page_label in the context.

        Args:
            documents (list[Document]): The list of documents.
        """
        logger.debug(f"Excluding metadata from {len(documents)} documents")
        for document in documents:
            document.metadata["doc_id"] = document.doc_id
            document.excluded_embed_metadata_keys = ["doc_id"]
            document.excluded_llm_metadata_keys = ["file_name", "doc_id", "page_label"]
