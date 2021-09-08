# telegram_bot_handler.py by.KimSeongUk A.K.A.pangin as student @DonggukUniv.GyeongJu

# Library
from telegram.ext import *
import logging

# Module
from com import telegram_command

# Set logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def add_command_handlers(updater):
    updater.dispatcher.add_handler(CommandHandler("start", telegram_command.greeting))
    updater.dispatcher.add_handler(CommandHandler("help", telegram_command.com_help))
    updater.dispatcher.add_handler(CommandHandler("signup", telegram_command.sign_up))
    updater.dispatcher.add_handler(CommandHandler("delme", telegram_command.delete_me))
    updater.dispatcher.add_handler(CommandHandler("setuniv", telegram_command.set_univ_inline_keyboard))
    updater.dispatcher.add_handler(CommandHandler("showkw", telegram_command.show_keyword))
    updater.dispatcher.add_handler(CommandHandler("setkw", telegram_command.set_keyword, pass_args=True))
    updater.dispatcher.add_handler(CommandHandler("delkw", telegram_command.delete_keyword_inline_keyboard, pass_user_data=True))


def add_callback_query_handlers(updater):
    updater.dispatcher.add_handler(CallbackQueryHandler(telegram_command.set_univ_callback_query))
    updater.dispatcher.add_handler(CallbackQueryHandler(telegram_command.delete_keyword_callback_query))


def set_updater(bot_token):
    updater = Updater(bot_token, use_context=True)
    add_command_handlers(updater)
    add_callback_query_handlers(updater)
    updater.start_polling()
    updater.idle()


def send_noti(user_code, content):
    telegram_command.send_noti(user_code=user_code, content=content)
