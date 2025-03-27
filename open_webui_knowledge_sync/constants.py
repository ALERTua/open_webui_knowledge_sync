"""open_webui_knowledge_sync/constants.py"""

EXCLUDES = [
    r".*/",
    r"__pycache__/",
    r"build/",
    r"dist/",
    r"wheels/",
    r"*.egg-info/",
    r".venv/",
    r"**/.*",
    r"*.py[oc]",
    r"**/*.lock",
    r"**/*.tmp",
    r"*~",
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
