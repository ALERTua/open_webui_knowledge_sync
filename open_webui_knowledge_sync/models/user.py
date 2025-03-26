"""open_webui_knowledge_sync/models/user.py"""

from pydantic import BaseModel


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    role: str
    profile_image_url: str
