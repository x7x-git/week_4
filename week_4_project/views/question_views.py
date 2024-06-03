from flask import Blueprint, render_template, request, url_for, g, flash, redirect, abort
from week_3_project.forms import QuestionForm, AnswerForm
from week_3_project.views.auth_views import login_required
import week_3_project.models as models

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

@bp.route('/detail/<int:question_id>/')
def q_detail(question_id):
    question = models.get_question_by_id(question_id)
    if question is None:
        abort(404)
    answers = models.get_answers_by_question_id(question_id)
    form = AnswerForm()
    return render_template('question/question_detail.html', question=question, answers=answers, form=form)

@bp.route('/create/', methods=('GET', 'POST'))
@login_required
def q_create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        models.insert_question(form.title.data, form.content.data, g.user['id'])
        return redirect(url_for('question.q_list'))
    return render_template('question/question_form.html', form=form)

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