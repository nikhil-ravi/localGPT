import argparse
import os
import shutil

from huggingface_hub import hf_hub_download, snapshot_download
from transformers import AutoTokenizer

from ._paths import models_cache_path, models_path
from .settings import settings

parser = argparse.ArgumentParser(prog="Setup: Download models from huggingface.co")
parser.add_argument(
    "--resume",
    default=True,
    action=argparse.BooleanOptionalAction,
    help="Enable or disable resuming downloads.",
)


def setup() -> None:
    """
    Performs the setup process for the localGPT application.
    This function downloads the required models, creates necessary directories, and initializes the tokenizer.
    """
    args = parser.parse_args()
    resume_download = args.resume

    os.makedirs(models_path, exist_ok=True)

    # Download Embedding model
    embedding_path = models_path / "embedding"
    print(f"Downloading embedding {settings().local.embedding_hf_model_name}")
    snapshot_download(
        repo_id=settings().local.embedding_hf_model_name,
        cache_dir=models_cache_path,
        local_dir=embedding_path,
    )
    print("Embedding model downloaded.")

    # Download LLM and create a symlink to the model file
    print(f"Downloading LLM {settings().local.llm_hf_model_file}")
    hf_hub_download(
        repo_id=settings().local.llm_hf_repo_id,
        filename=settings().local.llm_hf_model_file,
        cache_dir=models_cache_path,
        local_dir=models_path,
        resume_download=resume_download,
    )
    print("LLM model downloaded.")

    # Download tokenizer
    print(f"Downloading tokenizer {settings().llm.tokenizer}")
    AutoTokenizer.from_pretrained(
        pretrained_model_name_or_path=settings().llm.tokenizer,
        cache_dir=models_cache_path,
    )
    print("Tokenizer downloaded.")

    print("Setup complete.")


def wipe_local_data() -> None:
    """
    Wipes the local data directory by removing all files and subdirectories, except for the .gitignore file.

    Raises:
        PermissionError: If a file or directory cannot be removed due to permission restrictions.
    """
    path = "local_data"
    print(f"Wiping {path}...")
    all_files = os.listdir(path)

    files_to_remove = [file for file in all_files if file != ".gitignore"]
    for file_name in files_to_remove:
        file_path = os.path.join(path, file_name)
        try:
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            elif os.path.isfile(file_path):
                os.remove(file_path)
            print(f"Removed {file_path}")
        except PermissionError:
            print(
                f"PermissionError: Failed to remove {file_path}. It is in use by another process."
            )
            continue
    print(f"{path} wiped.")
