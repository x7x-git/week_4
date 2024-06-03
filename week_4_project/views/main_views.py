from flask import Blueprint, url_for, redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_x7x():
    return '안뇽'

@bp.route('/')
def index():
    return redirect(url_for('question.q_list'))