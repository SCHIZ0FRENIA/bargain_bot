from handlers.new_sub_handler import cancel_conversation, new_subscription_start, get_sub_name
from telegram.ext import ConversationHandler, filters, MessageHandler, CommandHandler
from utils.constants import NEW_SUB, NEW_SUB_NAME_STATE, CANCEL_ID


def get_new_sub_conversation():
    return ConversationHandler(
        entry_points=[
            MessageHandler(filters.Regex('^' + NEW_SUB + '$'), new_subscription_start)
        ],

        states={
            NEW_SUB_NAME_STATE: [
                MessageHandler((filters.TEXT | filters.Regex('^' + CANCEL_ID + '$')) & ~filters.COMMAND, get_sub_name)
            ],
        },

        fallbacks=[CommandHandler(CANCEL_ID, cancel_conversation)]
    )
