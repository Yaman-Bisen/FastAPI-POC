import importlib
from config.settings import settings
from starlette.middleware.cors import CORSMiddleware

def setup_middlewares(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_HOSTS,
        allow_credentials=settings.ALLOWED_CREDENTIALS,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )
            
    for middleware_path in settings.MIDDLEWARES:
        module_name, function_name = middleware_path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        middleware_function = getattr(module, function_name)
        app.middleware("http")(middleware_function)
