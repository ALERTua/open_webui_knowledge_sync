"""open_webui_knowledge_sync/env.py"""

import os

from dotenv import load_dotenv

load_dotenv()

OPEN_WEBUI_URL = os.getenv("OPEN_WEBUI_URL", "http://localhost:8080")
OPEN_WEBUI_TOKEN = os.getenv("OPEN_WEBUI_TOKEN", "")
