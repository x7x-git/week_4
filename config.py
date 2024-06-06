import os

class Config:
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'root'
    MYSQL_DB = 'week_4'
    MYSQL_CHARSET = 'utf8'
    SECRET_KEY = "dev"
    UPLOAD_FOLDER = 'week_4_project/static/profile_images'
    PROFILE_IMAGE_ALLOWED_EXTENSIONS = {'jpg', 'png'}
    QUESTION_FILE_UPLOAD_FOLDER = 'week_4_project/static/question_files'
    QUESTION_FILE_ALLOWED_EXTENSIONS = {'txt'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024