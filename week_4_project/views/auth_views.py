from flask import Blueprint, url_for, render_template, flash, abort, request, session, g, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
import week_4_project.models as models
from week_4_project.forms import UserCreateForm, UserLoginForm, ProfileForm, FindUsernameForm, ResetPasswordRequestForm, ResetPasswordForm
import functools
import os
import uuid
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

bp = Blueprint('auth', __name__, url_prefix='/auth')
mail = Mail()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            _next = request.url if request.method == 'GET' else ''
            return redirect(url_for('auth.signin', next=_next))
        return view(*args, **kwargs)
    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = models.get_user_by_id(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = models.get_user_by_username(form.username.data)
        email = models.get_user_by_email(form.email.data)
        if not user and not email:
            hashed_password = generate_password_hash(form.password1.data)
            models.insert_user(form.username.data, hashed_password, form.email.data, form.name.data, form.school.data)
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자 이름 또는 이메일입니다.')
    return render_template('auth/signup.html', form=form)

@bp.route('/signin/', methods=('GET', 'POST'))
def signin():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = models.get_user_by_username(form.username.data)
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user['password'], form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            _next = request.args.get('next', '')
            if _next:
                return redirect(_next)
            else:
                return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/signin.html', form=form)

def allowed_profile_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['PROFILE_IMAGE_ALLOWED_EXTENSIONS']

@bp.route('/profile/', methods=('GET', 'POST'))
@login_required
def profile():
    form = ProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        school = form.school.data
        profile_image = form.profile_image.data
        if profile_image and allowed_profile_image(profile_image.filename):
            # 기존 프로필 이미지 삭제
            if g.user['profile_image']:
                existing_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], g.user['profile_image'])
                if os.path.exists(existing_image_path):
                    os.remove(existing_image_path)
            
            file_ext = profile_image.filename.split('.')[-1]
            profile_image_filename = f"{g.user['id']}_{uuid.uuid4().hex}.{file_ext}"
            profile_image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], profile_image_filename))
            g.user['profile_image'] = profile_image_filename
        models.update_user_profile(g.user['id'], name, school, g.user['profile_image'])
        flash('프로필이 업데이트되었습니다.')
        return redirect(url_for('auth.profile'))
    return render_template('profile.html', form=form, user=g.user, editable=True)

@bp.route('/profile/<int:user_id>/', methods=('GET',))
@login_required
def view_profile(user_id):
    user = models.get_user_by_id(user_id)
    if user is None:
        abort(404)
    form = ProfileForm(obj=user)
    return render_template('profile.html', form=form, user=user, editable=False)

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=current_app.config['SECURITY_PASSWORD_SALT'])

@bp.route('/reset_password_request/', methods=['GET', 'POST'])
def reset_password_request():
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        email = form.email.data
        user = models.get_user_by_email(email)
        if user:
            token = generate_reset_token(email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            msg = Message('비밀번호 재설정', sender=current_app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = f"비밀번호 재설정 링크: {reset_url}"
            mail.send(msg)
            flash('비밀번호 재설정 메일이 전송 되었습니다.', 'info')
        else:
            flash('등록된 이메일이 아닙니다.', 'danger')
        return redirect(url_for('auth.reset_password_request'))
    return render_template('auth/reset_password_request.html', form=form)

def confirm_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = serializer.loads(token, salt=current_app.config['SECURITY_PASSWORD_SALT'], max_age=expiration)
    except SignatureExpired:
        return False
    return email

@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = confirm_reset_token(token)
    except:
        flash('재설정 링크가 잘못되었거나 만료되었습니다.', 'danger')
        return redirect(url_for('auth.reset_password_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        hashed_password = generate_password_hash(password)
        models.update_user_password(email, hashed_password)
        flash('비밀번호가 업데이트 되었습니다.', 'success')
        return redirect(url_for('auth.signin'))
    return render_template('auth/reset_password.html', form=form)

@bp.route('/find_username/', methods=['GET', 'POST'])
def find_username():
    form = FindUsernameForm()
    if form.validate_on_submit():
        email = form.email.data
        user = models.get_user_by_email(email)
        if user:
            flash(f"사용자 ID: {user['username']}", 'info')
        else:
            flash('등록된 이메일이 아닙니다.', 'danger')
        return redirect(url_for('auth.find_username'))
    return render_template('auth/find_username.html', form=form)