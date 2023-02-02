import logging
import os
import telegram
from telegram.error import BadRequest
from telegram.ext import Updater, CommandHandler, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the remove_deleted_accounts function
def remove_deleted_accounts(update: Update, context: CallbackContext):
    group = update.message.chat
    members = context.bot.get_chat_administrators(chat_id=group.id)

    for member in members:
        user = member.user
        try:
            context.bot.get_chat_member(chat_id=group.id, user_id=user.id)
        except BadRequest as e:
            if e.message == "User not found":
                context.bot.kick_chat_member(chat_id=group.id, user_id=user.id)

def cancel(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.message.chat_id, text="Cancelling command...")

# Define the main function
def main():
    # Get the API key from the environment
    API_KEY = os.environ.get("5648103386:AAGb2tlYazkxTI3OVJp5khtTFOq6DVWL8eU", None)
    if API_KEY is None:
        print("The TELEGRAM_BOT_API_KEY environment variable is not set")
        return

    # Set up the updater and dispatcher
    updater = Updater(token=API_KEY, use_context=True)
    dp = updater.dispatcher

    # Add the command handler for the remove_deleted_accounts command
    dp.add_handler(CommandHandler("remove_deleted_accounts", remove_deleted_accounts))
    dp.add_handler(CommandHandler("cancel", cancel))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
