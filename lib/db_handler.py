# db_handler.py by.KimSeongUk A.K.A.pangin as student @DonggukUniv.GyeongJu

# Library
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import logging

# Module
from lib import telegram_bot_handler

# Set logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.DEBUG)

# Flages
dongguk_univ_gyeongju_init = False
dounguk_univ_seoul_init = False
hanyang_univ_init = False
kyeonggui_univ_init = False


# Firestore init Function
def set_db():
    cred = credentials.Certificate('cred/kpj-nial-firebase-adminsdk-q167i-c1490df415.json')
    firebase_admin.initialize_app(cred)
    return firestore.client()


# Firestore db Function
def new_noti(db, univ_code: str, url_key: str, writer: str, noti_title: str, url: str, date: str, content: str):
    doc_ref = db.collection(univ_code).document(url_key)
    doc_ref.set({
        "title": noti_title,
        "univ_code": univ_code,
        "writer": writer,
        "date": date,
        "url": url,
        "contents": content,
        "url_key": url_key
    })


def check_noti(db, univ_code: str, url_key: str):
    logger.info("check noti in {} {} exist".format(univ_code, url_key))
    doc = db.collection(univ_code).document(url_key).get()
    doc = doc.to_dict()
    if doc is None:
        logger.info("noti in {} {} not exist.".format(univ_code, url_key))
        return False
    elif doc is not None:
        logger.info("noti in {} {} is exist".format(univ_code, url_key))
        return True
    else:
        logger.critical("db: {}, univ_code: {}, url: {}".format(db, univ_code, url_key))


def count_noti(db, univ_code: str):
    counter = 1
    logger.info("count noties in {}".format(univ_code))
    docs = db.collection(univ_code).where(u'univ_code', u'==', "동국대학교 경주캠퍼스").stream()
    for doc in docs:
        counter = counter + 1
    return counter


# telegram command related Function
def add_user(db, user_code: int):
    doc_ref = db.collection(u"users").document(str(user_code))
    doc = doc_ref.get()
    doc = doc.to_dict()
    if doc is None:
        doc_ref.set({
            "user_code": user_code
        })
        logger.info("Registerd user {}".format(user_code))
        return True
    elif doc is not None:
        logger.error("User {} is Already Registered.".format(user_code))
        return False
    else:
        logger.critical("user_code: {}, doc: {}".format(user_code, doc))


def check_user(db, user_code: int):
    logger.info("User {} trying to get user info.".format(user_code))
    doc = get_user(db, user_code)
    logger.info("check_user {}".format(doc))
    if doc is None:
        logger.error("User {} is Already Registered.".format(user_code))
        return True
    elif doc is not None:
        logger.error("User {} not Registered.".format(user_code))
        return False
    else:
        logger.critical("user_code: {}, doc: {}".format(user_code, doc))


def get_user(db, user: int or str):
    logger.info("Trying to get user info.")
    if user is int:
        logger.info("Got user code {}".format(user))
        doc_ref = db.collection(u"users").document(str(user))
        doc = doc_ref.get()
        return doc.to_dict()
    elif user is str:
        logger.info("Got user doc ref {}".format(user))
        doc = user.get
        return doc.to_dict()
    else:
        logger.critical("db: {}, user code or doc ref: {}".format(db, user))


def del_user(db, user_code: int):
    logger.info("User {} trying to delete user.".format(user_code))
    doc_ref = db.collection(u"users").document(str(user_code))
    doc = doc_ref.get()
    doc = doc.to_dict()
    if doc is None:
        logger.error("User {} is not in system.".format(user_code))
        return False
    elif doc is not None:
        doc_ref.delete()
        logger.info("User {} had been deleted.".format(user_code))
        return True
    else:
        logger.critical("db: {}, user_code: {}, doc: {}".format(db, user_code, doc))


def set_univ(db, user_code: int, univ_code: str):
    logger.info("Trying to set {} to {}".format(univ_code, user_code))
    doc_ref = db.collection(u"users").document(str(user_code))
    doc = doc_ref.get()
    doc = doc.to_dict()
    user_state = check_user(db, user_code)
    if user_state is False:
        logger.error("user {} is not registered on system.".format(user_code))
        return user_state
    elif user_state is True:
        doc_ref.update({
            u"univ_code": univ_code
        })
        return user_state
    else:
        logger.critical("db: {}, user_code: {}, univ_code: {}".format(db, user_code, univ_code))


def add_admin(db, user_code: int):
    add_user(db, user_code)
    db.collection(u"admin").document(str(user_code)).set({
        "admin_code": user_code
    })
    logger.info("Now user {} is admin.".format(user_code))
    return True


def del_admin(db, user_code: int):
    del_user(db, user_code)
    db.collection(u"admin").document(str(user_code)).delete()
    logger.info("Now user {} is not admin.".format(user_code))


def show_keyword(db, user_code: int):
    logger.info("User {} trying to show keywords".format(user_code))
    doc = db.collection(u"users").document(str(user_code)).get()
    doc = doc.to_dict()
    return doc["keywords"]


