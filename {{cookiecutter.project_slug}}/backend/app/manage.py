import typer
import graphql

from app.core.config import settings
from app.graphql.schema import schema

app = typer.Typer()


@app.command()
def print_schema():
    typer.echo(graphql.print_schema(schema))


@app.command()
def print_settings():
    typer.echo(settings)


if __name__ == "__main__":
    app()
