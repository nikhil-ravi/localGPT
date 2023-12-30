from pathlib import Path

PROJECT_ROOT_PATH: Path = Path(__file__).parents[2]
models_path: Path = PROJECT_ROOT_PATH / "models"
models_cache_path: Path = models_path / "cache"
local_data_path: Path = PROJECT_ROOT_PATH / "local_data"
