from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

from keyboards.main_menu import get_main_menu_keyboard
from utils.constants import NEW_SUB_NAME_STATE


async def new_subscription_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Name your subscription.'
    )
    return NEW_SUB_NAME_STATE


async def get_sub_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subscription_name = update.message.text
    context.user_data['new_sub_name'] = subscription_name

    await update.message.reply_text(
        f'Subscription name is {subscription_name}.'
    )

    await on_end_of_conversation(update, context)

    return ConversationHandler.END

async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Action cancelled. Returning to the main menu.'
    )

    await on_end_of_conversation(update, context)

    return ConversationHandler.END

async def on_end_of_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'DO you want to do anything else?',
        reply_markup=get_main_menu_keyboard(),
    )