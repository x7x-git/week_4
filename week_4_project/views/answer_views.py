from flask import Blueprint, url_for, render_template, redirect, abort, flash, request, g
from datetime import datetime
from week_3_project.forms import AnswerForm
import week_3_project.models as models
from .auth_views import login_required

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>/', methods=('POST',))
@login_required
def create(question_id):
    form = AnswerForm()
    question = models.get_question_by_id(question_id)
    if question is None:
        abort(404)
    
    if form.validate_on_submit():
        content = form.content.data
        models.insert_answer(question_id, content, g.user['id'])
        return redirect(url_for('question.q_detail', question_id=question_id))
    
    answers = models.get_answers_by_question_id(question_id)
    return render_template('question/question_detail.html', question=question, answers=answers, form=form)

@bp.route('/modify/<int:answer_id>/', methods=('GET', 'POST'))
@login_required
def modify(answer_id):
    answer = models.get_answer_by_id(answer_id)
    if answer is None or g.user['id'] != answer['user_id']:
        flash('수정권한이 없습니다')
        return redirect(url_for('question.q_detail', question_id=answer['question_id']))
    if request.method == 'POST':
        form = AnswerForm()
        if form.validate_on_submit():
            models.update_answer(answer_id, form.content.data)
            return redirect(url_for('question.q_detail', question_id=answer['question_id']))
    else:
        form = AnswerForm(data={'content': answer['content']})
    return render_template('answer/answer_form.html', form=form)

@bp.route('/delete/<int:answer_id>/')
@login_required
def delete(answer_id):
    answer = models.get_answer_by_id(answer_id)
    if answer is None:
        abort(404)
    question_id = answer['question_id']
    if g.user['id'] != answer['user_id']:
        flash('삭제권한이 없습니다')
    else:
        models.delete_answer(answer_id)
    return redirect(url_for('question.q_detail', question_id=question_id))