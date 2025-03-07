import logging
import uvicorn
import typer

logger = logging.getLogger(__name__)
app = typer.Typer()

@app.command()
def runserver(
    host: str=None,
    # host: str = typer.Option("127.0.0.1", help="Host address to bind to"),
    # port: int = typer.Option(8000, help="Port to bind to"),
    # reload: bool = typer.Option(True, help="Enable auto-reload"),
    # workers: int = typer.Option(1, help="Number of worker processes"),
    # log_level: str = typer.Option("info", help="Logging level")
):
    print('hello')
    # """Run the FastAPI development server."""
    # logger.info(f"Starting server at {host}:{port} (reload: {reload}, workers: {workers})")

    # try:
    #     uvicorn.run(
    #         "app.main:app",
    #         host=host,
    #         port=port,
    #         reload=reload,
    #         workers=workers,
    #         log_level=log_level
    #     )
    # except Exception as e:
    #     logger.error(f"Error starting server: {e}")

if __name__ == "__main__":
    app()
