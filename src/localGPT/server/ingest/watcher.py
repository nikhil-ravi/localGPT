from typing import Any, Callable

from fastapi import Path
from watchdog.events import (
    DirCreatedEvent,
    DirModifiedEvent,
    FileCreatedEvent,
    FileModifiedEvent,
    FileSystemEventHandler,
)
from watchdog.observers import Observer


class IngestWatcher:
    """
    A class that watches a specified path for file changes and triggers a callback function when a file is modified or created.

    Args:
        watch_path (Path): The path to watch for file changes.
        on_file_changed (Callable[[Path], None]): The callback function to be called when a file is modified or created.

    Methods:
        start(): Starts the file watcher.
        stop(): Stops the file watcher.
    """

    def __init__(
        self, watch_path: Path, on_file_changed: Callable[[Path], None]
    ) -> None:
        self.watch_path = watch_path
        self.on_file_changed = on_file_changed

        class Handler(FileSystemEventHandler):
            def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
                if isinstance(event, FileModifiedEvent):
                    on_file_changed(Path(event.src_path))

            def on_created(self, event: DirCreatedEvent | FileCreatedEvent) -> None:
                if isinstance(event, FileCreatedEvent):
                    on_file_changed(Path(event.src_path))

        event_handler = Handler()
        observer: Any = Observer()
        self._observer = observer
        self._observer.schedule(event_handler, str(watch_path), recursive=True)

    def start(self) -> None:
        """
        Starts the file watcher.
        """
        self._observer.start()
        while self._observer.is_alive():
            try:
                self._observer.join(1)
            except KeyboardInterrupt:
                break

    def stop(self) -> None:
        """
        Stops the file watcher.
        """
        self._observer.stop()
        self._observer.join()
