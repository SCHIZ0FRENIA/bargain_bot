import os
import signal
import sys

from django.apps import AppConfig
from pyngrok import ngrok, conf
from pyngrok.exception import PyngrokNgrokError

from bargain_bot import settings

def shutdown_ngrok(signum, frame):
    print('/nShutting down ngrok')
    ngrok.kill()
    print('Ngrok shut down')
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
                    print('Starting NGROK:')
                    port = settings.NGROK_PORT
                    tunnel = ngrok.connect(port, 'http')
                    public_url = tunnel.public_url
                    settings.PUBLIC_URL = public_url
                    print(f'Public URL: {public_url}')

                    from telegram_bot import views
                    views.setwebhook()

                    signal.signal(signal.SIGTRAP, shutdown_ngrok)
                except PyngrokNgrokError as e:
                    print(f'Ngrok error: {e.ngrok_error}')
        else:
            if not hasattr(settings, 'PUBLIC_URL'):
                settings.PUBLIC_URL = None
