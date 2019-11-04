from flask import request, render_template, Blueprint, send_from_directory, current_app,redirect, url_for,flash
from it_center.users.utils import verify_login
from flask_login import login_user, current_user, logout_user, login_required
import json, os   
from it_center.models import Course,Shift, Role, User, TuitionReceipt
from it_center.educate.forms import UpdateCourseForm, CreateCourseForm
from datetime import datetime, date
 
educate = Blueprint('educate', __name__) 
@educate.route("/educate/<string:page>",methods=['GET','POST']) 
@login_required
def index(page): 
    if current_user.is_authenticated:   
        activate = list(range(10))
        activate[3] = "active"
        page = int(page)
        if page is None or page == 1:  
            page = request.args.get('page', 1, type=int) 
            courses = Course.objects.order_by('-finish_date').limit(10)
        elif page <= -1:
            page = int((Course.objects.count()-10) /10) + 2   
            num_skip = Course.objects.count()-10
            if num_skip <0: num_skip = 0
            courses = Course.objects.order_by('-finish_date').skip(num_skip)
        else:
            courses = Course.objects.order_by('-finish_date').skip(page*10-10).limit(10)
        now = datetime.utcnow() 
        return render_template('educate.html', title='Educate',activate=activate,courses=courses,page_num=page,now=now)
    return redirect(url_for('users.login'))

@educate.route("/educate/info/<string:id>",methods=['GET','POST']) 
@login_required
def educate_info(id): 
    if current_user.is_authenticated:   
        activate = list(range(10))
        activate[3] = "active"
        form = UpdateCourseForm()    
        if id is None:
            return redirect(url_for('educate.index'))
        course = Course.objects(id=id).first_or_404()    
        if form.validate_on_submit():  
            role_teacher = Role.objects(name='teacher').first()
            list_teacher = User.objects(role=role_teacher,is_activate=True)
            course.name = form.name.data
            course.start_date = form.start_date.data
            course.finish_date = form.finish_date.data 
            course.tuition = float(form.tuition.data)
            shift = Shift.objects(name=form.shift.data).first() 
            course.shift = shift  
            for item in list_teacher:
                if item.first_name + ' ' + item.last_name == form.teacher.data:
                    course.teacher = item
                    break
             
            if form.status.data == 'True':
                course.status = True
            else:
                course.status = False   
            course.save()
            flash('Course has been updated!', 'success')
            return redirect(url_for('educate.educate_info',id=id))
        elif request.method == 'GET':
            form.id_course.data = course.id_course
            form.name.data = course.name
            form.start_date.data = course.start_date
            form.finish_date.data = course.finish_date
            form.tuition.data = course.tuition  
            
            form.shift.data = course.shift.name
            form.teacher.data = course.teacher.first_name +' ' + course.teacher.last_name
           
            form.status.data = course.status
            TuitionReceipts = TuitionReceipt.objects(course=course)    
        return render_template('educate_info.html', title='Educate Info',activate=activate,form=form,students=course.list_student,id_course=id, TuitionReceipts=TuitionReceipts)
    return redirect(url_for('users.login'))

@educate.route("/educate/remove/<string:id_course>/<string:id>",methods=['GET','POST']) 
@login_required
def remove_student(id_course,id):  
    if current_user.is_authenticated: 
        course = Course.objects(id=id_course).first()
        for item in course.list_student: 
            if str(item.id) == id: 
                course.list_student.pop(course.list_student.index(item)) 
                flash('Remove student success!', 'success') 
                course.save()
                break  
        return redirect(url_for('educate.educate_info',id = str(id_course)))
    return redirect(url_for('users.login'))

@educate.route("/educate/remove/<string:id>",methods=['GET','POST']) 
@login_required
def remove_course(id):  
    if current_user.is_authenticated: 
        course = Course.objects(id=id).first()
        if course is None:
            flash('Can\'t find out course. Please contact admin!', 'danger') 
            return redirect(url_for('educate.index',page=1)) 
        if len(course.list_student) > 0:
            flash('Can\'t remove course cause there are student in here. Must be remove all student before remove this course!', 'danger') 
            return redirect(url_for('educate.index',page=1)) 
        course.delete() 
        return redirect(url_for('educate.index',page=1)) 
    return redirect(url_for('users.login'))

@educate.route("/api/educate/<string:id>",methods=['GET']) 
@login_required
def get_course(id): 
    if current_user.is_authenticated:   
        activate = list(range(10))
        activate[3] = "active"
      

        course = Course.objects(id=id).first()
        if course:
            response = {
                'status':True,
                'message':'Get Course Success',
                'data':course
            }
        else:
            response = {
                'status':False,
                'message':'Get Course Failed',
                'data': None
            }

    return response

