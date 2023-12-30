import logging

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from injector import Injector

from .server import (
    chat_router,
    chunks_router,
    completions_router,
    embeddings_router,
    health_router,
    ingest_router,
)
from .settings import Settings

logger = logging.getLogger(__name__)


def create_app(root_injector: Injector) -> FastAPI:
    async def bind_injector_to_request(request: Request) -> None:
        request.state.injector = root_injector

    app = FastAPI(dependencies=[Depends(bind_injector_to_request)])

    app.include_router(chat_router)
    app.include_router(chunks_router)
    app.include_router(completions_router)
    app.include_router(embeddings_router)
    app.include_router(health_router)
    app.include_router(ingest_router)

    settings = root_injector.get(Settings)
    if settings.server.cors.enabled:
        logger.debug("Setting up CORS middleware")
        app.add_middleware(
            CORSMiddleware,
            allow_credentials=settings.server.cors.allow_credentials,
            allow_origins=settings.server.cors.allow_origins,
            allow_methods=settings.server.cors.allow_methods,
            allow_headers=settings.server.cors.allow_headers,
        )

    if settings.ui.enabled:
        logger.debug("Setting up UI")
        from .ui import UI

        ui = root_injector.get(UI)
        ui.mount_in_app(app, settings.ui.path)
    return app
