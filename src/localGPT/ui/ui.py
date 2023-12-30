import itertools
import logging
from pathlib import Path
from typing import Any, Iterable

import gradio as gr
from fastapi import FastAPI
from gradio.themes.utils.colors import slate
from injector import inject, singleton
from llama_index.llms import ChatMessage, ChatResponse, MessageRole
from pydantic import BaseModel

from .._paths import PROJECT_ROOT_PATH
from ..di import global_injector
from ..server import ChatService, ChunksService, IngestService
from ..server.chat import CompletionGen
from ..server.chunks import Chunk
from ..settings import settings

logger = logging.getLogger(__name__)

THIS_DIRECTORY_RELATIVE = Path(__file__).parent.relative_to(PROJECT_ROOT_PATH)
UI_TAB_TITLE = "LocalGPT"
SOURCES_SEPARATOR = "\n\n Sources: \n"
MODES = ["Query Docs", "Search in Docs", "LLM Chat"]


class Source(BaseModel):
    """
    Represents a source with file, page, and text information.

    Attributes:
        file (str): The file name.
        page (str): The page label.
        text (str): The text content.
    """

    file: str
    page: str
    text: str

    class Config:
        frozen = True

    @staticmethod
    def curate_sources(sources: list[Chunk]) -> list["Source"]:
        """
        Curates a list of sources and returns a list of Source objects.

        Args:
            sources (list[Chunk]): The list of Chunk objects to be curated.

        Returns:
            list[Source]: The curated list of Source objects.
        """
        curated_sources = []
        for chunk in sources:
            doc_metadata = chunk.document.doc_metadata

            file_name = doc_metadata.get("file_name", "-") if doc_metadata else "-"
            page_label = doc_metadata.get("page_label", "-") if doc_metadata else "-"
            source = Source(file=file_name, page=page_label, text=chunk.text)
            curated_sources.append(source)
        return curated_sources


