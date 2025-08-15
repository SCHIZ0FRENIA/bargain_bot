import json
import logging
import requests

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from bargain_bot import settings
from telegram_bot.enums import StartMenuIds, NewSubIds

logger = logging.getLogger()
TOKEN = settings.TELEGRAM_BOT_TOKEN
URL = settings.PUBLIC_URL
TELEGRAM_API_URL = f'https://api.telegram.org/bot{TOKEN}/'

last_menu = -1

def setwebhook():
    webhook_url_to_send = TELEGRAM_API_URL + 'setWebhook?url=' + URL + '/getpost/'
    response = requests.post(webhook_url_to_send).json()
    return HttpResponse(f'{response}')

@csrf_exempt
def telegram_bot(request):
    if request.method == 'POST':
        try:
            update_data = json.loads(request.body.decode('utf-8'))
            update = Update.de_json(update_data)
            logger.debug(f'Received Telegram update: {update_data}')
            handle_update(update)
            return HttpResponse('ok')

        except json.JSONDecodeError as e:
            logger.error(f'Error decoding JSON from Telegram update: {e}', exc_info=True)
            return HttpResponseBadRequest('Invalid JSON')

        except Exception as e:
            logger.error(f'An unexpected error occurred processing Telegram update: {e}', exc_info=True)
            return HttpResponseBadRequest('Internal Server Error')
    else:
        return HttpResponseBadRequest('Bad Request')

def handle_update(update):
    if update.message:
        message = update.message

        if message.chat_id and message.text:
            logger.info(f'Received message from {message.chat_id} text: {message.text}')
            if message.text == '/start':
                logger.info(f'Handling start.')
                send_start_menu(message.chat_id)
            else:
                send_message('sendMessage', {
                    'chat_id': message.chat_id,
                    'text': f'You said {message.text}'
                })
                logger.info(f'Sent echo message to {message.chat_id}')
        else:
            logger.warning(f'Received incorrect message: {update}')
    elif update.callback_query:
        query = update.callback_query
        chat_id = query.message.chat_id
        callback_data = query.data
        logger.info(f'Received callback query from {chat_id}, data: {callback_data}')

        send_message('answerCallbackQuery', {
            'callback_query_id': query.id,
            'text': f'You pressed: {callback_data}'
        })

        if callback_data == StartMenuIds.NEW_SUBSCRIPTION.value:
            send_new_sub_menu(chat_id)
        elif callback_data == StartMenuIds.LIST_SUBSCRIPTIONS.value:
            send_message('sendMessage', {
                'chat_id': chat_id,
                'text': 'You chose to list your subscription',
            })
        elif callback_data == StartMenuIds.EDIT_SUBSCRIPTION.value:
            send_message('sendMessage', {
                'chat_id': chat_id,
                'text': 'You chose to edit subscription',
            })
        else:
            send_message('sendMessage', {
                'chat_id': chat_id,
                'text': 'Invalid callback data.'
            })

def send_message(method, data):
    return requests.post(TELEGRAM_API_URL + method, data)

def send_start_menu(chat_id: int):
    keyboard = [
        [
            InlineKeyboardButton('New Subscription', callback_data = StartMenuIds.NEW_SUBSCRIPTION.value),
        ],
        [
            InlineKeyboardButton('My Subscriptions', callback_data = StartMenuIds.LIST_SUBSCRIPTIONS.value),
        ],
        [
            InlineKeyboardButton('Change Subscription', callback_data = StartMenuIds.EDIT_SUBSCRIPTION.value),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard).to_json()
    message_text = 'Welcome to Bargain Bot! Please choose an option:'

    send_message('sendMessage', {
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': reply_markup,
    })
    logger.info(f'Sent /start menu to chat_id {chat_id}.')

def send_new_sub_menu(chat_id: int):
    keyboard = [
        [
            InlineKeyboardButton('Rent apartment', callback_data = NewSubIds.RENT_APARTMENT.value),
        ],
        [
            InlineKeyboardButton('Buy apartment', callback_data=NewSubIds.BUY_APARTMENT.value),
            InlineKeyboardButton('Goods', callback_data=NewSubIds.GOODS.value),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard).to_json()
    message_text = 'Choose the category for subscription:'

    send_message('sendMessage',{
        'chat_id': chat_id,
        'text': message_text,
        'reply_markup': reply_markup,
    })

    logger.info(f'Sent new subscription menu to chat_id {chat_id}.')