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
    filtered_files = [
        _ for _ in all_files
        if _.is_file() and not should_exclude(_) and should_include(_)
    ]
    return filtered_files


if __name__ == "__main__":
    # _directory = Path("C:\\Users\\alexe\\Nextcloud\\Medical\\ALERT")
    _directory = Path("V:\\projects\\hass-gaggiuino")
    _all_files = _directory.rglob("**/*")
    for f in _all_files:
        print(f"{f}: exclude: {should_exclude(f)} include: {should_include(f)}")
