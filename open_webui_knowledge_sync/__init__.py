"""open_webui_knowledge_sync/__init__.py"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.absolute()))

from open_webui_knowledge_sync.entrypoints.sync import app
