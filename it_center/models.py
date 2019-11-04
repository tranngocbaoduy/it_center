from it_center import db, login_manager
# from flask_mongoengien import BaseQueryQuerySetSet
from datetime import datetime
from flask import current_app
from flask_login import UserMixin, logout_user
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import json
# @login_manager.user_loader
# def loader_user(user_email): 
#     return User.objects.get(email=user_email) 
 
@login_manager.user_loader
def load_user(id):  
    return Account.objects(id=id).first() 

class JsonSerializable(object):
    def toJson(self):
        return json.dumps(self.__dict__)

    def __repr__(self):
        return self.toJson()
 
class Role(db.Document):
    name = db.StringField(max_length=25,required=True)
    is_activate = db.BooleanField(default=True)

class User(db.Document):
    first_name = db.StringField(max_length=1000,required=True, default="")
    last_name = db.StringField(max_length=100,required=True, default="")
    phone = db.StringField(max_length=15,required=True, default="")
    email = db.StringField(max_length=50,required=True, default="")
    address = db.StringField(max_length=200,required=True, default="")
    birth = db.DateTimeField(default = datetime.utcnow())
    gender = db.StringField(max_length=10,required=True, default="")
    image_file = db.StringField(max_length=200, default='avatar.jpg')
    status = db.BooleanField(default=True) 
    is_activate = db.BooleanField(default=True)
    salary = db.FloatField(default=0)
    role = db.ReferenceField(Role, required=True)  
    is_confirmed = db.BooleanField(default=False)
    created_date = db.DateTimeField(default = datetime.utcnow()) 

    def get_reset_token(user=None, expires_sec = 1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec) 
        return s.dumps({'user_id': str(user.id)}).decode('utf-8')
 
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        print(s)
        try: 
            user_id = s.loads(token)['user_id']
            user = User.objects(id=user_id).first() 
            if user.is_confirmed == True:
                return None
        except:
            return None 
        return user

class Account(db.Document, UserMixin,JsonSerializable):
    # query_class = UserModel  
    username = db.StringField(max_length=50,required=True)
    password = db.StringField(max_length=100,required=True)
    is_activate = db.BooleanField(default=True)
    user = db.ReferenceField(User, required=True)

    # get code token for reset password
    # @staticmethod
 
    def __repr__(self):
        return f"Account('{self.username}','{self.password}')" 

class Shift(db.Document):
    name = db.StringField(required=True,default="")
    start = db.StringField(required=True,default="")
    finish = db.StringField(required=True,default="")
    is_activate = db.BooleanField(default=True)
    created_date = db.DateTimeField(default = datetime.utcnow()) 


class Course(db.Document):
    id_course = db.StringField(required=True,default="")
    name = db.StringField(max_length=100,required=True, default="")
    start_date = db.DateTimeField(default = datetime.utcnow())
    finish_date = db.DateTimeField(default = datetime.utcnow())
    list_student = db.ListField(db.ReferenceField(User, default=[]))
    tuition = db.FloatField(default=0)
    teacher = db.ReferenceField(User)
    status = db.BooleanField(default=False)
    shift = db.ReferenceField(Shift,required=True)
    is_activate = db.BooleanField(default=True)
    created_date = db.DateTimeField(default = datetime.utcnow()) 

class DetailTuitionReceipt(db.Document):
    tuition = db.FloatField(default=0,required=True)
    money_return = db.FloatField(default=0,required=True)
    created_user = db.ReferenceField(User,required=True)
    created_date = db.DateTimeField(default = datetime.utcnow()) 

class TuitionReceipt(db.Document):
    student = db.ReferenceField(User,required=True)
    course = db.ReferenceField(Course,required=True)
    reservate_tuition = db.FloatField(default=0,required=True)
    tuition_left = db.FloatField(default=0,required=True)
    list_detail = db.ListField(db.ReferenceField(DetailTuitionReceipt,default=[]))
    status = db.BooleanField(default=False)
    is_activate = db.BooleanField(default=True)
    updated_date = db.DateTimeField(default = datetime.utcnow()) 
    created_date = db.DateTimeField(default = datetime.utcnow()) 

class PaymentReceipt(db.Document):
    staff = db.ReferenceField(User,required=True) 
    money = db.FloatField(default=0,required=True) 
    basic_salary = db.FloatField(default=0,required=True) 
    from_date = db.DateTimeField(default = datetime.utcnow())
    to_date = db.DateTimeField(default = datetime.utcnow())
    is_activate = db.BooleanField(default=True) 
    created_user = db.ReferenceField(User,required=True)
    created_date = db.DateTimeField(default = datetime.utcnow()) 