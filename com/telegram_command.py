# telegram_command.py by.KimSeongUk A.K.A.pangin as student @DonggukUniv.GyeongJu

# Library
import telegram
import logging

# Module
from lib import db_handler, system_handler

# Set logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# init Firestore
db = db_handler.set_db()


def send_noti(update, context, user_code, content):
    bot = telegram.Bot(token="")
    bot.sendMessage(chat_id=user_code, text=content)


# Function
def greeting(update, context):
    update.message.reply_text("안녕하세요? {}님.\n대학을 지정하면 새로운 공지가 나타날 때 알림을 드릴게요!\n사용법이 궁금하시다면, /help 명령어를 사용해보세요.".format(
        update.message.from_user.first_name))


def sign_up(update, context):
    result = db_handler.add_user(db, update.message.from_user.id)
    if result is True:
        update.message.reply_text("니가 알아봐에 등록되었습니다! 이제 대학과 키워드를 등록해주시면 원하시는 공지사항을 빠르게 보실 수 있어요!")
    elif result is False:
        update.message.reply_text("이미 니가 알아봐에 등록되었습니다! 공지 알림이 오지 않는다면 재학 중이신 대학과 키워드를 등록해주세요!")
    else:
        update.message.reply_text("시스템에 문제가 생겼습니다. 빠르게 고칠게요!")


def delete_me(update, context):
    logger.info("User {} trying to delete account.".format(update.message.from_user.id))
    result = db_handler.del_user(db, update.message.from_user.id)
    if result is True:
        logger.info("User {} deleted from system.".format(update.message.from_user.id))
        update.message.reply_text("니가 알아봐를 이용해주셔서 감사합니다! 다시 등록하시려면 /signup 명령어를 사용해주세요!")
    elif result is False:
        logger.error("User {} is not registered on system.".format(update.message.from_user.id))
        update.message.reply_text(
            "{}님을 니가 알아봐 찾을 수 없어요. /signup 을 사용해서 {}님을 등록해주세요!".format(update.message.from_user.first_name,
                                                                       update.message.from_user.first_name))
    else:
        logger.critical("".format())
        update.message.reply_text("시스템에 문제가 생겼습니다. 빠르게 고칠게요!")


def set_univ_inline_keyboard(update, context):
    logger.info("Trying to set univ")
    univ_keyboard = [[telegram.InlineKeyboardButton("동국대학교 경주캠퍼스", callback_data='동국대학교 경주캠퍼스'),
                      telegram.InlineKeyboardButton("동국대학교 서울캠퍼스", callback_data='동국대학교 서울캠퍼스'),
                      telegram.InlineKeyboardButton("한양대학교", callback_data='한양대학교'),
                      telegram.InlineKeyboardButton("경기대학교", callback_data='경기대학교')]]
    update.message.reply_text("키워드 알림을 받으실 대학교를 선택해주세요!", reply_markup=telegram.InlineKeyboardMarkup(univ_keyboard))


def set_univ_callback_query(update, context):
    logger.info("User {} selected {}".format(update.callback_query.from_user.id, update.callback_query.data))
    update.callback_query.answer()
    update.callback_query.edit_message_text(text="{}로 등록할게요!".format(update.callback_query.data))
    user_state = db_handler.set_univ(db, update.callback_query.from_user.id, update.callback_query.data)
    if user_state is False:
        logger.error("User {} is not registered on system.".format(update.callback_query.from_user.id))
        update.message.reply_text(
            "{}님을 니가 알아봐 찾을 수 없어요. /signup 을 사용해서 {}님을 등록해주세요!".format(update.message.from_user.first_name,
                                                                       update.message.from_user.first_name))
    elif user_state is True:
        logger.info("User {} registered to {}".format(update.callback_query.from_user.id, update.callback_query.data))
        update.callback_query.message.reply_text("{}로 등록되었습니다!".format(update.callback_query.data))
    else:
        logger.critical("id: {}, data: {}, result: {}".format(update.callback_query.from_user.id, update.callback_query.data, user_state))
        update.callback_query.message.reply_text("시스템에 문제가 생겼습니다. 빠르게 고칠게요!")


