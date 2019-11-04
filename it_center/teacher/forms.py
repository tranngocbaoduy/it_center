from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,widgets,FieldList,FormField,FloatField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from it_center.models import Course,User, Shift
from wtforms.fields.html5 import DateField
from datetime import datetime
 

class PaymentReceiptForm(FlaskForm):  
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(min=5)])
    email = StringField('Email', validators=[DataRequired(), Length(min=10),Email()])
    birth = DateField('Birth', validators=[DataRequired()] )
    salary = FloatField('Basic Salary', validators=[] )
    from_date = DateField('From', validators=[DataRequired()] )
    to_date = DateField('To', validators=[DataRequired()] )
    payment = FloatField('Salary', validators=[DataRequired()] )
    gender = StringField('Gender',validators=[DataRequired()])
    role = StringField('Role', validators=[DataRequired()])  
    submit = SubmitField('Create Receipt')
 
class UpdateTeacherForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(min=10)])
    salary = FloatField('Inital Salary', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Length(min=10),Email()])
    birth = DateField('Birth', validators=[DataRequired()] )
    gender = SelectField('Gender',choices=[("Male", "Male"), ("Female", "Female")], validators=[DataRequired()]) 
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png','jpeg','JPG','PNG'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is None:
            raise ValidationError('That username isn\'t exist.')

    def validate_email(self, email):  
        user = User.objects(email=email.data).first() 
        if user is None:
            raise ValidationError('That username isn\'t exist.')
    
    def validate_phone(self, phone): 
        user = User.objects(phone=phone.data).first()
        if user is None:
            raise ValidationError('That username isn\'t exist.')

    def validate_salary(self, salary): 
        if float(salary.data) < 10:
            raise ValidationError('Salary must be larger than 10!!')