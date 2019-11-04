from flask import request, render_template, Blueprint,abort,flash,redirect,url_for
import json, os
from it_center.models import User, Account,Role, Course,TuitionReceipt,DetailTuitionReceipt,PaymentReceipt
from it_center import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from it_center.users.utils import save_picture, send_reset_email, verify_login  
from it_center.users.forms import UpdateUserForm
from it_center.teacher.forms import PaymentReceiptForm,UpdateTeacherForm 
from datetime import datetime

teacher = Blueprint('teacher', __name__)

@teacher.route("/teacher/<string:page>") 
@login_required
def index(page):  
    activate = list(range(10))
    activate[2] = "active"
    page = int(page) 
    role = Role.objects(name='teacher').first()
    if page is None or page == 1:
        page = request.args.get('page', 1, type=int) 
        teachers = User.objects(role=role,is_activate=True).limit(10) 
    elif page <= -1:
        page = int((User.objects(role=role,is_activate=True).count()-10) /10) + 2   
        num_skip= User.objects(role=role).count()-10
        if num_skip < 0: num_skip = 0
        teachers = User.objects(role=role,is_activate=True).skip(num_skip)
    else:
        teachers = User.objects(role=role,is_activate=True).skip(page*10-10).limit(10)  
    return render_template('teacher.html', title='Teacher',activate=activate,teachers=teachers,page_num=page)

@teacher.route("/teacher/info/<string:id>", methods=['GET', 'POST']) 
@login_required
def teacher_info(id):  
    if current_user.user.role.name != 'admin' and current_user.user.role.name != 'academic': 
        flash('You\'re not authorization.')
        return redirect(url_for('main.index'))
    activate = list(range(10))
    activate[2] = "active"
    is_activate = True
    if current_user.is_authenticated: 
        user = User.objects(id=id,is_activate=True).first()  
        form = UpdateTeacherForm()  
        if id is None or user is None:
            return redirect(url_for('teacher.index',page=1))   
        print(form.validate_on_submit())
        if form.validate_on_submit():
            print(123)
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                user.image_file = picture_file
            print(123)
            user.first_name=form.first_name.data 
            user.last_name=form.last_name.data 
            user.phone =form.phone.data 
            user.email =form.email.data
            user.salary =form.salary.data
            user.address =form.address.data
            user.birth =form.birth.data 
            user.gender = form.gender.data   
            if user.role.name != 'teacher': 
                flash('Can\'t find role, please reload page', 'danger')
                return redirect(url_for('teacher.teacher_info',id=id))
          
            user.save()
            flash('Teacher has been updated!', 'success')
            return redirect(url_for('teacher.teacher_info',id=id))
        else:
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.phone.data = user.phone
            form.email.data = user.email
            form.salary.data = user.salary
            form.address.data = user.address 
            form.gender.data = user.gender 
            form.birth.data = user.birth 
        receipts = PaymentReceipt.objects(staff=user)  
        return render_template('teacher_info.html', title='Teacher Info',activate=activate,teacher=user,form=form,receipts=receipts)
    return redirect(url_for('teacher.index',page=1))

@teacher.route("/teacher/create_reciept/<string:id>", methods=['GET', 'POST']) 
@login_required
def create_receipt(id): 
    activate = list(range(10))
    activate[2] = "active"     
    user = User.objects(id=id,is_activate=True).first()  
    form = PaymentReceiptForm()  
    if id is None or user is None:
        return redirect(url_for('teacher.index'))  

    if form.validate_on_submit():
        staff = user
        money = float(form.payment.data)
        basic_salary = user.salary
        from_date = form.from_date.data
        to_date = form.to_date.data
        created_user = current_user.user 
        receipt = PaymentReceipt(staff=staff,money=money,basic_salary=basic_salary,from_date=from_date,to_date=to_date,created_user=created_user)
        receipt.save()
        flash('Receipt has been created!', 'success')
        return redirect(url_for('teacher.teacher_info',id=id))
    
    print(user.gender )
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.phone.data = user.phone
    form.email.data = user.email
    form.address.data = user.address
    form.birth.data = user.birth  
    form.address.data = user.address
    form.birth.data = user.birth  
    form.gender.data = user.gender 
    form.role.data = user.role.name 
    form.salary.data = user.salary 
    form.payment.data = 0  
    return render_template('teacher_create_receipt.html', title='Create Payment Teacher',activate=activate,teacher=user,form=form)

