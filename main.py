# main.py by.KimSeongUk A.K.A.pangin as student @DonggukUniv.GyeongJu

# Library
from datetime import datetime
import logging

# Module
from lib import telegram_bot_handler
from com import telegram_command

# Variables
log_file_name: str = "log/{}.log".format(datetime.now())

# Token
bot_api_token = ""

# Set logger
logging.basicConfig(filename=log_file_name, level=logging.DEBUG)
logger = logging.getLogger(__name__)
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)

telegram_bot_handler.set_updater(bot_api_token)
telegram_command.set_bot(bot_api_token)