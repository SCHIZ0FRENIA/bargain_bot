import json
import os
import requests

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from bargain_bot import settings

TOKEN = settings.TELEGRAM_BOT_TOKEN
URL = settings.PUBLIC_URL
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'

def setwebhook():
  webhook_url_to_send = TELEGRAM_API_URL + "setWebhook?url=" + URL + "/getpost/"
  response = requests.post(webhook_url_to_send).json()
  return HttpResponse(f"{response}")

@csrf_exempt
def telegram_bot(request):
  if request.method == 'POST':
    update = json.loads(request.body.decode('utf-8'))
    handle_update(update)
    return HttpResponse('ok')
  else:
    return HttpResponseBadRequest('Bad Request')

def handle_update(update):
  chat_id = update['message']['chat']['id']
  text = update['message']['text']
  send_message("sendMessage", {
    'chat_id': chat_id,
    'text': f'you said {text}'
  })

def send_message(method, data):
  return requests.post(TELEGRAM_API_URL + method, data)
