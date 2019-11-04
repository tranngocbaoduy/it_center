from flask import request, render_template, Blueprint,abort,flash,redirect,url_for
import json, os
from it_center.models import User, Account,Role, TuitionReceipt,PaymentReceipt
from it_center import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from it_center.users.utils import save_picture, send_reset_email, verify_login 
from it_center.staff.forms import UpdateStaffForm, CreateStaffForm, PaymentReceiptForm
from fuzzywuzzy import fuzz

staff = Blueprint('staff', __name__)
 
@staff.route('/staff/<string:page>', methods=['GET', 'POST'])
@login_required
def index(page):       
    if current_user.user.role.name != 'admin': 
        flash('You\'re not admin. You can not access this page')
        return redirect(url_for('main.index'))
    activate = list(range(10))
    activate[4] = "active"  
    page = int(page) 
    role_academic = Role.objects(name='academic').first()
    role_cashier = Role.objects(name='cashier').first()
    if page is None or page == 1:
        page = request.args.get('page', 1, type=int) 
        users_1 = User.objects(role=role_academic,is_activate=True).limit(5) 
        users_2 = User.objects(role=role_cashier,is_activate=True).limit(5) 
    elif page <=-1:
        page = int((User.objects(role=role,is_activate=True).count()-10) /10) + 2   
        num_skip= User.objects(role=role).count()-5
        if num_skip < 0: num_skip = 0
        users_1 = User.objects(role=role_academic,is_activate=True).skip(num_skip)
        users_2 = User.objects(role=role_cashier,is_activate=True).skip(num_skip)
    else:
        users_1 = User.objects(role=role_academic,is_activate=True).skip(page*5-5).limit(5)
        users_2 = User.objects(role=role_cashier,is_activate=True).skip(page*5-5).limit(5)  
     
    users = list()
    for item in users_1:
        users.append(item)

    for item in users_2:
        users.append(item) 
    return render_template('staff.html', title='Staff',activate=activate,users=users,page_num=page)  
    
@staff.route("/staff/info/<string:id>", methods=['GET', 'POST']) 
@login_required
def staff_info(id):  
    if current_user.user.role.name != 'admin': 
        flash('You\'re not admin. You can not access this page')
        return redirect(url_for('main.index'))
    activate = list(range(10))
    activate[4] = "active"
    is_activate = True
    if current_user.is_authenticated:
        user = User.objects(id=id,is_activate=True).first()  
        form = UpdateStaffForm()  
        if id is None or user is None:
            return redirect(url_for('staff.index',page=1))  
        if form.validate_on_submit():
            if form.picture.data:
                picture_file = save_picture(form.picture.data)
                user.image_file = picture_file
            user.first_name=form.first_name.data 
            user.last_name=form.last_name.data 
            user.phone =form.phone.data 
            user.email =form.email.data
            user.salary =form.salary.data
            user.address =form.address.data
            user.birth =form.birth.data 
            user.gender = form.gender.data  
            role = form.role.data
            if role == 'cashier' or role == 'academic':
                role = Role.objects(name=role).first()
                # print(role.name)  
                user.role = role
                # print(user.role.id,role.id)
            else:  
                flash('Can\'t find role, please reload page', 'danger')
                return redirect(url_for('staff.staff_info',id=id))
                
            user.save()
            flash('Staff has been updated!', 'success')
            return redirect(url_for('staff.staff_info',id=id))
        elif request.method == 'GET':
            form.first_name.data = user.first_name
            form.last_name.data = user.last_name
            form.phone.data = user.phone
            form.email.data = user.email
            form.salary.data = user.salary
            form.address.data = user.address 
            form.gender.data = user.gender 
            form.birth.data = user.birth
            form.role.data = user.role 
        receipts = PaymentReceipt.objects(staff=user)
        account = Account.objects(user=user).first()
        if account and account.is_activate == False:
            flash('Account of staff hasn\'t been acitved yet !!', 'info')  
            is_activate = False
        return render_template('staff_info.html', title='Staff Info',activate=activate,staff=user,form=form,receipts=receipts,is_activate = is_activate)
    return redirect(url_for('staff.index',page=1))
   

