from typing import Literal

from pydantic import BaseModel, Field

from .settings_loader import load_active_settings


class CorsSettings(BaseModel):
    """
    Represents the CORS (Cross-Origin Resource Sharing) settings.

    Attributes:
        enabled (bool): Indicates if CORS is enabled.
        allow_credentials (bool): Indicates if credentials are allowed to be sent with CORS requests.
        allow_origins (list[str]): List of allowed origins for CORS requests.
        allow_origin_regex (str): Regular expression pattern for allowed origins.
        allow_methods (list[str]): List of allowed HTTP methods for CORS requests.
        allow_headers (list[str]): List of allowed headers for CORS requests.
    """

    enabled: bool = Field(default=False)
    allow_credentials: bool = Field(default=False)
    allow_origins: list[str] = Field(default=[])
    allow_origin_regex: str = Field(default=None)
    allow_methods: list[str] = Field(default=["GET"])
    allow_headers: list[str] = Field(default=[])


# class AuthSettings(BaseModel):
#     enabled: bool = Field(default=False)
#     secret: str = Field()


class ServerSettings(BaseModel):
    """
    Represents the settings for the server.

    Attributes:
        env_name (str): Name of the environment (prod, staging, local...)
        port (int): Port to run the server on
        cors (CorsSettings): CORS settings
    """

    env_name: str = Field(
        description="Name of the environment (prod, staging, local...)"
    )
    port: int = Field(default=8001, description="Port to run the server on")
    cors: CorsSettings = Field(
        default=CorsSettings(enabled=False), description="CORS settings"
    )
    # auth: AuthSettings = Field(
    #     default_factory=lambda: AuthSettings(enabled=False, secret="secret-key"),
    #     description="Authentication settings",
    # )


class DataSettings(BaseModel):
    """
    Settings for data related configurations.

    Attributes:
        local_data_folder (str): Path to local data folder
    """

    local_data_folder: str = Field(description="Path to local data folder")


class LLMSettings(BaseModel):
    """
    Settings for the Local Language Model (LLM).

    Attributes:
        mode (Literal["local"]): Mode of LLM.
        max_new_tokens (int): Maximum number of tokens that the LLM is authorized to generate in one completion.
        context_window (int): The number of context tokens for the model.
        tokenizer (str): The model id of a predefined tokenizer hosted inside a model repo on huggingface.co. Valid model ids can be located at the root-level, like `bert-base-uncased`, or namespaced under a user or organization name, like `HuggingFaceH4/zephyr-7b-beta`. If not set, will load a tokenizer matching gpt-3.5-turbo LLM.
    """

    mode: Literal["local"] = Field(description="Mode of LLM")
    max_new_tokens: int = Field(
        default=256,
        description="Maximum number of tokens that the LLM is authorized to generate in one completion.",
    )
    context_window: int = Field(
        default=3900,
        description="The number of context tokens for the model.",
    )
    tokenizer: str = Field(
        None,
        description="The model id of a predefined tokenizer hosted inside a model repo on huggingface.co. Valid model ids can be located at the root-level, like `bert-base-uncased`, or namespaced under a user or organization name, like `HuggingFaceH4/zephyr-7b-beta`. If not set, will load a tokenizer matching gpt-3.5-turbo LLM.",
    )


class VectorstoreSettings(BaseModel):
    """
    Settings for the vector store.

    Attributes:
        database (Literal["qdrant"]): The type of database to use for the vector store.
    """

    database: Literal["qdrant"]


class LocalSettings(BaseModel):
    """
    Represents the local settings for the chat engine.

    Attributes:
        llm_hf_repo_id (str): The ID of the LLM HF repository.
        llm_hf_model_file (str): The file path of the LLM HF model.
        embedding_hf_model_name (str): The name of the embedding HF model.
        prompt_style (Literal["default", "llama2", "tag"]): The prompt style to use for the chat engine. If 'default', use the default prompt style from the llama_index. It should look like 'role: message'. If 'llama2', use the llama2 prompt style from the llama_index. Based on '<s>', '[INST]', and '<<SYS>>'. If 'tag', use the 'tag' prompt style. It should look like '<|role|>: message'. 'llama2' is the historic behavior. 'default' might work better with your custom models.
    """

    llm_hf_repo_id: str
    llm_hf_model_file: str
    embedding_hf_model_name: str
    prompt_style: Literal["default", "llama2", "tag"] = Field(
        "llama2",
        description=(
            "The prompt style to use for the chat engine. "
            "If `default` - use the default prompt style from the llama_index. It should look like `role: message`.\n"
            "If `llama2` - use the llama2 prompt style from the llama_index. Based on `<s>`, `[INST]` and `<<SYS>>`.\n"
            "If `tag` - use the `tag` prompt style. It should look like `<|role|>: message`. \n"
            "`llama2` is the historic behaviour. `default` might work better with your custom models."
        ),
    )


