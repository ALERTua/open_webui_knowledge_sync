"""open_webui_knowledge_sync/models/knowledge.py"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from open_webui_knowledge_sync.models.user import UserResponse  # noqa: TC001
from open_webui_knowledge_sync.models.files import FileMetadataResponse, FileModel  # noqa: TC001


class KnowledgeFileIdForm(BaseModel):
    file_id: str


class KnowledgeModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str

    name: str
    description: str

    data: dict | None = None
    meta: dict | None = None

    access_control: dict | None = None

    created_at: int  # timestamp in epoch
    updated_at: int  # timestamp in epoch


class KnowledgeResponse(KnowledgeModel):
    files: list[FileMetadataResponse | dict] | None = None


class KnowledgeFilesResponse(KnowledgeResponse):
    files: list[FileModel]


class KnowledgeUserModel(KnowledgeModel):
    user: UserResponse | None = None


class KnowledgeResponse(KnowledgeModel):
    files: list[FileMetadataResponse | dict] | None = None


class KnowledgeUserResponse(KnowledgeUserModel):
    files: list[FileMetadataResponse | dict] | None = None


class KnowledgeForm(BaseModel):
    name: str
    description: str
    data: dict | None = None
    access_control: dict | None = None
