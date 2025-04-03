"""open_webui_knowledge_sync/backends/filesystem.py"""

import re
import logging

from pathlib import Path

from open_webui_knowledge_sync.constants import EXCLUDES, INCLUDES

LOG = logging.getLogger(__name__)


def matches_any_pattern(path: Path, patterns: list[str]) -> bool:
    """Check if a given path matches any of the exclusion patterns."""
    normalized_path = Path(path).resolve().as_posix()

    for pattern in patterns:
        try:
            compiled = re.compile(
                pattern.replace("**", "[^/]+").replace("*", "[^/]*"),
                flags=re.IGNORECASE,
            )
            if compiled.search(normalized_path):
                LOG.debug(f"{path} matches: {pattern}")
                return True
        except re.error:
            # If the pattern is invalid, skip it
            continue

    return False


def should_exclude(path: Path):
    """Check if the path matches any exclusion pattern."""
    return matches_any_pattern(path, EXCLUDES)


def should_include(path: Path):
    """Check if the path matches any inclusion pattern."""
    return matches_any_pattern(path, INCLUDES)


def get_filtered_files(directory: Path):
    """Recursively find files matching INCLUDES while avoiding EXCLUDES."""
    all_files = directory.rglob("**/*")  # Get all files and directories
    return [_ for _ in all_files if _.is_file() and not should_exclude(_) and should_include(_)]


if __name__ == "__main__":
    pass
