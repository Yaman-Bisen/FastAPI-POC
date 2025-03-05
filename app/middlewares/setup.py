import importlib
from config.settings import settings

def setup_middlewares(app):
    for middleware_path in settings.MIDDLEWARES:
        module_name, function_name = middleware_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        middleware_function = getattr(module, function_name)
        app.middleware("http")(middleware_function)
