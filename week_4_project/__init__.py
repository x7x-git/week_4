from flask import Flask, render_template, g
from pymysql.cursors import DictCursor
from config import Config
import pymysql
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    def get_db_connection():
        connection = pymysql.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            db=Config.MYSQL_DB,
            charset=Config.MYSQL_CHARSET,
            cursorclass=DictCursor
        )
        return connection

    @app.before_request
    def before_request():
        if 'db' not in g:
            g.db = get_db_connection()
            #print('DB Conn!')

    @app.teardown_request
    def teardown_request(exception):
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()
            #print('DB Closed!')

    from week_4_project.views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    
    if not os.path.exists(app.config['QUESTION_FILE_UPLOAD_FOLDER']):
        os.makedirs(app.config['QUESTION_FILE_UPLOAD_FOLDER'])

    return app