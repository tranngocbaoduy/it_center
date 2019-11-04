from flask import request, render_template, Blueprint, send_from_directory, current_app,redirect, url_for, abort, flash
from it_center.users.utils import verify_login
from flask_login import login_user, current_user, logout_user, login_required
from it_center.models import Course, PaymentReceipt, TuitionReceipt, Role, User
import json 
import os  
from datetime import datetime,date
main = Blueprint('main', __name__)
   
@main.route("/")
@main.route("/index") 

@login_required
def index():  
    if current_user.is_authenticated:  
        activate = list(range(10))
        activate[0] = "active"
        courses = Course.objects(start_date__gte=date.today()).limit(10) 
        now = date.today()
        return render_template('index.html', title="Dashboard",activate=activate,courses=courses,now=now) 
    return redirect(url_for('users.login')) 

@main.route("/finance")
@login_required
def finance(): 
    activate = list(range(10))
    activate[5] = "active"
    return render_template('finance.html', title='Finance',activate=activate)

@main.route("/statistic")
@login_required
def statistic(): 
    if current_user.user.role.name != 'admin': 
        flash('You\'re not admin. You can not access this page')
        return redirect(url_for('main.index'))
    activate = list(range(10))
    activate[6] = "active"
    legend = 'Monthly Payment Data'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August","September", "October","November", "December"]
    salaries = PaymentReceipt.objects.all()
    money_monthly = dict()
    payment_values = list()
    tuition_values = list()
    year = 2019 
    for i in range(1,13,1):
        money_monthly[i] = 0
    for key,value in money_monthly.items(): 
        for item in salaries:
            if item.created_date.month == key and item.created_date.year == year:  
                value = money_monthly[item.created_date.month]
                money_monthly[item.created_date.month] = item.money + value
 
    for i in list(money_monthly.items()):
        payment_values.append(i[1])

    for i in range(1,13,1):
        money_monthly[i] = 0
    tuitions = TuitionReceipt.objects.all() 
    for key,value in money_monthly.items(): 
        for item in tuitions:
            for element in item.list_detail:
                if element.created_date.month == key and element.created_date.year == year:  
                    value = money_monthly[element.created_date.month] 
                    money_monthly[element.created_date.month] = (element.tuition - element.money_return) + value   
    for i in list(money_monthly.items()):
        tuition_values.append(i[1]) 

    now = datetime.utcnow()
    role = Role.objects(name='student').first()
    student_in_system = User.objects(role=role).all()
    student_in_class = list()
    class_in_active = list()
    for item in tuitions: 
        if item.course.finish_date >= now and item.course.start_date <= now:
            if item.student in student_in_class:
                continue
            student_in_class.append(item.student)  

    class_in_system = Course.objects.all()
    for item in class_in_system:
        if item.finish_date >= now:
            class_in_active.append(item)
    now = datetime.utcnow() 
    print(payment_values,int(now.month))
    now_payment_values = payment_values[int(now.month)-1]
    now_tuition_values = tuition_values[int(now.month)-1]
    colors = ['#a991ff','#f48fff','#61ffdd','#00a879','#73ff9f','#ff6395','#ffcdbf','#7857ff','#b1b0b5','#362a69','#659476','#ffa578']
    return render_template('statistic.html', title='Statistic',activate=activate, now_payment_values=now_payment_values,now_tuition_values=now_tuition_values,payment_values=payment_values,tuition_values=tuition_values,colors=colors,labels=labels,now=now, legend=legend,class_in_system=class_in_system,class_in_active=class_in_active,student_in_class=student_in_class,student_in_system=student_in_system)
 
@main.route("/setting")  
@login_required
def setting(): 
    activate = list(range(10))
    activate[7] = "active"
    return render_template('setting.html', title='Setting',activate=activate)

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static/icon'),
                          'favicon.ico',mimetype='image/vnd.microsoft.icon')