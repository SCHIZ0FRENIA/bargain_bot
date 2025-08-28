import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

from conversations.new_sub_conversation import get_new_sub_conversation
from handlers.plain_text_handler import handle_text
from handlers.start_handler import start

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')


def main() -> None:
    application = (Application
                   .builder()
                   .token(TOKEN)
                   .read_timeout(30)
                   .connect_timeout(30)
                   .build())

    # conversations
    application.add_handler(get_new_sub_conversation())

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