@educate.route("/api/educate/get/<string:keyword>",methods=['GET']) 
@login_required
def get_course_keyword(keyword):  
    if keyword is not None:
        if keyword == 'all':
            course = Course.objects(is_activate=True).order_by('finish_date').limit(10)
            list_course = list()
            for item in course: 
                ele = {
                    "id":str(item.id),
                    "created_date": item.created_date.strftime("%m-%d-%Y"), 
                    "finish_date": item.finish_date.strftime("%m-%d-%Y"), 
                    "id_course":item.id_course, 
                    "is_activate": item.status,  
                    "name":item.name , 
                    "shift": item.shift.name, 
                    "start_date": item.start_date.strftime("%m-%d-%Y"), 
                    "status": item.status, 
                    "teacher":item.teacher.first_name + ' ' + item.teacher.last_name, 
                    "tuition": item.tuition
                }
                list_course.append(ele)
            if list_course:
                response = {
                    'status':True,
                    'message':'Get Course Success',
                    'data':list_course
                }
            else:
                response = {
                    'status':False,
                    'message':'Get Course Failed',
                    'data': None
                } 
        else:
            course = Course.objects(is_activate=True,id_course__istartswith=keyword).limit(5)
            list_course = list()
            for item in course: 
                ele = {
                    "id":str(item.id),
                    "created_date": item.created_date.strftime("%m-%d-%Y"), 
                    "finish_date": item.finish_date.strftime("%m-%d-%Y"), 
                    "id_course":item.id_course, 
                    "is_activate": item.is_activate,  
                    "name":item.name , 
                    "shift": item.shift.name, 
                    "start_date": item.start_date.strftime("%m-%d-%Y"), 
                    "status": item.status, 
                    "teacher":item.teacher.first_name + ' ' + item.teacher.last_name, 
                    "tuition": item.tuition
                }
                list_course.append(ele)
            
            course = Course.objects(is_activate=True,name__istartswith=keyword).limit(5)

            for item in course: 
                flag = False
                for i in list_course: 
                    if i['id'] == str(item.id):
                        flag = True
                        break
                if flag == False:
                    ele = {
                        "id":str(item.id),
                        "created_date": item.created_date.strftime("%m-%d-%Y"), 
                        "finish_date": item.finish_date.strftime("%m-%d-%Y"), 
                        "id_course":item.id_course, 
                        "is_activate": item.is_activate,  
                        "name":item.name , 
                        "shift": item.shift.name, 
                        "start_date": item.start_date.strftime("%m-%d-%Y"), 
                        "status": item.status, 
                        "teacher":item.teacher.first_name + ' ' + item.teacher.last_name, 
                        "tuition": item.tuition
                    }
                    list_course.append(ele)
            
            if list_course:
                response = {
                    'status':True,
                    'message':'Get Course Success',
                    'data':list_course
                }
            else:
                response = {
                    'status':False,
                    'message':'Get Course Failed',
                    'data': None
                } 
    else:
        response = {
            'status':False,
            'message':'Get Course Failed',
            'data': None
        } 
    return response

@educate.route("/api/shift/<string:id>",methods=['GET']) 
@login_required
def get_shift(id): 
    if current_user.is_authenticated:   
        activate = list(range(10))
        activate[3] = "active" 
        shift = Shift.objects(id=id).first()
        if shift:
            response = {
                'status':True,
                'message':'Get Shift Success',
                'data':shift
            }
        else:
            response = {
                'status':False,
                'message':'Get Shift Failed',
                'data': None
            }

    return response

@educate.route("/educate/create", methods=['GET', 'POST']) 
@login_required
def create(): 
    activate = list(range(10))
    activate[3] = "active"
    if current_user.is_authenticated:    
        form = CreateCourseForm()   
        if form.validate_on_submit():  
            id_course = form.id_course.data
            course = Course.objects(id_course=id_course).first()
            if course is None:
              
                name = form.name.data

                start_date = form.start_date.data
                finish_date = form.finish_date.data 
                tuition = float(form.tuition.data)
                shift = Shift.objects(name=form.shift.data).first()   
                role_teacher = Role.objects(name='teacher').first()
                list_teacher = User.objects(role=role_teacher,is_activate=True)
                for item in list_teacher:
                    if item.first_name + ' ' + item.last_name == form.teacher.data:
                        teacher = item
                        break
                course = Course(id_course=id_course, name=name,start_date=start_date, finish_date=finish_date,tuition=tuition,shift=shift,teacher=teacher)  
                course.save()
                flash('Course has been created!', 'success')
                return redirect(url_for('educate.educate_info',id=course.id))  
            flash('Course is exist!, please check again', 'danger')
            return redirect(url_for('educate.create'))  

        return render_template('educate_create.html', title='Educate Create Course',activate=activate,form=form)
    return redirect(url_for('users.login'))