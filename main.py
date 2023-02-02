import logging
import telegram
from telegram import ChatAction, Bot, ChatMember
from telegram.ext import Updater, CommandHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def start(update, context):
    update.message.reply_text("Hi! I'm a bot that can help you remove dead members from your Telegram community. Use /remove to start removing.")

def help(update, context):
    update.message.reply_text("I can remove dead members from your Telegram community. Try using /remove to start removing.")

def remove(update, context):
    bot = context.bot
    chat_id = update.message.chat.id
    members = bot.get_chat_administrators(chat_id)
    dead_members = []
    for member in members:
        user_id = member.user.id
        try:
            bot.get_chat_member(chat_id, user_id)
        except telegram.TelegramError:
            dead_members.append(user_id)
    for dead_member in dead_members:
        bot.kick_chat_member(chat_id, dead_member)
    update.message.reply_text("Removed {} dead members from the community.".format(len(dead_members)))

def error(update, context):
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5648103386:AAGb2tlYazkxTI3OVJp5khtTFOq6DVWL8eU", use_context=True)

    dp = updater.dispatcher

    # Add command handler to start and help commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("remove", remove))

    # Add error handler
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