@staff.route("/staff/create", methods=['GET', 'POST']) 
@login_required
def create():  
    if current_user.user.role.name != 'admin': 
        flash('You\'re not admin. You can not access this page')
        return redirect(url_for('main.index'))
    activate = list(range(10))
    activate[4] = "active"  
    form = CreateStaffForm()  
    image_file = ""
    if id is None:
        return redirect(url_for('staff.index',page=1))

    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            image_file = picture_file
        first_name=form.first_name.data 
        last_name=form.last_name.data 
        phone =form.phone.data
        salary = form.salary.data 
        email =form.email.data
        address =form.address.data
        birth =form.birth.data 
        gender = form.gender.data  
        if form.role.data == 'cashier' or form.role.data == 'academic' or form.role.data == 'admin':
            role = Role.objects(name=form.role.data).first() 
        else:  
            flash('Can\'t find role, please reload page', 'danger')
            return redirect(url_for('staff.create'))
        if image_file == "":
            user = User(first_name=first_name,last_name=last_name,phone=phone,email=email,gender=gender,address=address,birth=birth,role=role,image_file=image_file,salary=salary).save()
        else:
            user = User(first_name=first_name,last_name=last_name,phone=phone,email=email,gender=gender,address=address,birth=birth,role=role,salary=salary).save()
        account = Account(username=phone,password="1",user=user,is_activate=False).save()
        send_reset_email(user)  
        flash('Staff has been created! Your account is also created, please use phone to login to system. Verify is sending to your gmail, please wait a few minutes. Within 3 hour, you must login to system to change your new password', 'success')
        return redirect(url_for('staff.staff_info',id=user.id)) 
    return render_template('staff_create.html', title='Staff Create Staff\'s Info',activate=activate,form=form)


@staff.route("/staff/send_active/<string:id>", methods=['GET']) 
@login_required
def send_active_again(id): 
    if current_user.user.role.name != 'admin': 
        flash('You\'re not admin. You can not access this page')
        return redirect(url_for('main.index'))
    activate = list(range(10))
    activate[4] = "active"  
    user = User.objects(id=id).first()  
    if id is None or user is None:
        flash("Can't find this id !!!","info")
        return redirect(url_for('staff.index',page=1))
    send_reset_email(user)  
    flash('Activate is sent, this command is effectived within 30 minutes please active now', 'success')
    return redirect(url_for('staff.staff_info',id=user.id)) 

@staff.route("/staff/remove/<string:id>", methods=['GET']) 
@login_required
def remove(id): 
    activate = list(range(10))
    activate[4] = "active"  
    role = Role.objects(name="staff").first()
    staff = User.objects(id=id,is_activate=True).first()
    account = Account.objects(user=staff).first()
    
    if staff and account:
        TuitionReceipts = TuitionReceipt.objects(student=staff)
        if len(TuitionReceipts) > 0:
            flash('Staff can\'t remove !!', 'danger')
            return redirect(url_for('staff.staff_info',id=staff.id)) 
        staff.is_activate = False 
        account.is_activate = False
        staff.save()  
        account.save()
        flash('Staff delete success !!', 'success') 
        return redirect(url_for('staff.index',page=1))
    flash('Can\'t find staff !!', 'danger')
    return redirect(url_for('staff.index',page=1))

