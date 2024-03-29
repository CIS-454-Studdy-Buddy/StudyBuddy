class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SECRET_KEY = 'thisisasecretkey'
    MAIL_SERVER ='smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'su.study.buddy@gmail.com'
    MAIL_PASSWORD = 'mvzuqlkwoedrkcsi'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class DebugConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    DEBUG = False
    TESTING = True

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    DEBUG = False
    TESTING = True 
