from handlers.new_sub_handler import new_subscription_start, get_sub_name, get_category, get_query, get_price_min, \
    get_price_max, get_condition, confirm_subscription, cancel_conversation
from telegram.ext import ConversationHandler, filters, MessageHandler
from utils.constants import NEW_SUB, CANCEL, CONFIRM, NEW_SUB_CATEGORY_STATE, NEW_SUB_QUERY_STATE, \
    NEW_SUB_PRICE_MIN_STATE, NEW_SUB_PRICE_MAX_STATE, NEW_SUB_CONDITION_STATE, RENT_APARTMENT, \
    BUY_APARTMENT, GOODS, NEW_SUB_NAME_STATE, NEW_SUB_CONFIRM_STATE


def get_new_sub_conversation():
    return ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^' + NEW_SUB + '$'), new_subscription_start)
        ],
        states={
            NEW_SUB_NAME_STATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex(CANCEL), get_sub_name)],
            NEW_SUB_CATEGORY_STATE: [
                MessageHandler(filters.Regex(f'^({RENT_APARTMENT}|{BUY_APARTMENT}|{GOODS})$'), get_category)],
            NEW_SUB_QUERY_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex(CANCEL), get_query)],
            NEW_SUB_PRICE_MIN_STATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex(CANCEL), get_price_min)],
            NEW_SUB_PRICE_MAX_STATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex(CANCEL), get_price_max)],
            NEW_SUB_CONDITION_STATE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex(CANCEL), get_condition)],
            NEW_SUB_CONFIRM_STATE: [MessageHandler(filters.Regex(f'^({CONFIRM}|{CANCEL})$'), confirm_subscription)],
        },
        fallbacks=[MessageHandler(filters.Regex(f'^{CANCEL}$'), cancel_conversation)],
    )
