class DevelopmentConfig():
    DEBUG = True
    # CONFIG MYSQL → CONNECTION DB
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'flask-contacts'


config = {
    'development': DevelopmentConfig
}