@teacher.route("/api/teacher/get/<string:key_word>", methods=['GET', 'POST']) 
@login_required
def get_teacher(key_word):  
    if current_user.is_authenticated:
        data = list()    
        role = Role.objects(name='teacher').first()
        if key_word == 'all':
            teachers = User.objects(role=role,is_activate=True).limit(10)
            if teachers:  
                for item in teachers:
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
                    'message':'Get Teachers Success',
                    'data':data
                }  
        else:
            teachers = User.objects(role=role,is_activate=True,first_name__istartswith=key_word).limit(5) 
            if teachers:  
                for item in teachers:
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

            teachers = User.objects(role=role,is_activate=True,last_name__istartswith=key_word).limit(5)
            if teachers:  
                for item in teachers: 
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
            teachers = User.objects(role=role,is_activate=True,phone__istartswith=key_word).limit(5)
            if teachers:  
                for item in teachers: 
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
            teachers = User.objects(role=role,is_activate=True,email__istartswith=key_word).limit(5)
            if teachers:  
                for item in teachers: 
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
                'message':'Get Teachers Success',
                'data':data
            } 
    else:
        response = {
            'status':False,
            'message':'Get Teachers Failed',
            'data': None
        } 
    return response 
 
@teacher.route("/teacher/create", methods=['GET', 'POST']) 
@login_required
def create(): 
    activate = list(range(10))
    activate[2] = "active"   
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
        role = Role.objects(name='teacher').first()
        user = User(first_name=first_name,last_name=last_name,phone=phone,email=email,address=address,birth=birth,role=role,gender=gender)
        user.save()
        flash('Teacher has been created!', 'success')
        return redirect(url_for('teacher.teacher_info',id=user.id)) 
    return render_template('teacher_create.html', title='Create Teacher\'s Info',activate=activate,form=form)
    
 

@teacher.route("/teacher/remove/<string:id>", methods=['GET']) 
@login_required
def remove(id): 
    activate = list(range(10))
    activate[2] = "active"  
    role = Role.objects(name="teacher").first()
    teacher = User.objects(role=role,id=id,is_activate=True).first()
    if teacher:
        receipts = PaymentReceipt.objects(staff=teacher)
        if len(receipts) > 0:
            flash('Teacher can\'t remove !!', 'danger')
            return redirect(url_for('teacher.teacher_info',id=teacher.id)) 
        teacher.is_activate = False
        teacher.save()
        flash('Teacher delete success !!', 'success')
    return redirect(url_for('teacher.index',page=1))
 

@teacher.route("/teacher/removed/<string:page>") 
@login_required
def teacher_removed(page):    
    activate = list(range(10))
    activate[2] = "active"
    page = int(page) 
    role = Role.objects(name='teacher').first()
    if page is None or page == 1:
        page = request.args.get('page', 1, type=int) 
        teachers = User.objects(role=role,is_activate=False).limit(10) 
    elif page <= -1:
        page = int((User.objects(role=role,is_activate=False).count()-10) /10) + 2   
        num_skip= User.objects(role=role).count()-10
        if num_skip < 0: num_skip = 0
        teachers = User.objects(role=role,is_activate=False).skip(num_skip)
    else:
        teachers = User.objects(role=role,is_activate=False).skip(page*10-10).limit(10)  
    return render_template('teacher_removed.html', title='Removed Teacher',activate=activate,teachers=teachers,page_num=page)

@teacher.route("/teacher/restore/<string:id>", methods=['GET']) 
@login_required
def restore(id): 
    activate = list(range(10))
    activate[2] = "active"  
    role = Role.objects(name="teacher").first()
    teacher = User.objects(role=role,id=id,is_activate=False).first() 
    if teacher: 
        teacher.is_activate = True
        teacher.save()
        flash('Teacher restore success !!', 'success')  
        return redirect(url_for('teacher.teacher_removed',page=1))
    else:
        flash('Teacher with id ' + id+ ' can\'t find  !!', 'danger')
    return redirect(url_for('teacher.teacher_removed',page=1))


@teacher.route("/api/teacher/get_remove/<string:key_word>", methods=['GET', 'POST']) 
@login_required
def get_removed_teacher(key_word):  
    if current_user.is_authenticated:
        data = list()    
        role = Role.objects(name='teacher').first()
        if key_word == 'all':
            teachers = User.objects(role=role,is_activate=False).limit(10)
            if teachers:  
                for item in teachers:
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
                    'message':'Get Teachers Success',
                    'data':data
                }  
        else:
            teachers = User.objects(role=role,is_activate=False,first_name__istartswith=key_word).limit(5) 
            if teachers:  
                for item in teachers:
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

            teachers = User.objects(role=role,is_activate=False,last_name__istartswith=key_word).limit(5)
            if teachers:  
                for item in teachers: 
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
            teachers = User.objects(role=role,is_activate=False,phone__istartswith=key_word).limit(5)
            if teachers:  
                for item in teachers: 
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
            teachers = User.objects(role=role,is_activate=False,email__istartswith=key_word).limit(5)
            if teachers:  
                for item in teachers: 
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
                'message':'Get Teachers Success',
                'data':data
            } 
    else:
        response = {
            'status':False,
            'message':'Get Teachers Failed',
            'data': None
        } 
    return response 
