from flask_babel import lazy_gettext as _
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,widgets
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from it_center.models import User,Course,Shift
from wtforms.fields.html5 import DateField

class LoginForm(FlaskForm):
    username = StringField('User Name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
  
class UpdateUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(min=10)])
    email = StringField('Email', validators=[DataRequired(), Length(min=10),Email()])
    birth = DateField('Birth', validators=[DataRequired()] )
    gender = SelectField('Gender',choices=[("Male", "Male"), ("Female", "Female")], validators=[DataRequired()]) 
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg','JPG','PNG'])])
    submit = SubmitField('Update')

     
    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
 
    def validate_phone(self, phone): 
        user = User.objects(phone=phone.data).first()
        if user:
            raise ValidationError('That phone is taken. Please choose a different one.')
            return

class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must contact to admin to register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