class EmbeddingSettings(BaseModel):
    """
    Settings for embedding.

    Attributes:
        mode (Literal["local"]): Mode of embedding.
        ingest_mode (Literal["simple", "batch", "parallel"]): Ingest mode for embedding.
        count_workers (int): Number of workers for embedding.
    """

    mode: Literal["local"] = Field(description="Mode of Embedding")
    ingest_mode: Literal["simple", "batch", "parallel"] = Field(
        "simple", description="Ingest mode for embedding"
    )
    count_workers: int = Field(2)


class UISettings(BaseModel):
    """
    Represents the settings for the user interface.

    Attributes:
        enabled (bool): Indicates whether the user interface is enabled or not.
        path (str): The path to the user interface.
        default_chat_system_prompt (str, optional): The default system prompt for chat.
        default_query_system_prompt (str, optional): The default system prompt for queries.
    """

    enabled: bool
    path: str
    default_chat_system_prompt: str = Field(None)
    default_query_system_prompt: str = Field(None)


class QdrantSettings(BaseModel):
    """
    Settings for Qdrant instance.

    Attributes:
        location (str | None): If `:memory:` - use in-memory Qdrant instance. If `str` - use it as a `url` parameter.
        url (str | None): Either host or str of 'Optional[scheme], host, Optional[port], Optional[prefix]'.
        port (int | None): Port of Qdrant REST API interface.
        grpc_port (int | None): Port of Qdrant gRPC API interface.
        prefer_grpc (bool | None): If True - use gRPC interface for Qdrant.
        https (bool | None): If True - use https for Qdrant.
        api_key (str | None): API key for authentication in Qdrant cloud.
        prefix (str | None): Prefix to add to the REST URL path. Example: `service/v1` will result in 'http://localhost:6333/service/v1/{qdrant-endpoint}' for REST API.
        timeout (float | None): Timeout for requests to Qdrant.
        host (str | None): Host name of Qdrant service. If url and host are None, set to 'localhost'.
        path (str | None): Persistent path to store QdrantLocal.
        force_disable_same_thread (bool | None): For QdrantLocal, force disable check_same_thread. Default: `True`. Only use this if you can guarantee that you can resolve the thread safety outside QdrantClient.
    """

    location: str | None = Field(
        None,
        description=(
            "If `:memory:` - use in-memory Qdrant instance.\n"
            "If `str` - use it as a `url` parameter.\n"
        ),
    )
    url: str | None = Field(
        None,
        description=(
            "Either host or str of 'Optional[scheme], host, Optional[port], Optional[prefix]'."
        ),
    )
    port: int | None = Field(6333, description="Port of Qdrant REST API interface.")
    grpc_port: int | None = Field(
        6334, description="Port of Qdrant gRPC API interface."
    )
    prefer_grpc: bool | None = Field(False)
    https: bool | None = Field(None)
    api_key: str | None = Field(
        None, description="API key for authentication in Qdrant cloud"
    )
    prefix: str | None = Field(
        None,
        description=(
            "Prefix to add to the REST URL path."
            "Example: `service/v1` will result in "
            "'http://localhost:6333/service/v1/{qdrant-endpoint}' for REST API."
        ),
    )
    timeout: float | None = Field(
        None,
        description=("Timeout for requests to Qdrant."),
    )
    host: str | None = Field(
        None,
        description="Host name of Qdrant service. If url and host are None, set to 'localhost'.",
    )
    path: str | None = Field(
        None,
        description="Persistent path to store QdrantLocal.",
    )
    force_disable_same_thread: bool | None = Field(
        True,
        description=(
            "For QdrantLocal, force disable check_same_thread. Default: `True`"
            "Only use this if you can guarantee that you can resolve the thread safety outside QdrantClient."
        ),
    )


class Settings(BaseModel):
    """
    Represents the settings for the application.

    Attributes:
        server (ServerSettings): The server settings.
        data (DataSettings): The data settings.
        llm (LLMSettings): The LLM settings.
        vectorstore (VectorstoreSettings): The vectorstore settings.
        local (LocalSettings): The local settings.
        embedding (EmbeddingSettings): The embedding settings.
        ui (UISettings): The UI settings.
        qdrant (QdrantSettings): The Qdrant settings.
    """

    server: ServerSettings
    data: DataSettings
    llm: LLMSettings
    vectorstore: VectorstoreSettings
    local: LocalSettings
    embedding: EmbeddingSettings
    ui: UISettings
    qdrant: QdrantSettings


unsafe_settings = load_active_settings()

unsafe_typed_settings = Settings(**unsafe_settings)


def settings() -> Settings:
    """
    Retrieve the global settings object.

    Returns:
        The global settings object.
    """
    from ..di import global_injector

    return global_injector.get(Settings)
