from pathlib import Path

from open_webui_knowledge_sync.backends.filesystem import should_include, should_exclude


def test_include_exclude():
    _file = Path("V:\\projects\\project\\.venv\\Lib\\site-packages\\botocore\\paginators-1.json")
    assert should_include(_file)
    assert should_exclude(_file)
