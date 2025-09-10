import logging

from keyboards.main_menu import get_main_menu_keyboard
from keyboards.new_sub import get_category_keyboard, get_confirm_keyboard, get_cancel_keyboard, get_condition_keyboard
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from utils.constants import NEW_SUB_CONDITION_STATE, RENT_APARTMENT, BUY_APARTMENT, GOODS, NEW_SUB_PRICE_MIN_STATE, \
    CONFIRM, NEW_SUB_PRICE_MAX_STATE, NEW_SUB_NAME_STATE, NEW_SUB_CATEGORY_STATE, NEW_SUB_QUERY_STATE, \
    NEW_SUB_CONFIRM_STATE
from utils.logging import logger


async def new_subscription_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Name your subscription.', reply_markup=get_cancel_keyboard())
    return NEW_SUB_NAME_STATE


async def get_sub_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    subscription_name = update.message.text
    context.user_data['new_sub'] = {'name': subscription_name}
    await update.message.reply_text(
        f'Subscription name is "{subscription_name}".\n\nNow, please choose a category:',
        reply_markup=get_category_keyboard()
    )
    return NEW_SUB_CATEGORY_STATE


async def get_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    category = update.message.text
    if category not in [RENT_APARTMENT, BUY_APARTMENT, GOODS]:
        await update.message.reply_text("Please choose a valid category from the keyboard.")
        return NEW_SUB_CATEGORY_STATE
    context.user_data['new_sub']['category'] = category
    await update.message.reply_text(
        f'Category selected: "{category}".\n\nWhat are you looking for? Please enter your search query:',
        reply_markup=get_cancel_keyboard()
    )
    return NEW_SUB_QUERY_STATE


async def get_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    context.user_data['new_sub']['query'] = query
    await update.message.reply_text(
        f'Search query is "{query}".\n\nWhat is the minimum price?',
        reply_markup=get_cancel_keyboard()
    )
    return NEW_SUB_PRICE_MIN_STATE


async def get_price_min(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price_min = update.message.text
    try:
        context.user_data['new_sub']['price_min'] = float(price_min)
        await update.message.reply_text('What is the maximum price?', reply_markup=get_cancel_keyboard())
        return NEW_SUB_PRICE_MAX_STATE
    except ValueError:
        await update.message.reply_text('Invalid price. Please enter a number.')
        return NEW_SUB_PRICE_MIN_STATE


async def get_price_max(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price_max = update.message.text
    try:
        context.user_data['new_sub']['price_max'] = float(price_max)
        await update.message.reply_text(
            f'Price range is {context.user_data["new_sub"]["price_min"]} to {price_max}.\n\nWhat is the condition of the item?',
            reply_markup=get_condition_keyboard()
        )
        return NEW_SUB_CONDITION_STATE
    except ValueError:
        await update.message.reply_text('Invalid price. Please eccnter a number.')
        return NEW_SUB_PRICE_MAX_STATE


async def get_condition(update: Update, context: ContextTypes.DEFAULT_TYPE):
    condition = update.message.text
    context.user_data['new_sub']['condition'] = condition
    subscription_data = context.user_data['new_sub']
    summary = (
        f"Please confirm your new subscription details:\n\n"
        f"Name: {subscription_data['name']}\n"
        f"Category: {subscription_data['category']}\n"
        f"Query: {subscription_data['query']}\n"
        f"Price Range: {subscription_data['price_min']} to {subscription_data['price_max']}\n"
        f"Condition: {subscription_data['condition']}"
    )
    await update.message.reply_text(summary, reply_markup=get_confirm_keyboard())
    return NEW_SUB_CONFIRM_STATE


async def confirm_subscription(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == CONFIRM:
        subscription_data = context.user_data.get('new_sub', {})
        logger.debug('ASDFASDFASDF')
        logger.debug(subscription_data)

    await update.message.reply_text(
        'What do you want to do next?.',
        reply_markup=get_main_menu_keyboard()
    )
    return ConversationHandler.END


async def cancel_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        'Action cancelled. Returning to the main menu.',
        reply_markup=get_main_menu_keyboard()
    )
    return ConversationHandler.END
