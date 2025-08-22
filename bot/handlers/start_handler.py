from telegram import Update
from telegram.ext import ContextTypes

from keyboards.main_menu import get_main_menu_keyboard


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello form bargain bot!",
        reply_markup=get_main_menu_keyboard(),
    )
