#!/usr/bin/env python3

# system_hander.py by.Pangin A.K.A Kim Seong Uk @ NICC corp. as intern

# Library
import sys
import os.path
from datetime import datetime
import logging
import signal


# Set logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)


def is_system_argument_enough(less_argument, more_argument):
    if more_argument < len(sys.argv) or len(sys.argv) < less_argument:
        return False
        logger.critical("Less or too much argument!")
    else:
        return True


def is_telegram_argument_enough(less_argument, more_argument, telegram_args):
    if more_argument < len(telegram_args) or len(telegram_args) < less_argument:
        return False
        logger.critical("Less or too much argument!")
    else:
        return True


def get_argument(argument_num):
    argument = sys.argv[argument_num]
    logger.debug("{} loaded from system argument.".format(argument))
    return argument


def is_file_exist(file_name):
    file_exist = os.path.isfile(file_name)
    logger.debug("{} is exist? {}".format(file_name, file_exist))
    return


def make_up():
    logger.info("Server Terminated!")
    exit()


def signal_handler(sig, frame):
    logger.info("Ctrl+C Keyboard Interrupt Detected!")
    make_up()


def get_time():
    return datetime.now().strftime("%Y%m%d")
