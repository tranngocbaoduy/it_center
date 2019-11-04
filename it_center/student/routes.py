from flask import request, render_template, Blueprint,abort,flash,redirect,url_for
import json, os
from it_center.models import User, Account,Role, Course,TuitionReceipt,DetailTuitionReceipt, Shift
from it_center import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from it_center.users.utils import save_picture, send_reset_email, verify_login  
from it_center.users.forms import UpdateUserForm
from it_center.student.forms import AddStudentToClass, UpdateStudentToClass
from datetime import datetime

student = Blueprint('student', __name__)

@student.route("/student/<string:page>") 
@login_required
def index(page): 
    if current_user.is_authenticated:   
        activate = list(range(10))
        activate[1] = "active"
        page = int(page) 
        role = Role.objects(name='student').first()
        if page is None or page == 1:
            page = request.args.get('page', 1, type=int) 
            students = User.objects(role=role,is_activate=True).limit(10) 
        elif page <= -1:
            page = int((User.objects(role=role,is_activate=True).count()-10) /10) + 2   
            num_skip= User.objects(role=role).count()-10
            if num_skip < 0: num_skip = 0
            students = User.objects(role=role,is_activate=True).skip(num_skip)
        else:
            students = User.objects(role=role,is_activate=True).skip(page*10-10).limit(10)  
        return render_template('student.html', title='Student',activate=activate,students=students,page_num=page)
    return redirect(url_for('users.login'))

@student.route("/student/info/<string:id>", methods=['GET', 'POST']) 
@login_required
def student_info(id): 
    activate = list(range(10))
    activate[1] = "active"
    if current_user.is_authenticated:   

        user = User.objects(id=id,is_activate=True).first()  
        form = UpdateUserForm()  
        if id is None or user is None:
            return redirect(url_for('student.index',page=1))
  
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                user.image_file = picture_file
            user.first_name=form.first_name.data 
            user.last_name=form.last_name.data 
            user.phone =form.phone.data 
            user.email =form.email.data
            user.address =form.address.data
            user.birth =form.birth.data 
            user.gender = form.gender.data  
            
            user.save()
            flash('Student has been updated!', 'success')
            return redirect(url_for('student.student_info',id=id))
        elif request.method == 'GET':
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.phone.data = user.phone
            form.email.data = user.email
            form.address.data = user.address 
            form.gender.data = user.gender 
            form.birth.data = user.birth
 

        receipts = TuitionReceipt.objects(student=user) 
        return render_template('student_info.html', title='Student Info',activate=activate,student=user,form=form,receipts=receipts)
    return redirect(url_for('users.login'))

@student.route("/student/create_reciept/<string:id>", methods=['GET', 'POST']) 
@login_required
def create_receipt(id): 
    activate = list(range(10))
    activate[1] = "active"
    if current_user.is_authenticated:    
        user = User.objects(id=id,is_activate=True).first()  
        form = AddStudentToClass()  
        if id is None or user is None:
            return redirect(url_for('student.index'))  
    
        if form.validate_on_submit():
            id_course = form.course.data
            course = Course.objects(id=id_course).first()
            reservate_tuition = float(form.reservate_tuition.data)
            tuition_left = course.tuition - reservate_tuition
            money_return = 0 
            status = False
            if tuition_left <= 0:
                status = True 
                money_return = -1 * tuition_left  
                tuition_left = 0
            if course is None:
                flash('Can\'t find class, please inform to admin!', 'danger')
                return redirect(url_for('student.create_receipt',id=id)) 
            list_detail_tuition = list() 
            course.list_student.append(user)
            if len(course.list_student) > 5:
                course.status = True
            course.save()
            detail_receipt= DetailTuitionReceipt(tuition=reservate_tuition,money_return=money_return,created_user=current_user.user).save()
            list_detail_tuition.append(detail_receipt)
            receipt = TuitionReceipt(student=user, course=course,reservate_tuition=reservate_tuition,tuition_left=tuition_left,list_detail=list_detail_tuition,status=status).save()
            flash('Receipt has been created!', 'success')
            return redirect(url_for('student.student_info',id=id))
        

        # list_course = Course.objects.all() 
        # form.course_choices = [(str(c['id']), c['id_course']) for c in list_course if c.finish_date >= datetime.utcnow()] 
        
        # list_shift = Shift.objects.all()
        # form.shift_choices = [(str(c['id']), c['name']) for c in list_shift] 
        
        form.first_name.data = user.first_name
        form.last_name.data = user.last_name
        form.phone.data = user.phone
        form.email.data = user.email
        form.address.data = user.address
        form.birth.data = user.birth  
        form.gender.data = user.gender 
        form.reservate_tuition.data = 0 
        form.money_return.data = 0  
        return render_template('student_create_receipt.html', title='Student Info',activate=activate,student=user,form=form)
    return redirect(url_for('users.login'))

