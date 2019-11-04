from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField,SelectField,widgets,FieldList,FormField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from flask_login import current_user
from it_center.models import Course,User, Shift, Role
from wtforms.fields.html5 import DateField

list_shift = Shift.objects.all()
shift_choices = [(str(c['name']), c['name']) for c in list_shift]  

role_teacher = Role.objects(name='teacher').first()
list_teacher = User.objects(role=role_teacher,is_activate=True)
teacher_choices = [ (c['first_name'] +' ' +  c['last_name'], c['first_name'] +' ' +  c['last_name']) for c in list_teacher]

class UpdateCourseForm(FlaskForm):
    id_course = StringField('Code', validators=[DataRequired(), Length(min=2, max=30)])
    name = StringField('Course Name', validators=[DataRequired(), Length(min=2, max=50)]) 
    start_date = DateField('Start Date', validators=[DataRequired()] )
    finish_date = DateField('Finish Date', validators=[DataRequired()] )
    tuition = StringField('Tuition', validators=[DataRequired()]) 
    shift = SelectField('Shift',choices=shift_choices, validators=[DataRequired()])
    teacher = SelectField('Teacher',choices=teacher_choices, validators=[DataRequired()]) 
    status = SelectField('Status',choices=[("True", "True"), ("False", "False")], validators=[DataRequired()]) 
    submit = SubmitField('Update')

class CreateCourseForm(FlaskForm):
    id_course = StringField('Code', validators=[DataRequired(), Length(min=2, max=30)])
    name = StringField('Course Name', validators=[DataRequired(), Length(min=2, max=50)]) 
    start_date = DateField('Start Date', validators=[DataRequired()] )
    finish_date = DateField('Finish Date', validators=[DataRequired()] )
    tuition = StringField('Tuition', validators=[DataRequired()]) 
    shift = SelectField('Shift',choices=shift_choices, validators=[DataRequired()])
    teacher = SelectField('Teacher',choices=teacher_choices, validators=[DataRequired()]) 
    submit = SubmitField('Create')

    def validate_id_course(self, id_course): 
        if current_user.user.role.name == 'admin' or current_user.user.role.name == 'academic':
            course = Course.objects(id_course=id_course.data).first()
            if course:
                raise ValidationError('That username is taken. Please choose a different one.')
        else:
            raise ValidationError('You\'re not a member of system. Please contact to manager.')
            

    def validate_tuition(self, tuition):
        if current_user.user.role.name == 'admin' or current_user.user.role.name == 'academic':
            if float(tuition.data) < 0:
                raise ValidationError('Tuition must be larger than 0.')
        else:
            raise ValidationError('You\'re not a member of system. Please contact to manager.')
    
    def validate_teacher(self, teacher): 
        if current_user.user.role.name == 'admin' or current_user.user.role.name == 'academic':
            flag = False
            role_teacher = Role.objects(name='teacher').first()
            list_teacher = User.objects(role=role_teacher,is_activate=True)
            for item in list_teacher:
                if item.first_name + ' ' + item.last_name == teacher.data:
                    flag = True
                    break 
            if flag == False:
                raise ValidationError('Name teacher isn\'t exist. Please reload page and input again')
        else:
            raise ValidationError('You\'re not a member of system. Please contact to manager.')
    
    def validate_date(self, start_date, finish_date):
        print(start_date.data, finish_date.data)
        if current_user.user.role.name == 'admin' or current_user.user.role.name == 'academic':
            if finish_date.data < start_date.data:
                raise ValidationError('Finish date must be after start date')
        else:
            raise ValidationError('You\'re not a member of system. Please contact to manager.')
    

    
 