@staff.route("/staff/removed/<string:page>") 
@login_required
def staff_removed(page):    
    if current_user.user.role.name != 'admin': 
        flash('You\'re not admin. You can not access this page')
        return redirect(url_for('main.index'))
    activate = list(range(10))
    activate[4] = "active"  
    page = int(page) 
    role_academic = Role.objects(name='academic').first()
    role_cashier = Role.objects(name='cashier').first() 
    if page is None or page == 1:
        page = request.args.get('page', 1, type=int) 
        users_1 = User.objects(role=role_academic,is_activate=False).limit(5) 
        users_2 = User.objects(role=role_cashier,is_activate=False).limit(5) 
        print(users_2)
    elif page <=-1:
        page = int((User.objects(role=role,is_activate=False).count()-10) /10) + 2  
        num_skip= User.objects(role=role).count()-5
        if num_skip < 0: num_skip = 0
        users_1 = User.objects(role=role_academic,is_activate=False).skip(num_skip)
        users_2 = User.objects(role=role_cashier,is_activate=False).skip(num_skip)
    else:
        users_1 = User.objects(role=role_academic,is_activate=False).skip(page*5-5).limit(5)
        users_2 = User.objects(role=role_cashier,is_activate=False).skip(page*5-5).limit(5)  
     
    users = list()
    for item in users_1:
        users.append(item)

    for item in users_2:
        users.append(item)  
    return render_template('staff_removed.html', title='Staff',activate=activate,staffs=users,page_num=page)  

@staff.route("/staff/restore/<string:id>", methods=['GET']) 
@login_required
def restore(id): 
    activate = list(range(10))
    activate[4] = "active"     
    staff = User.objects(id=id,is_activate=False).first() 
    account = Account.objects(user=staff).first()
    if staff: 
        staff.is_activate = True
        account.is_activate = True
        staff.save()
        account.save()
        flash('Staff restore success !!', 'success')  
        return redirect(url_for('staff.staff_removed',page=1))
    else:
        flash('Student with id ' + id+ ' can\'t find  !!', 'danger')
    return redirect(url_for('staff.staff_removed',page=1))


@staff.route("/staff/inactived/<string:page>") 
@login_required
def staff_inactived(page):    
    if current_user.user.role.name != 'admin': 
        flash('You\'re not admin. You can not access this page')
        return redirect(url_for('main.index'))
    activate = list(range(10))
    activate[4] = "active"  
    page = int(page) 
    role_academic = Role.objects(name='academic').first()
    role_cashier = Role.objects(name='cashier').first() 
    if page is None or page == 1:
        page = request.args.get('page', 1, type=int) 
        accounts = Account.objects(is_activate=False).limit(10)
    elif page <=-1:
        page = int((Account.objects(is_activate=False).count()-10) /10) + 2   
        accounts = Account.objects(is_activate=False).skip(Account.objects().count()-10) 
    else:
        accounts = Account.objects(is_activate=False).skip(page*10-10).limit(10) 
     
    users = list()
    for item in accounts: 
        users.append(item.user)
    return render_template('staff_inactived.html', title='Staff Inactive Yet',activate=activate,staffs=users,page_num=page)  


@staff.route("/staff/create_reciept/<string:id>", methods=['GET', 'POST']) 
@login_required
def create_receipt(id): 
    activate = list(range(10))
    activate[1] = "active"     
    user = User.objects(id=id,is_activate=True).first()  
    form = PaymentReceiptForm()  
    if id is None or user is None:
        return redirect(url_for('staff.index'))  
      
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
        return redirect(url_for('staff.staff_info',id=id))
    
    form.first_name.data = user.first_name
    form.last_name.data = user.last_name
    form.phone.data = user.phone
    form.email.data = user.email
    form.address.data = user.address
    form.birth.data = user.birth  
    form.address.data = user.address
    form.birth.data = user.birth    
    form.salary.data = user.salary 
    form.payment.data = 0
    
    return render_template('staff_create_receipt.html', title='Create Payment Staff',activate=activate,staff=user,form=form)



