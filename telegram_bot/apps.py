import logging
import os
import signal
import sys

from django.apps import AppConfig
from pyngrok import ngrok, conf
from pyngrok.exception import PyngrokNgrokError

from bargain_bot import settings

logger = logging.getLogger('telegram_bot')

def shutdown_ngrok(signum, frame):
    logger.info('Shutting down ngrok...')
    ngrok.kill()
    logger.info('Ngrok shut down.')
    sys.exit(0)


class TelegramBotConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telegram_bot'
    verbose_name = 'Telegram Bot'

    def ready(self):
        if os.getenv('RUN_MAIN') == 'true':
            if settings.USE_NGROK:
                ngrok.kill()
                try:
                    logger.info('Starting NGROK:')
                    port = settings.NGROK_PORT
                    tunnel = ngrok.connect(port, 'http')
                    public_url = tunnel.public_url
                    settings.PUBLIC_URL = public_url
                    logger.info(f'Public URL: {public_url}')

                    from telegram_bot import views
                    views.setwebhook()

                    signal.signal(signal.SIGTRAP, shutdown_ngrok)
                except PyngrokNgrokError as e:
                    logger.error(f'Ngrok error: {e.ngrok_error}')
        else:
            if not hasattr(settings, 'PUBLIC_URL'):
                settings.PUBLIC_URL = None
