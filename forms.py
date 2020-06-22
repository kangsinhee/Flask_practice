from flask_wtf import FlaskForm
from models import cuser
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class RegisterForm(FlaskForm):
    userid = StringField('userid', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])

class LoginForm(FlaskForm):
    class UserPassword(object):
        def __init__(self, message=None):
            self.message = message
        def __call__(self,form,field):
            userid = form['userid'].data
            password = field.data
            fcuser = cuser.query.filter_by(userid=userid).first()
            if fcuser.password != password:
                raise ValueError('패스워드가 틀렸습니다.')
    userid = StringField('userid', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired(), UserPassword()])