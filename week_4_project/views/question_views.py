from flask import Blueprint, render_template, request, url_for, g, flash, redirect, abort, current_app, send_from_directory
from week_4_project.forms import QuestionForm, AnswerForm
from week_4_project.views.auth_views import login_required
from werkzeug.security import generate_password_hash, check_password_hash
import week_4_project.models as models
import os
import uuid

bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/list/')
def q_list():
    page = request.args.get('page', type=int, default=1)
    kw = request.args.get('kw', type=str, default='')
    per_page = 2
    offset = (page - 1) * per_page

    question_list = models.get_paginated_questions(offset, per_page)
    if kw:
        question_list = models.search_questions(kw, offset, per_page)

    total_questions = models.get_question_count()
    total_pages = (total_questions + per_page - 1) // per_page
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw, total_pages=total_pages, per_page=per_page)

def allowed_question_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['QUESTION_FILE_ALLOWED_EXTENSIONS']

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def q_create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        password = form.password.data
        if password:
            password = generate_password_hash(password)
        
        file_path = None
        file = form.file.data
        if file and allowed_question_file(file.filename):
            file_ext = file.filename.split('.')[-1]
            file_path = f"{g.user['id']}_{uuid.uuid4().hex}.{file_ext}"
            file.save(os.path.join(current_app.config['QUESTION_FILE_UPLOAD_FOLDER'], file_path))
        
        models.insert_question(form.title.data, form.content.data, g.user['id'], password, file_path)
        return redirect(url_for('question.q_list'))
    return render_template('question/question_form.html', form=form)

@bp.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(current_app.config['QUESTION_FILE_UPLOAD_FOLDER'], filename, as_attachment=True)

@bp.route('/detail/<int:question_id>/', methods=('GET', 'POST'))
def q_detail(question_id):
    question = models.get_question_by_id(question_id)
    if question is None:
        abort(404)
    if question['password']:
        if request.method == 'POST':
            password = request.form['password']
            if not check_password_hash(question['password'], password):
                flash('비밀번호가 틀렸습니다.')
                return redirect(url_for('question.q_detail', question_id=question_id))
        else:
            return render_template('question/question_password.html', question_id=question_id)
    answers = models.get_answers_by_question_id(question_id)
    form = AnswerForm()
    return render_template('question/question_detail.html', question=question, answers=answers, form=form)

@bp.route('/modify/<int:question_id>/', methods=('GET', 'POST'))
@login_required
def modify(question_id):
    question = models.get_question_by_id(question_id)
    if question is None or g.user['id'] != question['user_id']:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.q_detail', question_id=question_id))
    if request.method == 'POST':
        form = QuestionForm()
        if form.validate_on_submit():
            models.update_question(question_id, form.title.data, form.content.data)
            return redirect(url_for('question.q_detail', question_id=question_id))
    else:
        form = QuestionForm(data={'title': question['title'], 'content': question['content']})
    return render_template('question/question_form.html', form=form)

@bp.route('/delete/<int:question_id>/')
@login_required
def delete(question_id):
    question = models.get_question_by_id(question_id)
    if question is None or g.user['id'] != question['user_id']:
        flash('삭제권한이 없습니다')
        return redirect(url_for('question.q_detail', question_id=question_id))
    models.delete_question(question_id)
    return redirect(url_for('question.q_list'))