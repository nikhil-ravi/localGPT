from injector import Injector

from .settings import Settings, unsafe_typed_settings


def create_application_injector() -> Injector:
    _injector = Injector(auto_bind=True)
    _injector.binder.bind(Settings, to=unsafe_typed_settings)
    return _injector


global_injector: Injector = create_application_injector()
