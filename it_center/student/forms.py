from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,widgets,FieldList,FormField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from it_center.models import Course,User, Shift
from wtforms.fields.html5 import DateField
from datetime import datetime
 
class AddStudentToClass(FlaskForm):

    list_course = Course.objects.all() 
    course_choices = [(str(c['id']), c['id_course']) for c in list_course if c.finish_date >= datetime.utcnow()] 
    
    list_shift = Shift.objects.all()
    shift_choices = [(str(c['id']), c['name']) for c in list_shift] 

    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(min=10)])
    email = StringField('Email', validators=[DataRequired(), Length(min=10),Email()])
    birth = DateField('Birth', validators=[DataRequired()] )
    gender = SelectField('Gender',choices=[("Male", "Male"), ("Female", "Female")], validators=[DataRequired()]) 
    course = SelectField('Code Course',choices=course_choices, validators=[DataRequired()]) 
    shift = StringField('Shift', validators=[DataRequired()]) 
    course_name = StringField('Course Name', validators=[DataRequired()])  
    course_tuition = StringField('Tuition',validators=[DataRequired()])
    money_return = StringField('Money Return',validators=[DataRequired()])
    reservate_tuition = StringField('Reservate Tuition',validators=[DataRequired()])
    submit = SubmitField('Create Receipt')

class UpdateStudentToClass(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=30)])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=9, max=15)])
    address = StringField('Address', validators=[DataRequired(), Length(min=10)])
    email = StringField('Email', validators=[DataRequired(), Length(min=10),Email()])
    birth = DateField('Birth', validators=[DataRequired()] )
    gender = SelectField('Gender',choices=[("Male", "Male"), ("Female", "Female")], validators=[DataRequired()]) 
    course = StringField('Code Course', validators=[DataRequired()]) 
    shift = StringField('Shift',validators=[DataRequired()]) 
    course_name = StringField('Course Name', validators=[DataRequired()])  
    course_tuition = StringField('Tuition',validators=[DataRequired()])
    reservate_tuition = StringField('Paid Tuition',validators=[DataRequired()])
    next_pay = StringField('Next Tuition',validators=[DataRequired()])
    money_return = StringField('Money Return',validators=[DataRequired()])
    submit = SubmitField('Update Receipt')