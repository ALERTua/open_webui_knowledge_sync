"""open_webui_knowledge_sync/entrypoints/cli.py"""

from __future__ import annotations

import logging
from pathlib import Path  # noqa: TC003

from typing import Annotated

import typer

from open_webui_knowledge_sync.backends.filesystem import get_filtered_files
from open_webui_knowledge_sync.backends.openwebui.knowledge import OpenWebUIKnowledgeAPI
from open_webui_knowledge_sync.backends.openwebui.files import OpenWebUIFilesAPI

LOG = logging.getLogger(__name__)
app = typer.Typer(add_completion=False)


# noinspection PyShadowingBuiltins
@app.command(no_args_is_help=True)
def sync(  # noqa: C901,PLR0912
    path: Annotated[
        list[Path] | None,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=True,
            readable=True,
            resolve_path=True,
            help="File or Directory to sync. Can be used multiple times.",
        ),
    ] = None,
    knowledge: Annotated[
        str | None,
        typer.Option(
            help="Knowledge Name or ID.",
        ),
    ] = None,
    url: Annotated[
        str | None,
        typer.Option(
            help="Open-WebUI URL. E.g. http://localhost:8080",
        ),
    ] = None,
    token: Annotated[
        str | None,
        typer.Option(
            help="Open-WebUI Token",
        ),
    ] = None,
    cleanup: Annotated[
        bool,
        typer.Option(
            help="After successful upload, cleans up redundant files.",
        ),
    ] = True,
) -> None:
    if not knowledge:
        typer.echo("Please provide either Knowledge ID or Knowledge Name")
        raise typer.Abort

    if not path:
        typer.echo("No path provided")
        raise typer.Abort

    LOG.debug(f"working with poath: {path}")

    owk = OpenWebUIKnowledgeAPI(url=url, token=token)
    knowledge = owk.get_knowledge(knowledge)
    if knowledge is None:
        typer.echo(f"Couldn't find Knowledge: {knowledge}")
        raise typer.Exit(code=1)

    knowledge_id = knowledge.id

    files: list[Path] = []
    for p in path:
        if p.is_file():
            LOG.error(f" file: {p}")
            files.append(p)
        elif p.is_dir():
            LOG.error(f" dir: {p}")
            dir_files = get_filtered_files(p)
            files.extend(dir_files)

    # filter zero size files
    files = [f for f in files if f.stat().st_size > 0]

    if not files:
        typer.echo("No files found")
        raise typer.Exit(code=1)

    LOG.debug(f"Files:\n{'\n'.join([str(f) for f in files])}")
    owf = OpenWebUIFilesAPI(url=url, token=token)
    uploaded = False
    typer.echo(f"Processing {len(files)} files...")
    with typer.progressbar(files) as progress:
        for file_ in progress:
            typer.echo(f" {file_}")
            upload_result = owk.upload_file(file_)
            if upload_result:
                file_id = owf.upload_file(file_)
                if file_id:
                    response = owk.add_file_to_knowledge_by_id(knowledge_id, file_id)
                    if not response:
                        typer.echo(f" {file_} adding to knowledge failed")
                        continue

                    uploaded = True
                else:
                    typer.echo(f" {file_} upload failed")

    if cleanup and uploaded:
        typer.echo("Cleaning up files")
        owf.cleanup()


if __name__ == "__main__":
    app(
        [
            "--knowledge=open-webui-knowledge-sync",
            "V:\\projects\\open-webui-knowledge-sync",
        ],
    )
