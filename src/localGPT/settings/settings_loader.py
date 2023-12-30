import functools
import logging
import os
from pathlib import Path
from typing import Any, Iterable

from pydantic.v1.utils import deep_update, unique_list

from .._paths import PROJECT_ROOT_PATH
from .yaml import load_yaml_with_envvars

logger = logging.getLogger(__name__)

_settings_folder = os.environ.get("PGPT_SETTINGS_FOLDER", PROJECT_ROOT_PATH)
active_profiles: list[str] = unique_list(
    ["default"]
    + [
        item.strip()
        for item in os.environ.get("PGPT_PROFILES", "").split(",")
        if item.strip()
    ]
)


def merge_settings(settings: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """
    Merge multiple settings dictionaries into a single dictionary.

    Args:
        settings: An iterable of dictionaries containing settings.

    Returns:
        A dictionary containing the merged settings.
    """
    return functools.reduce(deep_update, settings, {})


def load_settings_from_profile(profile: str) -> dict[str, Any]:
    """
    Load settings from a specific profile.

    Args:
        profile: The name of the profile.

    Returns:
        A dictionary containing the settings for the specified profile.

    Raises:
        ValueError: If the config file has no top-level mapping.
    """
    if profile == "default":
        profile_file_name = "settings.yaml"
    else:
        profile_file_name = f"settings-{profile}.yaml"

    path = Path(_settings_folder) / profile_file_name
    with Path(path).open("r") as f:
        config = load_yaml_with_envvars(f)
    if not isinstance(config, dict):
        raise ValueError(f"Config file has no top-level mapping: {path}")
    return config


def load_active_settings() -> dict[str, Any]:
    """
    Load the active settings based on the active profiles.

    Returns:
        A dictionary containing the merged settings from all active profiles.
    """
    logger.info(f"Starting application with profiles {active_profiles}")
    loaded_profiles = [
        load_settings_from_profile(profile) for profile in active_profiles
    ]
    merged: dict[str, Any] = merge_settings(loaded_profiles)
    return merged
