import os

class Config:
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'week_4'
    MYSQL_CHARSET = 'utf8'

    SECRET_KEY = "dev"

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    QUESTION_FILE_ALLOWED_EXTENSIONS = {'txt'}
    PROFILE_IMAGE_ALLOWED_EXTENSIONS = {'jpg', 'png'}
    QUESTION_FILE_UPLOAD_FOLDER = 'week_4_project/static/question_files'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'week_4_project/static/profile_images')

    MAIL_SERVER = ''
    MAIL_PORT = 587
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    SECURITY_PASSWORD_SALT = 'dev'