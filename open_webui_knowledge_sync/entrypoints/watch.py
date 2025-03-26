"""open_webui_knowledge_sync/entrypoints/watch.py"""

import time
from pathlib import Path
from typing import Annotated

import typer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from open_webui_knowledge_sync.backends.filesystem import should_exclude
from open_webui_knowledge_sync.backends.openwebui.knowledge import OpenWebUIKnowledgeAPI
from open_webui_knowledge_sync.backends.openwebui.files import OpenWebUIFilesAPI


app = typer.Typer(add_completion=False)


class UploadEventHandler(FileSystemEventHandler):
    def __init__(
        self,
        knowledge_id: str,
        url: str,
        token: str,
        cleanup: bool = True,  # noqa: FBT001
    ):
        self.owk = OpenWebUIKnowledgeAPI(url=url, token=token)
        self.owf = OpenWebUIFilesAPI(url=url, token=token)
        self.knowledge_id = knowledge_id
        self.cleanup = cleanup

    def on_modified(self, event):
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if should_exclude(file_path):
            return

        typer.echo(f"Uploading {file_path}")
        upload_result = self.owk.upload_file(file_path)
        uploaded = False
        if upload_result:
            file_id = self.owf.upload_file(file_path)
            if file_id:
                self.owk.add_file_to_knowledge_by_id(self.knowledge_id, file_id)
                uploaded = True
            else:
                typer.echo(f"{file_path} upload failed")
                typer.echo(f"Uploaded and linked: {file_path}")
        else:
            typer.echo(f"{file_path} upload failed")

        if self.cleanup and uploaded:
            typer.echo("Cleaning up files")
            self.owf.cleanup()


def _watch(
    paths: list[str | Path],
    knowledge_id: str,
    url: str,
    token: str,
    cleanup: bool,  # noqa: FBT001
):
    event_handler = UploadEventHandler(knowledge_id, url, token, cleanup=cleanup)
    observer = Observer()

    for path in paths:
        observer.schedule(event_handler, path=str(path), recursive=True)

    typer.echo(f"Watching {len(paths)} paths. Press Ctrl+C to stop...")
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


@app.command(no_args_is_help=True)
def watch(
    path: Annotated[
        list[Path] | None,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=True,
            readable=True,
            resolve_path=True,
            help="File or Directory to watch. Can be used multiple times.",
        ),
    ] = None,
    knowledge: Annotated[
        str | None,
        typer.Option(
            help="Knowledge Name or ID.",
        ),
    ] = None,
    url: Annotated[str | None, typer.Option(help="Open-WebUI URL. E.g. http://localhost:8080")] = None,
    token: Annotated[str | None, typer.Option(help="Open-WebUI Token")] = None,
    cleanup: Annotated[
        bool,
        typer.Option(
            help="After successful upload, cleans up redundant files.",
        ),
    ] = True,
):
    if not knowledge:
        typer.echo("Please provide either Knowledge ID or Knowledge Name")
        raise typer.Abort

    if not path:
        typer.echo("No path provided")
        raise typer.Abort

    owk = OpenWebUIKnowledgeAPI(url=url, token=token)
    knowledge = owk.get_knowledge(knowledge)
    if knowledge is None:
        typer.echo(f"Couldn't find Knowledge: {knowledge}")
        raise typer.Abort

    knowledge_id = knowledge.id

    _watch(paths=path, knowledge_id=knowledge_id, url=url, token=token, cleanup=cleanup)


if __name__ == "__main__":
    app(
        [
            "--knowledge=open-webui-knowledge-sync",
            "V:\\projects\\open-webui-knowledge-sync",
        ],
    )
