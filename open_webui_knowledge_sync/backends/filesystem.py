"""open_webui_knowledge_sync/backends/filesystem.py"""

import fnmatch
from pathlib import Path

from open_webui_knowledge_sync.constants import EXCLUDES, INCLUDES


def should_exclude(path: Path):
    """Check if the path matches any exclusion pattern."""
    return any(fnmatch.fnmatch(str(path), pattern) for pattern in EXCLUDES)


def should_include(path: Path):
    """Check if the path matches any inclusion pattern."""
    return any(fnmatch.fnmatch(str(path), pattern) for pattern in INCLUDES)


def get_filtered_files(directory: Path):
    """Recursively find files matching INCLUDES while avoiding EXCLUDES."""
    all_files = directory.rglob("**/*")  # Get all files and directories
    return [_ for _ in all_files if _.is_file() and not should_exclude(_) and should_include(_)]


if __name__ == "__main__":
    pass
