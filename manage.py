import typer
from app.management.commands import runserver_command, fetch_users_cron

app = typer.Typer(help="FastAPI Management Commands")

app.add_typer(runserver_command.app)
app.add_typer(fetch_users_cron.app)

if __name__ == "__main__":
    app()