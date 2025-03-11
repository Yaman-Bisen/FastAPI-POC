import typer

app = typer.Typer(help="Fetch all users command")

@app.command()
def list_users(test_arg: str='test'):
    print(f"Running list_users: test_arg: {test_arg}")
    