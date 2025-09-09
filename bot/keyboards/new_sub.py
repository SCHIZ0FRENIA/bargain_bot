from telegram import KeyboardButton, ReplyKeyboardMarkup
from utils.constants import RENT_APARTMENT, BUY_APARTMENT, GOODS, CANCEL, CONFIRM, USED, NEW, ANY


def get_category_keyboard():
    keyboard = [
        [KeyboardButton(RENT_APARTMENT), KeyboardButton(BUY_APARTMENT)],
        [KeyboardButton(GOODS)],
        [KeyboardButton(CANCEL)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_confirm_keyboard():
    keyboard = [
        [KeyboardButton(CONFIRM)],
        [KeyboardButton(CANCEL)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_cancel_keyboard():
    keyboard = [
        [KeyboardButton(CANCEL)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_condition_keyboard():
    keyboard = [
        [KeyboardButton(USED) , KeyboardButton(NEW)],
        [KeyboardButton(ANY)],
        [KeyboardButton(CANCEL)]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