@staff.route("/api/staff/get/<string:key_word>", methods=['GET', 'POST']) 
@login_required
def get_staff(key_word):  
    if current_user.is_authenticated:
        data = list()    
        role_academic = Role.objects(name='academic').first()
        role_cashier = Role.objects(name='cashier').first()
        if key_word == 'all':
            staffs_academic = User.objects(role=role_academic,is_activate=True).limit(5)
            staffs_cashier = User.objects(role=role_cashier,is_activate=True).limit(5)
            if staffs_academic:  
                for item in staffs_academic:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "role": item.role.name,
                        "phone": item.phone,
                        "is_activate": item.is_activate
                    } 
                    data.append(ele)
            if staffs_cashier:  
                for item in staffs_cashier:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "role": item.role.name,
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
            staffs_academic = User.objects(role=role_academic,is_activate=True,first_name__istartswith=key_word).limit(3)
            staffs_cashier = User.objects(role=role_cashier,is_activate=True,first_name__istartswith=key_word).limit(3) 
            if staffs_academic:  
                for item in staffs_academic:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "role": item.role.name,
                        "phone": item.phone,
                        "is_activate": item.is_activate
                    } 
                    data.append(ele)
            if staffs_cashier:
                for item in staffs_cashier:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "role": item.role.name,
                        "phone": item.phone,
                        "is_activate": item.is_activate
                    } 
                    data.append(ele)
            staffs_academic = User.objects(role=role_academic,is_activate=True,last_name__istartswith=key_word).limit(3)
            staffs_cashier = User.objects(role=role_cashier,is_activate=True,last_name__istartswith=key_word).limit(3) 
             
            if staffs_academic:  
                for item in staffs_academic: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            if staffs_cashier:  
                for item in staffs_cashier: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
 
            staffs_academic = User.objects(role=role_academic,is_activate=True,phone__istartswith=key_word).limit(3)
            staffs_cashier = User.objects(role=role_cashier,is_activate=True,phone__istartswith=key_word).limit(3) 
             
            if staffs_academic:  
                for item in staffs_academic: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            if staffs_cashier:  
                for item in staffs_cashier: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele)  

            staffs_academic = User.objects(role=role_academic,is_activate=True,email__istartswith=key_word).limit(3)
            staffs_cashier = User.objects(role=role_cashier,is_activate=True,email__istartswith=key_word).limit(3) 
             
            if staffs_academic:  
                for item in staffs_academic: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            if staffs_cashier:  
                for item in staffs_cashier: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
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

@staff.route("/api/staff/get_removed/<string:key_word>", methods=['GET', 'POST']) 
@login_required
def get_removed_staff(key_word):  
    if current_user.is_authenticated:
        data = list()    
        role_academic = Role.objects(name='academic').first()
        role_cashier = Role.objects(name='cashier').first()
        if key_word == 'all':
            staffs_academic = User.objects(role=role_academic,is_activate=False).limit(5)
            staffs_cashier = User.objects(role=role_cashier,is_activate=False).limit(5)
            if staffs_academic:  
                for item in staffs_academic:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "role": item.role.name,
                        "phone": item.phone,
                        "is_activate": item.is_activate
                    } 
                    data.append(ele)
            if staffs_cashier:  
                for item in staffs_cashier:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "role": item.role.name,
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
            staffs_academic = User.objects(role=role_academic,is_activate=False,first_name__istartswith=key_word).limit(3)
            staffs_cashier = User.objects(role=role_cashier,is_activate=False,first_name__istartswith=key_word).limit(3) 
            if staffs_academic:  
                for item in staffs_academic:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "role": item.role.name,
                        "phone": item.phone,
                        "is_activate": item.is_activate
                    } 
                    data.append(ele)
            if staffs_cashier:
                for item in staffs_cashier:
                    ele = {
                        "id": str(item.id),
                        "address": item.address,
                        "birth": item.birth.strftime("%m-%d-%Y"),
                        "email": item.email,
                        "first_name": item.first_name,
                        "gender": item.gender,
                        "image_file": item.image_file,
                        "last_name": item.last_name,
                        "role": item.role.name,
                        "phone": item.phone,
                        "is_activate": item.is_activate
                    } 
                    data.append(ele)
            staffs_academic = User.objects(role=role_academic,is_activate=False,last_name__istartswith=key_word).limit(3)
            staffs_cashier = User.objects(role=role_cashier,is_activate=False,last_name__istartswith=key_word).limit(3) 
             
            if staffs_academic:  
                for item in staffs_academic: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            if staffs_cashier:  
                for item in staffs_cashier: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
 
            staffs_academic = User.objects(role=role_academic,is_activate=False,phone__istartswith=key_word).limit(3)
            staffs_cashier = User.objects(role=role_cashier,is_activate=False,phone__istartswith=key_word).limit(3) 
             
            if staffs_academic:  
                for item in staffs_academic: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            if staffs_cashier:  
                for item in staffs_cashier: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele)  

            staffs_academic = User.objects(role=role_academic,is_activate=False,email__istartswith=key_word).limit(3)
            staffs_cashier = User.objects(role=role_cashier,is_activate=False,email__istartswith=key_word).limit(3) 
             
            if staffs_academic:  
                for item in staffs_academic: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
                            "last_name": item.last_name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
            if staffs_cashier:  
                for item in staffs_cashier: 
                    flag = False
                    for ele in data:
                        if str(ele['id']) == str(item.id):
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
                            "role": item.role.name,
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

