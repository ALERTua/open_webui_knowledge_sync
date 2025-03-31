"""open_webui_knowledge_sync/constants.py"""

EXCLUDES = [
    r".*",
    r".*/",
    r"*~",
    r"__pycache__/",
    r"build/",
    r"dist/",
    r"wheels/",
    r"*.egg-info/",
    r".venv/",
    r"*.py[oc]",
    r"*.lock",
    r"*.tmp",
    r"*.typed",
    r"*.gz",
    r"*.zip",
    r"*.rar",
    r"*.7z",
    r"*.whl",
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
