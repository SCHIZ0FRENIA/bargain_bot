from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils.constants import NEW_SUB, MY_SUBS, CHANGE_SUB, REMOVE_SUB


def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton(NEW_SUB), KeyboardButton(MY_SUBS)],
        [KeyboardButton(CHANGE_SUB), KeyboardButton(REMOVE_SUB)],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)