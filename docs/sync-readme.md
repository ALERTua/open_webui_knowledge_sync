# Sync Command Documentation

The `owui_sync` command provides one-time synchronization of files and directories with Open WebUI knowledge bases.

## Usage

```bash
owui_sync --help
uv run owui_sync --help
uv run -m open_webui_knowledge_sync.entrypoints.sync --help

owui_sync --url "http://localhost:8080" --token "sk-12ab3a12345a1a1aa123a1234a1ab123" --knowledge "my_knowledge_name" /path/1 /path/2 /path/3/file.name
OPEN_WEBUI_URL="http://localhost:8080" OPEN_WEBUI_TOKEN="sk-12ab3a12345a1a1aa123a1234a1ab123" owui_sync --knowledge "my_knowledge_id" /path/1 /path/2 /path/3/file.name
```
