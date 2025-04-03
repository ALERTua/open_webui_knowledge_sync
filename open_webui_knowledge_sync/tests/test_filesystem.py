"""open_webui_knowledge_sync/tests/test_filesystem.py"""

from pathlib import Path

from open_webui_knowledge_sync.backends.filesystem import should_include, should_exclude


def test_include_exclude():
    _file = Path("V:\\projects\\project\\.venv\\Lib\\site-packages\\botocore\\paginators-1.json")
    assert should_exclude(_file), f"should exclude {_file}"

    _file = Path("V:\\projects\\open-webui-knowledge-sync\\.git\\config")
    assert should_exclude(_file), f"should exclude {_file}"

    _file = Path("V:\\projects\\open-webui-knowledge-sync\\.gitignore")
    assert should_exclude(_file), f"should exclude {_file}"

    _file = Path("V:\\projects\\open-webui-knowledge-sync\\pyproject.toml")
    assert not should_exclude(_file), f"should not exclude {_file}"
    assert should_include(_file), f"should include {_file}"
