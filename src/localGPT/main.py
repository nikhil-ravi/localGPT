import llama_index

from .di import global_injector
from .launcher import create_app

llama_index.set_global_handler("simple")
app = create_app(global_injector)
