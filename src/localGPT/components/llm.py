import logging

from injector import inject, singleton
from llama_index import set_global_tokenizer
from llama_index.llms import LLM, LlamaCPP
from transformers import AutoTokenizer

from .._paths import models_cache_path, models_path
from ..settings import Settings
from ._prompt_helper import Llama2PromptStyle

logger = logging.getLogger(__name__)


@singleton
class LLMComponent:
    """
    This class represents the LLMComponent, which is responsible for managing the LLM model.

    Args:
        settings (Settings): The settings object containing the configuration for the LLMComponent.
    """

    llm: LLM

    @inject
    def __init__(self, settings: Settings):
        if settings.llm.tokenizer:
            set_global_tokenizer(
                AutoTokenizer.from_pretrained(
                    pretrained_model_name_or_path=settings.llm.tokenizer,
                    cache_dir=str(models_cache_path),
                )
            )

        prompt_style = Llama2PromptStyle()

        self.llm = LlamaCPP(
            model_path=str(models_path / "mistral-7b-instruct-v0.2.Q4_K_M.gguf"),
            temperature=0.1,
            max_new_tokens=settings.llm.max_new_tokens,
            context_window=settings.llm.context_window,
            generate_kwargs={},
            model_kwargs={"n_gpu_layers": -1},
            messages_to_prompt=prompt_style.messages_to_prompt,
            completion_to_prompt=prompt_style.completion_to_prompt,
            verbose=True,
        )