def show_keyword(update, context):
    logger.info("User {} trying to see keyword list.".format(update.message.from_user.id))
    result = db_handler.show_keyword(db, update.message.from_user.id)
    if result is None:
        logger.error("No keyword for user {}".format(update.message.from_user.id))
        update.message.reply_text("등록하신 키워드가 없네요. /setkw 명령어 뒤에 같이 키워드를 입력하시면 키워드를 등록할 수 있어요! 예) /setkw 코로나")
    elif result is True:
        logger.info("User {}, keyword {}".format(update.message.from_user.id, result))
        update.message.reply_text("{}님의 키워드 목록입니다.\n{}".format(update.message.from_user.first_name, result))
    elif result is False:
        logger.critical("id: {}, keyword {}".format(update, result))
        update.message.reply_text("시스템에 문제가 생겼습니다. 빠르게 고칠게요!")
    else:
        logger.critical("id: {}, keyword {}".format(update, result))
        update.message.reply_text("시스템에 문제가 생겼습니다. 빠르게 고칠게요!")


def set_keyword(update, context):
    logger.info("User {} trying to set keyword.".format(update.message.from_user.id))
    for keyword in context.args:
        db_handler.set_keyword(db, update.message.from_user.id, keyword)
    update.message.reply_text("키워드가 등록되었습니다. 관련 알림이 오면 연락드릴게요!")


def delete_keyword_inline_keyboard(update, context):
    logger.info("Trying to set univ")
    keyword_keyboard = [[telegram.InlineKeyboardButton("동국대학교 경주캠퍼스", callback_data='동국대학교 경주캠퍼스'),
                         telegram.InlineKeyboardButton("동국대학교 서울캠퍼스", callback_data='동국대학교 서울캠퍼스'),
                         telegram.InlineKeyboardButton("한양대학교", callback_data='한양대학교')]]
    update.message.reply_text("삭제할 키워드를 선택해주세요!", reply_markup=telegram.InlineKeyboardMarkup(keyword_keyboard))


def delete_keyword_callback_query(update, context):
    logger.info("User {} selected {}".format(update.callback_query.from_user.id, update.callback_query.data))
    update.callback_query.answer()
    update.callback_query.edit_message_text(text="삭제할게요!".format(update.callback_query.data))
    result = db_handler.del_keyword(db, update.message.from_user.id, update.callback_query.data)
    if result is True:
        update.message.reply_text("키워드가 삭제되었습니다!")
    elif result is False:
        update.message.reply_text("키워드가 없어서 삭제하지 않았어요!")
    else:
        update.message.reply_text("시스템에 문제가 생겼습니다. 빠르게 해결할게요!")


def com_help(update, context):
    logger.info("User {} called help command.".format(update.message.from_user.id))
    update.message.reply_text(
        "도움을 요청하셨군요?\n아래는 현재 지원되는 명령들입니다.\n/signup : 사용자 등록을 할 때 사용해요.\n/delme : 사용자 등록을 해할 때 사용해요.\n/showkw : 현재 등록된 키워드들을 보여줘요.\n/setkw : 키워드를 등록해줘요.\n/delkw : 키워드를 삭제해줘요.\n/setuniv : 대학을 등록해줘요.\n도움이 되셨나요? 새로운 아이디어나 기능을 제안하시려면 개발자 이메일로 부담없이 연락해주세요!")





db_handler.watch_collection_dongguk_univ_gyeongju(db)
# db_handler.watch_collection_dongguk_univ_seoul(db)
# db_handler.watch_collection_hanyang_univ(db)
# db_handler.watch_collection_gyeonggui_univ(db)
