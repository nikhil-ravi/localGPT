import logging

from injector import inject, singleton
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.embeddings.base import BaseEmbedding

from .._paths import models_cache_path
from ..settings import Settings

logger = logging.getLogger(__name__)


@singleton
class EmbeddingComponent:
    """Component that provides the embedding model."""

    embedding_model: BaseEmbedding

    @inject
    def __init__(self, settings: Settings):
        self.embedding_model = HuggingFaceEmbedding(
            model_name=settings.local.embedding_hf_model_name,
            cache_folder=str(models_cache_path),
        )