def set_keyword(db, user_code: int, keyword: str):
    logger.info("User {} trying to register keyword {}".format(user_code, keyword))
    user_doc_ref = db.collection(u"users").document(str(user_code))
    doc = user_doc_ref.get()
    doc = doc.to_dict()
    if keyword in doc:
        logger.error("Duplicated keyword {}".format(keyword))
        return False
    elif keyword not in doc:
        user_doc_ref.update({
            u"keywords": firestore.ArrayUnion([keyword])
        })
        keyword_doc_ref = db.collection(u"{} keywords".format(doc["univ_code"])).document(keyword)
        keyword_doc = keyword_doc_ref.get()
        keyword_doc = keyword_doc.to_dict()
        if keyword_doc is True:
            keyword_doc_ref.update({
                u"users": firestore.ArrayUnion([user_code])
            })
        elif keyword_doc is False:
            keyword_doc_ref.set({
                u"users": firestore.ArrayUnion([user_code])
            })
        logger.info("keyword {} registered to user {}".format(keyword, user_code))
        return True
    else:
        logger.critical("db: {}, user_code: {}, keyword: {}".format(db, user_code, keyword))


def del_keyword(db, user_code: int, keyword: str):
    logger.info("User {} trying to delete keyword {}".format(user_code, keyword))
    user_doc_ref = db.collection(u"users").document(str(user_code))
    doc = user_doc_ref.get()
    doc = doc.to_dict()
    if keyword in doc:
        user_doc_ref.update({
            u"keywords": firestore.ArrayRemove([keyword])
        })
        keyword_doc_ref = db.collection(u"{} keywords".format(doc["univ_code"])).document(keyword)
        keyword_doc = keyword_doc_ref.get()
        keyword_doc = keyword_doc.to_dict()
        if keyword_doc is True:
            keyword_doc_ref.update({
                u"users": firestore.ArrayRemove([user_code])
            })
        elif keyword_doc is False:
            keyword_doc_ref.set({
                u"users": firestore.ArrayRemove([user_code])
            })
        logger.info("Keyword {} removed by user {}".format(keyword, user_code))
        return True
    elif keyword not in doc:
        logger.error("Keyword {} not found.".format(keyword))
        return False
    else:
        logger.critical("db: {}, user_code: {}, keyword: {}".format(db, user_code, keyword))


def get_keywords(db, univ_code: str):
    return db.collection(u"{} keywords".format(univ_code)).get()


# 동국대 경주
def on_snapshot_dongguk_univ_gyeongju(doc_snapshot, changes, read_time):
    global dongguk_univ_gyeongju_init
    if dongguk_univ_gyeongju_init is False:
        for doc in changes:
            logger.info("Initializing dongguk univ gyeongju db snapshot {}".format(doc))
        logger.info("Finished dongguk univ gyeongju db snapshot init process.")
        dongguk_univ_gyeongju_init = True
    elif dongguk_univ_gyeongju_init is True:
        for doc in changes:
            logger.info("Found new content {}".format(doc))
            telegram_bot_handler.send_noti("135580816", doc)
    else:
        logger.critical("changes: {}".format(changes))


def watch_collection_dongguk_univ_gyeongju(db):
    doc_ref = db.collection(u'동국대학교 경주캠퍼스')
    doc_watch = doc_ref.on_snapshot(on_snapshot_dongguk_univ_gyeongju)


# 동국대 서울
def on_snapshot_dongguk_univ_seoul(doc_snapshot, changes, read_time):
    global dongguk_univ_seoul_init
    if dongguk_univ_gyeongju_init is False:
        for doc in changes:
            logger.info("Initializing dongguk univ seoul db snapshot {}".format(doc.to_dict))
        dongguk_univ_seoul_init = True
        logger.info("Finished dongguk univ seoul db snapshot init process.")
    elif dongguk_univ_gyeongju_init is True:
        for doc in changes:
            logger.info("Found new content {}".format(doc.to_dict))

    else:
        logger.critical("changes: {}".format(changes.to_dict()))


def watch_collection_dongguk_univ_seoul(db):
    doc_ref = db.collection(u'동국대학교 서울캠퍼스')
    doc_watch = doc_ref.on_snapshot(on_snapshot_dongguk_univ_gyeongju)


# 한양대학교
def on_snapshot_hanyang_univ(doc_snapshot, changes, read_time):
    global hanyang_univ_init
    if hanyang_univ_init is False:
        for doc in changes:
            logger.info("Initializing hanyang univ db snapshot {}".format(doc.to_dict))
        hanyang_univ_init = True
        logger.info("Finished hanyang univ db snapshot init process.")
    elif hanyang_univ_init is True:
        for doc in changes:
            logger.info("Found new content {}".format(doc.to_dict))

    else:
        logger.critical("changes: {}".format(changes.to_dict()))


def watch_collection_hanyang_univ(db):
    doc_ref = db.collection(u'한양대학교')
    doc_watch = doc_ref.on_snapshot(on_snapshot_dongguk_univ_gyeongju)


# 경기대학교
def on_snapshot_gyeonggui_univ(doc_snapshot, changes, read_time):
    global gyeonggui_univ_init
    if gyeonggui_univ_init is False:
        for doc in changes:
            logger.info("Initializing gyeonggui univ db snapshot {}".format(doc.to_dict))
        gyeonggui_univ_init = True
        logger.info("Finished gyeonggui univ db snapshot init process.")
    elif gyeonggui_univ_init is True:
        for doc in changes:
            logger.info("Found new content {}".format(doc.to_dict))

    else:
        logger.critical("changes: {}".format(changes.to_dict()))


def watch_collection_gyeonggui_univ(db):
    doc_ref = db.collection(u'경기대학교')
    doc_watch = doc_ref.on_snapshot(on_snapshot_dongguk_univ_gyeongju)