@staff.route("/api/staff/get_inactived/<string:key_word>", methods=['GET', 'POST']) 
@login_required
def get_inactived_staff(key_word):  
    if current_user.is_authenticated:
        data = list()  
        account_inactived = Account.objects(is_activate=False).all()  
        staff = list()  
        print(account_inactived)
        for item in account_inactived:
            if item.user.role.name == 'academic' or item.user.role.name == 'cashier':
                staff.append(item.user)  

        print(staff)
        if key_word == 'all': 
            if staff:  
                count = 0
                for item in staff:
                    if count < 10:
                        ele = {
                            "id": str(item.id),
                            "address": item.address,
                            "birth": item.birth.strftime("%m-%d-%Y"),
                            "email": item.email,
                            "first_name": item.first_name,
                            "gender": item.gender,
                            "image_file": item.image_file,
                            "last_name": item.last_name,
                            "role": item.role.name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele) 
                        count+=1
            response = {
                'status':True,
                'message':'Get Students Success',
                'data':data
            }  
        else: 
            if staff:  
                count = 0
                for item in staff: 
                    print(key_word.lower() in item.first_name.lower(),key_word.lower() ,item.first_name.lower())
                    if count < 3 and key_word.lower() in item.first_name.lower() :
                        ele = {
                            "id": str(item.id),
                            "address": item.address,
                            "birth": item.birth.strftime("%m-%d-%Y"),
                            "email": item.email,
                            "first_name": item.first_name,
                            "gender": item.gender,
                            "image_file": item.image_file,
                            "last_name": item.last_name,
                            "role": item.role.name,
                            "phone": item.phone,
                            "is_activate": item.is_activate
                        } 
                        data.append(ele)
                        count+=1 
                count = 0
                for item in staff:
                    if count < 3 and key_word.lower() in item.last_name.lower() : 
                        flag = False                      
                        for ele in data:
                            if str(ele['id']) == str(item.id):
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
                                "role": item.role.name,
                                "phone": item.phone,
                                "is_activate": item.is_activate
                            } 
                            data.append(ele)
                            count+=1 
                count = 0
                for item in staff:
                    if count < 3 and key_word.lower() in item.phone.lower() : 
                        flag = False                      
                        for ele in data:
                            if str(ele['id']) == str(item.id):
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
                                "role": item.role.name,
                                "phone": item.phone,
                                "is_activate": item.is_activate
                            } 
                            data.append(ele)
                            count+=1 
                count = 0
                for item in staff: 
                    if count < 3 and key_word.lower() in item.email.lower():
                        flag = False                       
                        for ele in data:
                            if str(ele['id']) == str(item.id):
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
                                "role": item.role.name,
                                "phone": item.phone,
                                "is_activate": item.is_activate
                            } 
                            data.append(ele)
                            count+=1 
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