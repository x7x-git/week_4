from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileField, FileAllowed

class QuestionForm(FlaskForm):
    title = StringField('제목', validators=[DataRequired('제목은 필수입력 항목입니다.')])
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])
    password = PasswordField('비밀번호', validators=[Length(min=0, max=200)])
    file = FileField('파일 업로드', validators=[FileAllowed(['txt'], '파일 형식이 올바르지 않습니다.')])

class AnswerForm(FlaskForm):
    content = TextAreaField('내용', validators=[DataRequired('내용은 필수입력 항목입니다.')])

class UserCreateForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired('닉네임은 필수입력 항목입니다.'), Length(min=3, max=25)])
    password1 = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수입력 항목입니다.'), EqualTo('password2', '비밀번호가 일치하지 않습니다')])
    password2 = PasswordField('비밀번호 확인', validators=[DataRequired('비밀번호는 필수입력 항목입니다.')])
    email = EmailField('이메일', validators=[DataRequired('이메일은 필수입력 항목입니다.'), Email('이메일 형식이 올바르지 않습니다.')])
    name = StringField('성명', validators=[DataRequired('이름은 필수입력 항목입니다.')])
    school = StringField('학교', validators=[DataRequired('학교는 필수입력 항목입니다.')])

class UserLoginForm(FlaskForm):
    username = StringField('사용자 이름', validators=[DataRequired('이름은 필수입력 항목입니다.'), Length(min=3, max=25)])
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수입력 항목입니다.')])

class ProfileForm(FlaskForm):
    name = StringField('이름', validators=[DataRequired('이름은 필수입력 항목입니다.')])
    school = StringField('학교', validators=[DataRequired('학교는 필수입력 항목입니다.')])
    profile_image = FileField('프로필 이미지', validators=[FileAllowed(['jpg', 'png'], '이미지 파일만 업로드 가능합니다.')])





class FindUsernameForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired('이메일은 필수입력 항목입니다.'), Email('이메일 형식이 올바르지 않습니다.')])
    submit = SubmitField('아이디 찾기')

class ResetPasswordRequestForm(FlaskForm):
    email = EmailField('이메일', validators=[DataRequired('이메일은 필수입력 항목입니다.'), Email('이메일 형식이 올바르지 않습니다.')])
    submit = SubmitField('비밀번호 재설정')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('비밀번호', validators=[DataRequired('비밀번호는 필수입력 항목입니다.')])
    submit = SubmitField('비밀번호 재설정')