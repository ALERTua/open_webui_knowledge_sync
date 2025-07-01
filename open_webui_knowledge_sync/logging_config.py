"""open_webui_knowledge_sync/logging_config.py"""

import logging


def setup_logging():
    # Configure the root logger
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s[%(lineno)d] - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )
