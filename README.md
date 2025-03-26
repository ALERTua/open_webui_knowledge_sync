# Open WebUI Knowledge Sync

A Python CLI tool for synchronizing local files with Open WebUI knowledge bases.

Repository: https://github.com/ALERTua/open_webui_knowledge_sync


## Features

- One-time sync of files and/or directories with Open WebUI knowledge bases
- Real-time file watching and automatic synchronization
- Command-line interface for easy integration


## Requirements

- Open WebUI instance
- [uv](https://docs.astral.sh/uv/getting-started/installation/)


## Installation

```bash
git clone https://github.com/ALERTua/open_webui_knowledge_sync.git
cd open_webui_knowledge_sync
uv sync
```

## Settings

You can save the effort of providing the CLI with the Open WebUI URL and Token for each execution
by creating an `.env` file from [.env.example](.env.example) and filling it with the environment variables.
Or you can just fill those in your system.

## Command-line Tools

This package provides two main command-line tools:

- `owui_sync`: One-time synchronization of files and directories
- `owui_watch`: Continuous monitoring and synchronization of files

For detailed usage instructions, see:
- [Sync Usage](docs/sync-readme)
- [Watch Usage](docs/watch-readme.md)
