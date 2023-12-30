import uvicorn

from .main import app
from .settings import settings

uvicorn.run(app, port=settings().server.port, log_config=None)
