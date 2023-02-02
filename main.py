import logging
from telegram import Bot
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Define the bot's token
TOKEN = "your_token_here"

# Define the function that will be called every time the bot receives a message
def delete_deleted_accounts(update: Update, context: CallbackContext):
    group = update.message.chat
    members = context.bot.get_chat_members_count(chat_id=group.id)
    for i in range(members):
        user = context.bot.get_chat_member(chat_id=group.id, user_id=i)
        if user.user.is_deleted:
            context.bot.kick_chat_member(chat_id=group.id, user_id=i)

def main():
    # Create the Updater object
    updater = Updater(token=TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add a handler for the message
    dp.add_handler(MessageHandler(Filters.all, delete_deleted_accounts))

    # Start the bot
    updater.start_polling()

    # Run the bot until it receives a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
