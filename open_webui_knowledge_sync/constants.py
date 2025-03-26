"""open_webui_knowledge_sync/constants.py"""

EXCLUDES = [
    "**/.*",
    "**/.*/",
    "**/__pycache__/",
    "*.py[oc]",
    "**/build/",
    "**/dist/",
    "**/wheels/",
    "**/*.egg-info",
    "**/.venv/",
    "**/*.lock",
    "**/*.tmp",
    "*~",
]

INCLUDES = [
    # r"*.py",
    # r"*.pdf",
    # r"*.doc",
    # r"*.docx",
    # r"*.xls",
    # r"*.xlsx",
    # r"*.yaml",
    # r"*.yml",
    # r"*.jpg",
    # r"*.jpeg",
    r"*.*",
]
REQUEST_TIMEOUT = 600
