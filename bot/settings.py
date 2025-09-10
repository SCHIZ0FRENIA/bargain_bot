import os

from dotenv import load_dotenv

load_dotenv()

IS_DEBUG = os.getenv('IS_DEBUG')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')