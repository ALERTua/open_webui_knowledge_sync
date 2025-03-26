from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer

from open_webui_knowledge_sync.backends.filesystem import get_filtered_files
from open_webui_knowledge_sync.backends.openwebui.knowledge import OpenWebUIKnowledgeAPI
from open_webui_knowledge_sync.backends.openwebui.files import OpenWebUIFilesAPI

app = typer.Typer()


# noinspection PyShadowingBuiltins
@app.command(no_args_is_help=True)
def sync(
        knowledge_id: Annotated[
            str,
            typer.Option(
                help="Knowledge ID."
            ),
        ] = None,
        knowledge_name: Annotated[
            str,
            typer.Option(
                help="Knowledge Name."
            ),
        ] = None,
        file: Annotated[
            list[Path],
            typer.Option(
                exists=True,
                file_okay=True,
                dir_okay=False,
                readable=True,
                resolve_path=True,
                help="File to sync. Can be used multiple times."
            ),
        ] = None,
        dir: Annotated[
            list[Path],
            typer.Option(
                exists=True,
                file_okay=False,
                dir_okay=True,
                readable=True,
                resolve_path=True,
                help="Directory to sync. Can be used multiple times."
            ),
        ] = None,
        url: Annotated[str, typer.Option(help="Open-WebUI URL. E.g. http://localhost:8080")] = None,
        token: Annotated[str, typer.Option(help="Open-WebUI Token")] = None,
        cleanup: Annotated[
            bool,
            typer.Option(
                help="After successful upload, cleans up redundant files.",
            ),
        ] = True,
) -> None:
    if knowledge_id and knowledge_name:
        typer.echo("Please provide either Knowledge ID or Knowledge Name")
        raise typer.Abort()

    if not file and not dir:
        typer.echo("No file and directories provided")
        raise typer.Abort()

    file = file or []
    dir = dir or []

    owk = OpenWebUIKnowledgeAPI(url=url, token=token)
    if knowledge_name:
        knowledge = owk.get_knowledge_by_name(knowledge_name)
        if knowledge is None:
            typer.echo(f"Couldn't find Knowledge ID by Name: {knowledge_name}")
            raise typer.Abort()

        knowledge_id = knowledge.id

    files = file
    for dir_ in dir:
        dir_files = get_filtered_files(dir_)
        files.extend(dir_files)

    owf = OpenWebUIFilesAPI(url=url, token=token)
    uploaded = False
    with typer.progressbar(files, label=f"Processing {len(files)} files...") as progress:
        for file_ in progress:
            typer.echo(file_)
            upload_result = owk.upload_file(file_)
            if upload_result:
                file_id = owf.upload_file(file_)
                if file_id:
                    owk.add_file_to_knowledge_by_id(knowledge_id, file_id)
                    uploaded = True
                else:
                    typer.echo(f"{file_} upload failed")

    if cleanup and uploaded:
        typer.echo("Cleaning up files")
        owf.cleanup()


if __name__ == "__main__":
    # app([
    #     "--knowledge-name=test_script",
    #     '--file=V:\\projects\\hass-gaggiuino\\custom_components\\gaggiuino\\coordinator.py',
    #     '--file=V:\\projects\\hass-gaggiuino\\custom_components\\gaggiuino\\coordinator.py',
    #     '--dir=V:\\projects\\hass-gaggiuino\\custom_components',
    # ])
    app([
        "--knowledge-name=Health",
        '--dir=C:\\Users\\alexe\\Nextcloud\\Medical\\ALERT',
    ])
