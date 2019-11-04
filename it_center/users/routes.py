from flask import request, render_template, Blueprint,abort,flash,redirect,url_for
import json, os
from it_center.models import User, Account,PaymentReceipt
from it_center import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from it_center.users.utils import save_picture, send_reset_email, verify_login 
from it_center.users.forms import LoginForm, UpdateUserForm, RequestResetForm, ResetPasswordForm

users = Blueprint('users', __name__)
 
@users.route('/login', methods=['GET', 'POST'])
def login():      
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit(): 
        account = Account.objects(username=form.username.data).first()  
        if account and account.user.is_activate is False:
            flash('Login unsuccessful, because you are not belong to system. Please contact admin', 'danger')
        elif account and account.user.is_activate and bcrypt.check_password_hash(account.password, form.password.data):
            login_user(account, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.index')) 
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/profile', methods=['GET', 'POST']) 
@login_required
def profile():   
    activate = list(range(10))
    activate[7] = "active"   
    form = UpdateUserForm() 
    if form.validate_on_submit(): 
        user = User.objects(id=current_user.user.id,is_activate=True).first()
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.user.image_file = picture_file
        current_user.user.first_name=form.first_name.data 
        current_user.user.last_name=form.last_name.data 
        current_user.user.phone =form.phone.data 
        current_user.user.email =form.email.data
        current_user.user.address =form.address.data
        current_user.user.birth =form.birth.data 
        current_user.user.gender = form.gender.data  
        current_user.user.save()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.profile'))
    elif request.method == 'GET':
        form.first_name.data = current_user.user.first_name
        form.last_name.data = current_user.user.last_name
        form.phone.data = current_user.user.phone
        form.email.data = current_user.user.email
        form.address.data = current_user.user.address
        form.birth.data = current_user.user.birth 
        form.gender.data = current_user.user.gender   
    image_file = current_user.user.image_file 
    error = False
    if form.first_name.errors or form.last_name.errors or form.phone.errors or form.email.errors or form.address.errors or form.birth.errors or form.gender.errors:
        error = True
    receipts = ""
    if current_user.user.role.name !='admin' and current_user.user.role.name !='student' and current_user.user.role.name !='teacher':
        receipts = PaymentReceipt.objects(staff=current_user.user) 
    return render_template('profile.html', title='Profile',
                        image_file=image_file,form=form,activate=activate,error=error,receipts=receipts)

@users.route("/logout")
@login_required
def logout():
    if current_user.is_authenticated: 
        logout_user() 
        return redirect(url_for('users.login'))
    return render_template('index.html')


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request(): 
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        account = Account.objects(user=user).first()
        if user and account and account.is_activate:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
            return redirect(url_for('users.login'))
        elif user and account and account.is_activate == False:
            flash('You haven\'t login yet. Please contact admin to get more info.', 'info')
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):  
    user = User.verify_reset_token(token) 
    account = Account.objects(user=user).first() 
    if user is None or account is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') 
        account.password = hashed_password
        user.is_confirmed = True
        account.is_activate = True
        user.save()
        account.save()  
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form) 

