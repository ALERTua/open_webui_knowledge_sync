"""open_webui_knowledge_sync/backends/openwebui/knowledge.py"""

from __future__ import annotations

import logging
import requests

from open_webui_knowledge_sync.constants import REQUEST_TIMEOUT
from open_webui_knowledge_sync.env import OPEN_WEBUI_URL, OPEN_WEBUI_TOKEN
from open_webui_knowledge_sync.models.knowledge import (
    KnowledgeUserResponse,
    KnowledgeForm,
    KnowledgeResponse,
    KnowledgeFilesResponse,
    KnowledgeFileIdForm,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class OpenWebUIKnowledgeAPI:
    def __init__(self, url=OPEN_WEBUI_URL, token=OPEN_WEBUI_TOKEN):
        self.url = url or OPEN_WEBUI_URL
        self.url = self.url.rstrip("/")
        self.token = token or OPEN_WEBUI_TOKEN
        self.base_url = f"{self.url}/api/v1/knowledge"
        self.headers_auth = {
            "Authorization": f"Bearer {self.token}",
        }
        self.headers = {
            **self.headers_auth,
            "Content-Type": "application/json",
        }

    def upload_file(
        self,
        file_path: str | Path,
    ) -> str | None:
        url = f"{self.url}/api/v1/files/"
        with file_path.open("rb") as f:
            # , data={'file_metadata': file_metadata}
            response = requests.post(url, headers=self.headers_auth, files={"file": f}, timeout=REQUEST_TIMEOUT)

        if response.status_code == requests.status_codes.codes.ok:
            return response.json().get("id")

        logger.warning(f"Failed to upload: {file_path}. Status code: {response.status_code}: {response.text}")
        return None

    def get_knowledge_list(self) -> list[KnowledgeUserResponse]:
        url = f"{self.base_url}/list"
        response = requests.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
        return [KnowledgeUserResponse(**_) for _ in response.json()]

    def create_new_knowledge(
        self,
        knowledge_data: KnowledgeForm,
    ) -> KnowledgeResponse | None:
        url = f"{self.base_url}/create"
        response = requests.post(url, headers=self.headers, json=knowledge_data, timeout=REQUEST_TIMEOUT)
        if response.status_code != requests.status_codes.codes.created:
            return None

        return KnowledgeResponse(**response.json())

    def get_knowledge(self, knowledge_id_or_name: str):
        return self.get_knowledge_by_id(knowledge_id_or_name) or self.get_knowledge_by_name(knowledge_id_or_name)

    def get_knowledge_by_id(
        self,
        knowledge_id: str,
    ) -> KnowledgeFilesResponse | None:
        url = f"{self.base_url}/{knowledge_id}"
        response = requests.get(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != requests.status_codes.codes.ok:
            return None

        return KnowledgeFilesResponse(**response.json())

    def get_knowledge_by_name(
        self,
        knowledge_name: str,
    ) -> KnowledgeFilesResponse | None:
        knowledges = self.get_knowledge_list()
        if knowledges:
            return next((_ for _ in knowledges if _.name.lower() == knowledge_name.lower()), None)

        return None

    def update_knowledge_by_id(
        self,
        knowledge_id: str,
        knowledge_data: KnowledgeForm,
    ) -> KnowledgeFilesResponse | None:
        url = f"{self.base_url}/{knowledge_id}/update"
        response = requests.put(url, headers=self.headers, json=knowledge_data, timeout=REQUEST_TIMEOUT)
        if response.status_code != requests.status_codes.codes.ok:
            return None

        return KnowledgeFilesResponse(**response.json())

    def add_file_to_knowledge_by_id(
        self,
        knowledge_id: str,
        file_id: str,
    ) -> KnowledgeResponse | None:
        url = f"{self.base_url}/{knowledge_id}/file/add"
        data = {"file_id": file_id}
        response = requests.post(url, headers=self.headers, json=data, timeout=REQUEST_TIMEOUT)
        if response.status_code != requests.status_codes.codes.ok:
            return None

        return KnowledgeResponse(**response.json())

    def update_file_from_knowledge_by_id(
        self,
        knowledge_id: str,
        file_id: KnowledgeFileIdForm,
    ) -> KnowledgeFilesResponse | None:
        url = f"{self.base_url}/{knowledge_id}/file/update"
        data = {"id": file_id}
        response = requests.post(url, headers=self.headers, json=data, timeout=REQUEST_TIMEOUT)
        if response.status_code != requests.status_codes.codes.ok:
            return None

        return KnowledgeFilesResponse(**response.json())

    def remove_file_from_knowledge_by_id(
        self,
        knowledge_id: str,
        file_id: KnowledgeFileIdForm,
    ) -> KnowledgeFilesResponse | None:
        url = f"{self.base_url}/{knowledge_id}/file/remove"
        data = {"id": file_id}
        response = requests.post(url, headers=self.headers, json=data, timeout=REQUEST_TIMEOUT)
        if response.status_code != requests.status_codes.codes.ok:
            return None

        return KnowledgeFilesResponse(**response.json())

    def delete_knowledge_by_id(
        self,
        knowledge_id: str,
    ) -> bool:
        url = f"{self.base_url}/{knowledge_id}/delete"
        response = requests.delete(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
        return response.status_code == requests.status_codes.codes.ok

    def reset_knowledge_by_id(
        self,
        knowledge_id: str,
    ) -> KnowledgeResponse | None:
        url = f"{self.base_url}/{knowledge_id}/reset"
        response = requests.post(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
        if response.status_code != requests.status_codes.codes.ok:
            return None

        return KnowledgeResponse(**response.json())


def __main():
    kn = OpenWebUIKnowledgeAPI()
    knowledge = kn.get_knowledge("Health")  # noqa: F841


if __name__ == "__main__":
    __main()