@singleton
class UI:
    """
    The UI class represents the user interface for the LocalGPT application.
    It provides methods for interacting with the chatbot, managing system prompts,
    uploading files, and displaying ingested files.

    Args:
        ingest_service (IngestService): The IngestService instance.
        chat_service (ChatService): The ChatService instance.
        chunks_service (ChunksService): The ChunksService instance.
    """

    @inject
    def __init__(
        self,
        ingest_service: IngestService,
        chat_service: ChatService,
        chunks_service: ChunksService,
    ) -> None:
        self._ingest_service = ingest_service
        self._chat_service = chat_service
        self._chunks_service = chunks_service

        # Cache the UI blocks
        self._ui_blocks = None

        # Initialize system prompt based on default mode
        self.mode = MODES[0]
        self._system_prompt = self._get_default_system_prompt(self.mode)

    def _chat(self, message: str, history: list[list[str]], mode: str, *_: Any) -> Any:
        """Performs chat interaction with the assistant.

        Args:
            message (str): The user's message.
            history (list[list[str]]): List of previous user-assistant interactions.
            mode (str): The mode of chat interaction.

        Yields:
            str: The assistant's response or relevant information based on the mode.
        """

        def yield_deltas(completion_gen: CompletionGen) -> Iterable[str]:
            """
            Generator function that yields the deltas of a completion generator.

            Args:
                completion_gen (CompletionGen): The completion generator.

            Yields:
                str: The deltas of the completion generator.

            """
            full_response: str = ""
            stream = completion_gen.response

            for delta in stream:
                if isinstance(delta, str):
                    full_response += str(delta)
                elif isinstance(delta, ChatResponse):
                    full_response += delta.delta or ""
                yield full_response

            if completion_gen.sources:
                full_response += SOURCES_SEPARATOR
                cur_sources = Source.curate_sources(completion_gen.sources)
                sources_text = "\n\n\n".join(
                    f"{index}. {source.file} (page {source.page})"
                    for index, source in enumerate(cur_sources, start=1)
                )
                full_response += sources_text
            yield full_response

        def build_history() -> list[ChatMessage]:
            """
            Builds a list of ChatMessage objects representing the conversation history.

            Returns:
                list[ChatMessage]: The conversation history messages.
            """
            history_messages: list[ChatMessage] = list(
                itertools.chain(
                    *[
                        [
                            ChatMessage(
                                content=interaction[0],
                                role=MessageRole.USER,
                            ),
                            ChatMessage(
                                content=interaction[1].split(SOURCES_SEPARATOR)[0],
                                role=MessageRole.ASSISTANT,
                            ),
                        ]
                        for interaction in history
                    ]
                )
            )

            return history_messages[:20]

        new_message = ChatMessage(content=message, role=MessageRole.USER)
        all_messages = [*build_history(), new_message]

        if self._system_prompt:
            all_messages.insert(
                0, ChatMessage(content=self._system_prompt, role=MessageRole.SYSTEM)
            )
        match mode:
            case "Query Docs":
                query_stream = self._chat_service.stream_chat(
                    messages=all_messages, use_context=True
                )
                yield from yield_deltas(query_stream)
            case "Search in Docs":
                response = self._chunks_service.retrieve_relevant(
                    text=message, limit=4, prev_next_chunks=0
                )
                sources = Source.curate_sources(response)
                yield "\n\n\n".join(
                    f"{index}. **{source.file} "
                    f"(page {source.page})**\n "
                    f"{source.text}"
                    for index, source in enumerate(sources, start=1)
                )
            case "LLM Chat":
                llm_stream = self._chat_service.stream_chat(
                    messages=all_messages, use_context=False
                )
                yield from yield_deltas(llm_stream)

    @staticmethod
    def _get_default_system_prompt(mode: str) -> str:
        """
        Get the default system prompt based on the given mode.

        Args:
            mode (str): The mode for which the default system prompt is needed.

        Returns:
            str: The default system prompt for the given mode.
        """
        p = ""
        match mode:
            case "Query Docs":
                p = settings().ui.default_query_system_prompt
            case "LLM Chat":
                p = settings().ui.default_chat_system_prompt
            case _:
                p = ""
        return p

    def _set_system_prompt(self, system_prompt_input: str) -> None:
        """
        Sets the system prompt to the specified input.

        Args:
            system_prompt_input (str): The input string to set as the system prompt.

        Returns:
            None
        """
        logger.info(f"Setting system prompt to: {system_prompt_input}")
        self._system_prompt = system_prompt_input

    def _set_current_mode(self, mode: str) -> Any:
        """
        Sets the current mode of the UI.

        Args:
            mode (str): The mode to set.

        Returns:
            Any: The result of the gr.update() function call.
        """
        self.mode = mode
        self._set_system_prompt(self._get_default_system_prompt(mode))
        return gr.update(
            placeholder=self._system_prompt,
            interactive=True if self._system_prompt else False,
        )

    def _list_ingested_files(self) -> list[list[str]]:
        """
        Returns a list of ingested file names.

        Returns:
            A list of lists, where each inner list contains a single file name.
        """
        files = set()
        for ingested_document in self._ingest_service.list_ingested():
            if ingested_document.doc_metadata is None:
                continue
            file_name = ingested_document.doc_metadata.get(
                "file_name", "[FILE NAME MISSING]"
            )
            files.add(file_name)
        return [[row] for row in files]

    def _upload_file(self, files: list[str]) -> None:
        """
        Uploads multiple files for bulk ingestion.

        Args:
            files (list[str]): A list of file paths to be uploaded.

        Returns:
            None
        """
        logger.debug(f"Loading {len(files)} files")
        paths = [Path(file) for file in files]
        self._ingest_service.bulk_ingest([(str(path.name), path) for path in paths])

    def _build_ui_blocks(self) -> gr.Blocks:
        """
        Builds the UI blocks for the localGPT application.

        Returns:
            gr.Blocks: The UI blocks.
        """
        logger.debug("Building UI blocks")
        with gr.Blocks(
            title=UI_TAB_TITLE,
            theme=gr.themes.Soft(primary_hue=slate),
            css="",
        ) as blocks:
            with gr.Row(equal_height=False):
                with gr.Column(scale=3):
                    mode = gr.Radio(MODES, label="Mode", value=MODES[0])
                    upload_button = gr.components.UploadButton(
                        label="Upload File(s)",
                        type="filepath",
                        file_count="multiple",
                        size="sm",
                    )
                    ingested_dataset = gr.List(
                        self._list_ingested_files,
                        headers=["File name"],
                        label="Ingested Files",
                        interactive=False,
                        render=False,
                    )
                    upload_button.upload(
                        self._upload_file,
                        inputs=upload_button,
                        outputs=ingested_dataset,
                    )
                    ingested_dataset.change(
                        self._list_ingested_files,
                        outputs=ingested_dataset,
                    )
                    ingested_dataset.render()
                    system_prompt_input = gr.Textbox(
                        placeholder=self._system_prompt,
                        label="System Prompt",
                        lines=3,
                        interactive=True,
                        render=False,
                    )
                    mode.change(
                        self._set_current_mode,
                        inputs=mode,
                        outputs=system_prompt_input,
                    )
                    system_prompt_input.blur(
                        self._set_system_prompt,
                        inputs=system_prompt_input,
                    )

                with gr.Column(scale=7, elem_id="col"):
                    _ = gr.ChatInterface(
                        self._chat,
                        chatbot=gr.Chatbot(
                            label=f"LLM: {settings().llm.mode}",
                            show_copy_button=True,
                            elem_id="chatbot",
                            render=False,
                        ),
                        additional_inputs=[mode, upload_button, system_prompt_input],
                    )
        return blocks

    def get_ui_blocks(self) -> gr.Blocks:
        """
        Retrieves the UI blocks for the LocalGPT application.

        If the UI blocks have not been built yet, this method will build them
        using the _build_ui_blocks() method.

        Returns:
            gr.Blocks: The UI blocks for the LocalGPT application.
        """
        if self._ui_blocks is None:
            self._ui_blocks = self._build_ui_blocks()
        return self._ui_blocks

    def mount_in_app(self, app: FastAPI, path: str) -> None:
        """
        Mounts the UI in the FastAPI app at the specified path.

        Args:
            app (FastAPI): The FastAPI app instance.
            path (str): The path where the UI will be mounted.

        Returns:
            None
        """
        blocks = self.get_ui_blocks()
        blocks.queue()
        logger.info(f"Mounting UI at {path}")
        gr.mount_gradio_app(app, blocks, path)


if __name__ == "__main__":
    ui = global_injector.get(UI)
    _blocks = ui.get_ui_blocks()
    _blocks.queue()
    _blocks.launch(debug=False, show_api=False)
