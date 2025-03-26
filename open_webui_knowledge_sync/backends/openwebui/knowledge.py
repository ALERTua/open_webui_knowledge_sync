from __future__ import annotations

from pathlib import Path
from typing import Optional

import requests

from open_webui_knowledge_sync.env import OPEN_WEBUI_URL, OPEN_WEBUI_TOKEN
from open_webui_knowledge_sync.models.files import FileModelResponse
from open_webui_knowledge_sync.models.knowledge import (
    KnowledgeUserResponse,
    KnowledgeForm,
    KnowledgeResponse,
    KnowledgeFilesResponse,
    KnowledgeFileIdForm,
)


class OpenWebUIKnowledgeAPI:
    def __init__(self, url=OPEN_WEBUI_URL, token=OPEN_WEBUI_TOKEN):
        self.url = url or OPEN_WEBUI_URL
        self.token = token or OPEN_WEBUI_TOKEN
        self.base_url = f"{self.url}/api/v1/knowledge"
        self.headers_auth = {
            "Authorization": f"Bearer {self.token}",
        }
        self.headers = {
            **self.headers_auth,
            "Content-Type": "application/json"
        }

    def upload_file(
            self,
            file_path: str | Path,
            file_metadata: dict | None = None,
    ) -> Optional[str]:
        url = f'{self.url}/api/v1/files/'
        with open(file_path, 'rb') as f:
            # , data={'file_metadata': file_metadata}
            response = requests.post(url, headers=self.headers_auth, files={'file': f}, timeout=None)

        if response.status_code == 200:
            return response.json().get('id')
        else:
            print(f"Failed to upload: {file_path}. Status code: {response.status_code}")
            print(response.text)
            return None

    def get_knowledge_list(self) -> list[KnowledgeUserResponse]:
        url = f"{self.base_url}/list"
        response = requests.get(url, headers=self.headers)
        return [KnowledgeUserResponse(**_) for _ in response.json()]

    def create_new_knowledge(
            self,
            knowledge_data: KnowledgeForm,
    ) -> Optional[KnowledgeResponse]:
        url = f"{self.base_url}/create"
        response = requests.post(url, headers=self.headers, json=knowledge_data)
        return KnowledgeResponse(**response.json()) if response.status_code == 201 else None

    def get_knowledge_by_id(
            self,
            knowledge_id: str,
    ) -> Optional[KnowledgeFilesResponse]:
        url = f"{self.base_url}/{knowledge_id}"
        response = requests.get(url, headers=self.headers)
        return KnowledgeFilesResponse(**response.json()) if response.status_code == 200 else None

    def get_knowledge_by_name(
            self,
            knowledge_name: str,
    ) -> Optional[KnowledgeFilesResponse]:
        knowledges = self.get_knowledge_list()
        if knowledges:
            return next((_ for _ in knowledges
                         if _.name.lower() == knowledge_name.lower()), None)

        return None

    def update_knowledge_by_id(
            self,
            knowledge_id: str,
            knowledge_data: KnowledgeForm,
    ) -> Optional[KnowledgeFilesResponse]:
        url = f"{self.base_url}/{knowledge_id}/update"
        response = requests.put(url, headers=self.headers, json=knowledge_data)
        return KnowledgeFilesResponse(**response.json()) if response.status_code == 200 else None

    def add_file_to_knowledge_by_id(
            self,
            knowledge_id: str,
            file_id: str,
    ) -> Optional[KnowledgeFilesResponse]:
        url = f"{self.base_url}/{knowledge_id}/file/add"
        data = {"file_id": file_id}
        response = requests.post(url, headers=self.headers, json=data)
        return KnowledgeFilesResponse(**response.json()) if response.status_code == 200 else None

    def update_file_from_knowledge_by_id(
            self,
            knowledge_id: str,
            file_id: KnowledgeFileIdForm,
    ) -> Optional[KnowledgeFilesResponse]:
        url = f"{self.base_url}/{knowledge_id}/file/update"
        data = {"id": file_id}
        response = requests.post(url, headers=self.headers, json=data)
        return KnowledgeFilesResponse(**response.json()) if response.status_code == 200 else None

    def remove_file_from_knowledge_by_id(
            self,
            knowledge_id: str,
            file_id: KnowledgeFileIdForm,
    ) -> Optional[KnowledgeFilesResponse]:
        url = f"{self.base_url}/{knowledge_id}/file/remove"
        data = {"id": file_id}
        response = requests.post(url, headers=self.headers, json=data)
        return KnowledgeFilesResponse(**response.json()) if response.status_code == 200 else None

    def delete_knowledge_by_id(
            self,
            knowledge_id: str,
    ) -> bool:
        url = f"{self.base_url}/{knowledge_id}/delete"
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 200

    def reset_knowledge_by_id(
            self,
            knowledge_id: str,
    ) -> Optional[KnowledgeResponse]:
        url = f"{self.base_url}/{knowledge_id}/reset"
        response = requests.post(url, headers=self.headers)
        return KnowledgeResponse(**response.json()) if response.status_code == 200 else None


def __main():
    kn = OpenWebUIKnowledgeAPI()
    get_knowledge_list = kn.get_knowledge_list()
    pass


if __name__ == "__main__":
    __main()