@student.route("/api/student/receipt/<string:id>", methods=['GET', 'POST']) 
@login_required
def get_receipt(id):  
    print(id)
    if current_user.is_authenticated:    
        receipt = TuitionReceipt.objects(id=id).first()
        print(receipt,receipt.list_detail)
        if receipt: 
            data = list()
            for item in receipt.list_detail:
                print("123")
                ele = {
                    'id':str(item.id), 
                    'user_name': item.created_user.first_name + item.created_user.last_name,
                    'tuition':item.tuition,
                    'money_return':item.money_return,
                    'created_date':item.created_date
                } 
                data.append(ele) 
            response = {
                'status':True,
                'message':'Get Receipt Success',
                'data':data
            } 
    else:
        response = {
            'status':False,
            'message':'Get Receipt Failed',
            'data': None
        }  
    return response

@student.route("/api/student/get/<string:key_word>", methods=['GET', 'POST']) 
@login_required
def get_student(key_word):  
    if current_user.is_authenticated:
        data = list()    
        role = Role.objects(name='student').first()
        if key_word == 'all':
            students = User.objects(role=role,is_activate=True).limit(10)
            if students:  
                for item in students:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "phone": item.phone,
                        "is_activate": item.is_activate
                    } 
                    data.append(ele)
                response = {
                    'status':True,
                    'message':'Get Students Success',
                    'data':data
                }  
        else:
            students = User.objects(role=role,is_activate=True,first_name__istartswith=key_word).limit(5) 
            if students:  
                for item in students:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "phone": item.phone,
                        "is_activate": item.is_activate
                    } 
                    data.append(ele)

            students = User.objects(role=role,is_activate=True,last_name__istartswith=key_word).limit(5)
            if students:  
                for item in students: 
                    flag = False
                    for ele in data:
                        if ele['id'] == item.id:
                            flag = True
                            break
                    if flag == False:        
                        ele = {
                            "id": str(item.id),
                            "address": item.address,
                            "birth": item.birth.strftime("%m-%d-%Y"),
                            "email": item.email,
                            "first_name": item.first_name,
                            "gender": item.gender,
                            "image_file": item.image_file,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            students = User.objects(role=role,is_activate=True,phone__istartswith=key_word).limit(5)
            if students:  
                for item in students: 
                    flag = False
                    for ele in data:
                        if ele['id'] == item.id:
                            flag = True
                            break
                    if flag == False:        
                        ele = {
                            "id": str(item.id),
                            "address": item.address,
                            "birth": item.birth.strftime("%m-%d-%Y"),
                            "email": item.email,
                            "first_name": item.first_name,
                            "gender": item.gender,
                            "image_file": item.image_file,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            students = User.objects(role=role,is_activate=True,email__istartswith=key_word).limit(5)
            if students:  
                for item in students: 
                    flag = False
                    for ele in data:
                        if ele['id'] == item.id:
                            flag = True
                            break
                    if flag == False:        
                        ele = {
                            "id": str(item.id),
                            "address": item.address,
                            "birth": item.birth.strftime("%m-%d-%Y"),
                            "email": item.email,
                            "first_name": item.first_name,
                            "gender": item.gender,
                            "image_file": item.image_file,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            response = {
                'status':True,
                'message':'Get Students Success',
                'data':data
            } 
    else:
        response = {
            'status':False,
            'message':'Get Students Failed',
            'data': None
        } 
    return response 

@student.route("/student/update_reciept/<string:id>", methods=['GET', 'POST']) 
@login_required
def update_receipt(id): 
    activate = list(range(10))
    activate[1] = "active"
    if current_user.is_authenticated:    
        receipt = TuitionReceipt.objects(id=id).first()  
        form = UpdateStudentToClass()  
        if id is None or receipt is None:
            return redirect(url_for('student.index'))  
    
        if form.validate_on_submit(): 
            next_tuition = float(form.next_pay.data)

            reservate_tuition = float(form.reservate_tuition.data)
            tuition_left = receipt.course.tuition - (reservate_tuition + next_tuition)

            print(receipt.course.tuition,reservate_tuition,next_tuition,tuition_left)
            money_return = 0
            status = False
            if tuition_left <= 0:
                status = True 
                money_return = -1* tuition_left 
                tuition_left = 0

            detail_receipt = DetailTuitionReceipt(tuition=next_tuition,money_return=money_return,created_user=current_user.user).save()
            receipt.list_detail.append(detail_receipt)
            receipt.tuition_left = tuition_left
            receipt.reservate_tuition = reservate_tuition + next_tuition
            receipt.status = status
            receipt.updated_date = datetime.utcnow()
            receipt.save()
            flash('Receipt has been updated!', 'success')
            return redirect(url_for('student.student_info',id=receipt.student.id))
        
        form.first_name.data = receipt.student.first_name
        form.last_name.data = receipt.student.last_name
        form.phone.data = receipt.student.phone
        form.email.data = receipt.student.email
        form.address.data = receipt.student.address
        form.birth.data = receipt.student.birth  
        form.gender.data = receipt.student.gender 
        form.reservate_tuition.data = receipt.reservate_tuition
        form.course.data = receipt.course.id_course
        form.course_name.data = receipt.course.name
        form.shift.data = receipt.course.shift.name
        form.course_tuition.data = receipt.course.tuition  
        form.money_return.data = 0 
        
        return render_template('student_update_receipt.html', title='Update Student\'s Receipt',activate=activate, receipt= receipt,form=form)
    return redirect(url_for('users.login'))

@student.route("/student/create", methods=['GET', 'POST']) 
@login_required
def create(): 
    activate = list(range(10))
    activate[1] = "active"   
    form = UpdateUserForm()    
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image_file = picture_file
        first_name=form.first_name.data 
        last_name=form.last_name.data 
        phone =form.phone.data 
        email =form.email.data
        address =form.address.data
        birth =form.birth.data 
        gender = form.gender.data  
        role = Role.objects(name='student').first()
        user = User(first_name=first_name,last_name=last_name,phone=phone,email=email,address=address,birth=birth,gender=gender,role=role)
        user.save()
        flash('Student has been created!', 'success')
        return redirect(url_for('student.student_info',id=user.id)) 
    return render_template('student_create.html', title='Create Student\'s Info',activate=activate,form=form)
    
 

@student.route("/student/remove/<string:id>", methods=['GET']) 
@login_required
def remove(id): 
    activate = list(range(10))
    activate[1] = "active"  
    role = Role.objects(name="student").first()
    student = User.objects(role=role,id=id,is_activate=True).first()
    if student:
        receipts = TuitionReceipt.objects(student=student)
        if len(receipts) > 0:
            flash('Student can\'t remove !!', 'danger')
            return redirect(url_for('student.student_info',id=student.id)) 
        student.is_activate = False
        student.save()
        flash('Student delete success !!', 'success')
    return redirect(url_for('student.index',page=1))
 

@student.route("/student/removed/<string:page>") 
@login_required
def student_removed(page):    
    activate = list(range(10))
    activate[1] = "active"
    page = int(page) 
    role = Role.objects(name='student').first()
    if page is None or page == 1:
        page = request.args.get('page', 1, type=int) 
        students = User.objects(role=role,is_activate=False).limit(10) 
    elif page <= -1:
        page = int((User.objects(role=role,is_activate=False).count()-10) /10) + 2   
        num_skip= User.objects(role=role).count()-10
        if num_skip < 0: num_skip = 0
        students = User.objects(role=role,is_activate=False).skip(num_skip)
    else:
        students = User.objects(role=role,is_activate=False).skip(page*10-10).limit(10)  
    return render_template('student_removed.html', title='Removed Student',activate=activate,students=students,page_num=page)

@student.route("/student/restore/<string:id>", methods=['GET']) 
@login_required
def restore(id): 
    activate = list(range(10))
    activate[1] = "active"  
    role = Role.objects(name="student").first()
    student = User.objects(role=role,id=id,is_activate=False).first() 
    if student: 
        student.is_activate = True
        student.save()
        flash('Student restore success !!', 'success')  
        return redirect(url_for('student.student_removed',page=1))
    else:
        flash('Student with id ' + id+ ' can\'t find  !!', 'danger')
    return redirect(url_for('student.student_removed',page=1))


@student.route("/api/student/get_remove/<string:key_word>", methods=['GET', 'POST']) 
@login_required
def get_removed_student(key_word):  
    if current_user.is_authenticated:
        data = list()    
        role = Role.objects(name='student').first()
        if key_word == 'all':
            students = User.objects(role=role,is_activate=False).limit(10)
            if students:  
                for item in students:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "phone": item.phone,
                        "is_activate": item.is_activate
                    } 
                    data.append(ele)
                response = {
                    'status':True,
                    'message':'Get Students Success',
                    'data':data
                }  
        else:
            students = User.objects(role=role,is_activate=False,first_name__istartswith=key_word).limit(5) 
            if students:  
                for item in students:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "phone": item.phone,
                        "is_activate": item.is_activate
                    } 
                    data.append(ele)

            students = User.objects(role=role,is_activate=False,last_name__istartswith=key_word).limit(5)
            if students:  
                for item in students: 
                    flag = False
                    for ele in data:
                        if ele['id'] == item.id:
                            flag = True
                            break
                    if flag == False:        
                        ele = {
                            "id": str(item.id),
                            "address": item.address,
                            "birth": item.birth.strftime("%m-%d-%Y"),
                            "email": item.email,
                            "first_name": item.first_name,
                            "gender": item.gender,
                            "image_file": item.image_file,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            students = User.objects(role=role,is_activate=False,phone__istartswith=key_word).limit(5)
            if students:  
                for item in students: 
                    flag = False
                    for ele in data:
                        if ele['id'] == item.id:
                            flag = True
                            break
                    if flag == False:        
                        ele = {
                            "id": str(item.id),
                            "address": item.address,
                            "birth": item.birth.strftime("%m-%d-%Y"),
                            "email": item.email,
                            "first_name": item.first_name,
                            "gender": item.gender,
                            "image_file": item.image_file,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            students = User.objects(role=role,is_activate=False,email__istartswith=key_word).limit(5)
            if students:  
                for item in students: 
                    flag = False
                    for ele in data:
                        if ele['id'] == item.id:
                            flag = True
                            break
                    if flag == False:        
                        ele = {
                            "id": str(item.id),
                            "address": item.address,
                            "birth": item.birth.strftime("%m-%d-%Y"),
                            "email": item.email,
                            "first_name": item.first_name,
                            "gender": item.gender,
                            "image_file": item.image_file,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            response = {
                'status':True,
                'message':'Get Students Success',
                'data':data
            } 
    else:
        response = {
            'status':False,
            'message':'Get Students Failed',
            'data': None
        } 
    return response 
