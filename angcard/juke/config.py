# -*- encoding=utf-8 -*-


class BaseConfig(object):
    CARD_BIN = '999'
    EMAIL_ACCOUNT = 'no_reply@juke100.com'
    EMAIL_PASSWORD = 'zhangwei010158'
    WEBPOS_HOST = '127.0.0.1'
    WEBPOS_PORT = 8005
    SECRET_KEY = '6dd0e73fd261454e849d1ad35e2ee811'
    SINA_WEIBO_APP_KEY = '3086646579'
    SINA_WEIBO_APP_SECRET = 'fc29332cac6fef39f2a1e4def1bcbd51'


class DevelopmentConfig(BaseConfig):
    DOMAIN = 'http://127.0.0.1'
    DATABASE_URI = 'postgresql://postgres:123456@localhost/jf_card'
    DATABASE_ECHO = True
    DEBUG = True
    PROFILE_IMG_DIR = 'e:/coolcard/angcard/juke/static/profile_images'


class ProductionConfig(BaseConfig):
    DOMAIN = 'http://app.juke100.com'
    DATABASE_URI = 'postgresql://postgres:123456@localhost/jf_card'
    DATABASE_ECHO = True
    DEBUG = False
