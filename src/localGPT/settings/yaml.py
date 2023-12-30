import os
import re
import typing
from typing import Any

from yaml import SafeLoader

_env_replace_matcher = re.compile(r"\$\{(\w|_)+:?.*}")


@typing.no_type_check
def load_yaml_with_envvars(
    stream: typing.TextIO, environ: dict[str, Any] = os.environ
) -> dict[str, Any]:
    """
    Load YAML file with support for environment variables.

    This function takes a YAML file as input and loads its contents into a dictionary.
    It supports the usage of environment variables within the YAML file by replacing
    the variables with their corresponding values from the environment.

    Args:
        stream (typing.TextIO): The input stream containing the YAML file.
        environ (dict[str, Any], optional): The environment variables dictionary.
            Defaults to os.environ.

    Returns:
        dict[str, Any]: The loaded YAML data as a dictionary.

    Raises:
        ValueError: If an environment variable is not set and no default value is provided.

    """
    loader = SafeLoader(stream)

    def load_env_var(_, node) -> str:
        value = str(node.value).removeprefix("${").removesuffix("}")
        split = value.split(":", 1)
        env_var = split[0]
        value = environ.get(env_var)
        default = None if len(split) == 1 else split[1]
        if value is None and default is None:
            raise ValueError(
                f"Environment variable {env_var} is not set and no default value is provided"
            )
        return value or default

    loader.add_implicit_resolver("env_var_replacer", _env_replace_matcher, None)
    loader.add_constructor("env_var_replacer", load_env_var)

    try:
        return loader.get_single_data()
    finally:
        loader.dispose()
