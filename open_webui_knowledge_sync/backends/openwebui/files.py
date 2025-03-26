from __future__ import annotations

from pathlib import Path
from typing import Optional

import requests

from open_webui_knowledge_sync.env import OPEN_WEBUI_URL, OPEN_WEBUI_TOKEN
from open_webui_knowledge_sync.models.files import FileModelResponse


class OpenWebUIFilesAPI:
    def __init__(self, url=OPEN_WEBUI_URL, token=OPEN_WEBUI_TOKEN):
        self.url = url or OPEN_WEBUI_URL
        self.token = token or OPEN_WEBUI_TOKEN
        self.base_url = f"{self.url}/api/v1/files"
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
        url = f'{self.base_url}/'
        with open(file_path, 'rb') as f:
            # , data={'file_metadata': file_metadata}
            response = requests.post(url, headers=self.headers_auth, files={'file': f}, timeout=None)

        if response.status_code == 200:
            return response.json().get('id')
        else:
            print(f"Failed to upload: {file_path}. Status code: {response.status_code}")
            print(response.text)
            return None

    def list_files(self) -> list[FileModelResponse]:
        url = f"{self.base_url}/"
        response = requests.get(url, headers=self.headers)
        return [FileModelResponse(**_) for _ in response.json()]

    def delete_file_by_id(
            self,
            file_id: str,
    ) -> bool:
        url = f"{self.base_url}/{file_id}"
        response = requests.delete(url, headers=self.headers)
        return response.status_code == 200

    def get_file_by_id(
            self,
            file_id: str,
    ) -> Optional[FileModelResponse]:
        url = f"{self.base_url}/{file_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()

        return None

    def cleanup(self):
        files = self.list_files()
        for f in files:
            collection_name = getattr(f.meta, 'collection_name', '')
            if collection_name and collection_name.startswith('file-'):
                self.delete_file_by_id(f.id)


def __main():
    api = OpenWebUIFilesAPI()
    _files = api.cleanup()
    pass


if __name__ == "__main__":
    __main()
