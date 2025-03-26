# Watch Command Documentation

The `owui_watch` command provides real-time monitoring and synchronization of files with OpenWebUI knowledge bases.

### Features

- Real-time file monitoring
- Automatic synchronization on file changes
- Support for cleanup of removed files

## Usage

```bash
owui_watch --help
uv run owui_watch --help
uv run -m open_webui_knowledge_sync.entrypoints.watch --help

owui_watch --url "http://localhost:8080" --token "sk-12ab3a12345a1a1aa123a1234a1ab123" --knowledge "my_knowledge_name" /path/1 /path/2 /path/3/file.name
OPEN_WEBUI_URL="http://localhost:8080" OPEN_WEBUI_TOKEN="sk-12ab3a12345a1a1aa123a1234a1ab123" owui_watch --knowledge "my_knowledge_id" /path/1 /path/2 /path/3/file.name
```

### Notes

- The watch command will continue running until interrupted
- Changes to files are automatically synchronized
- Supports both file modifications and new file additions
