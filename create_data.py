import os
import urllib.parse
from mongoengine import *
from it_center.models import User, Account, Role, Course, Shift
import json
import random 
import datetime 
from it_center import bcrypt

def connect_db():
  MONGODB_DB = urllib.parse.quote_plus("it_center")
  MONGODB_USERNAME = urllib.parse.quote_plus('tamaki')
  MONGODB_PASSWORD = urllib.parse.quote_plus('mushroomzz99')
  MONGODB_HOST = 'mongodb+srv://%s:%s@cluster0-qz9ip.mongodb.net/%s?retryWrites=true' % (MONGODB_USERNAME, MONGODB_PASSWORD,MONGODB_DB)
  connect(username='tamaki', password='mushroomzz99', authentication_source='admin', host=MONGODB_HOST)

def create_data_role():
  Role(name="admin").save()
  Role(name="academic").save()
  Role(name="cashier").save()
  Role(name="student").save()
  Role(name="teacher").save()

def create_data_user(num_admin=2,num_academic=5,num_cashier=5,num_teacher=10):  
  num=0
  with open('it_center/data/user.json') as f:
    list_user = json.load(f)   
    roles = ["admin","academic","cashier","teacher","student"]
    ro = dict()
    num_role = 4
    for item in list_user:
      if ro.get('admin') and ro.get('admin') == num_admin: 
        num_admin = 0
        roles.pop(roles.index('admin'))
        num_role-=1
      if ro.get('academic') and ro['academic'] == num_academic: 
        num_academic = 0
        roles.pop(roles.index('academic'))
        num_role-=1
      if ro.get('cashier') and ro['cashier'] == num_cashier: 
        num_cashier=0
        roles.pop(roles.index('cashier'))
        num_role-=1
      if ro.get('teacher') and ro['teacher'] == num_teacher: 
        num_teacher=0
        roles.pop(roles.index('teacher'))
        num_role-=1
      num = random.randint(0, num_role) 
      if ro.get(roles[num]):
        count = ro[roles[num]] + 1
      else:
        count = 1 
      ro[roles[num]] = count
      role = Role.objects(name=roles[num]).first()
      birth = datetime.datetime.strptime(item['birth']['$date'], '%Y-%m-%dT%H:%M:%S.%fZ')
      if role:
        num +=1 
        User(first_name=item['first_name'],last_name=item['last_name'],email=item['email'],phone=item['phone'],role=role,birth=birth,address=item['address'],gender=item['gender'],image_file=item['image_file']).save()
  print("create success",num,"data user")

def create_data_account():
  role_admin = Role.objects(name="admin").first()
  role_academic = Role.objects(name="academic").first()
  role_cashier = Role.objects(name="cashier").first()

  list_admin = User.objects(role=role_admin)
  list_academic = User.objects(role=role_academic)
  list_cashier = User.objects(role=role_cashier)
  
  hashed_password = bcrypt.generate_password_hash("1").decode('utf-8') 

  num = 1 
  for item in list_admin:
    Account(username="admin"+str(num),password=hashed_password,user=item).save()
    num+=1


  num = 1 
  for item in list_academic: 
    Account(username="academic"+str(num),password=hashed_password,user=item).save()
    num+=1

  num = 1 
  for item in list_cashier: 
    Account(username="cashier"+str(num),password=hashed_password,user=item).save()
    num+=1
 

def create_data_shift():
  Shift(name="2_4_6 - Shift 1",start="17:30",finish="19:30").save()
  Shift(name="2_4_6 - Shift 2",start="19:30",finish="21:30").save()
  Shift(name="3_5_7 - Shift 1",start="17:30",finish="19:30").save()
  Shift(name="3_5_7 - Shift 2",start="19:30",finish="21:30").save()

def create_data_course(): 
  role_teacher = Role.objects(name='teacher').first()
  list_teacher = User.objects(role=role_teacher)
  role_student = Role.objects(name='student').first()
  list_student = User.objects(role=role_student)
  list_shift = Shift.objects.all()
  Course(id_course="SD-001",name="Word - Excel - Power Point",tuition=120,teacher=list_teacher[0],shift=list_shift[0]).save()
  Course(id_course="DB-001",name="DataBase System",tuition=199,teacher=list_teacher[1],shift=list_shift[1]).save()
  Course(id_course="WEB-001",name="Web Interface",tuition=149,teacher=list_teacher[2],shift=list_shift[2]).save()
  Course(id_course="JAVA-001",name="Java Application",tuition=299,teacher=list_teacher[3],shift=list_shift[0]).save()
  Course(id_course="RJ-001",name="React - Redux JavaScript",tuition=289,teacher=list_teacher[4],shift=list_shift[2]).save()
 
#get all name of images in DATA_TRAIN_FOLDER
def get_images(path=None):
  files = []
  exts = ['jpg', 'png', 'jpeg', 'JPG']
  for parent, dirnames, filenames in os.walk(path):
      for filename in filenames:
          for ext in exts:
              if filename.endswith(ext):
                  files.append(filename)
                  break
  print('Find {} images'.format(len(files)))
  return files

def create_avatar_availible():
  file_names= get_images(path="it_center/static/profile_pics")
  list_user = User.objects.all()
  for item in list_user:
    item.image_file = file_names[random.randint(0, len(file_names)-1)]
    item.save()
  
# connect_db()
# create_data_role()
# create_data_user(num_admin=2,num_academic=5,num_cashier=5,num_teacher=5)
# create_data_account() 
# create_data_shift() 
# create_data_course() 
# create_avatar_availible()