import logging

from settings import IS_DEBUG

logging.basicConfig(
    level=logging.DEBUG if IS_DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('bot_serv')