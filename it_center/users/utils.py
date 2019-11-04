import os
import secrets
import requests

from PIL import Image
from flask import current_app,url_for 
from flask_mail import Message 
from io import BytesIO
from it_center import mail 
from it_center.models import User,Account

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = User.get_reset_token(user=user)
    msg = Message('Password Reset Request',
                 sender='noreply@demo.com',
                 recipients=[user.email])
    msg.body = f'''To reset your password, visit following link: 
              {url_for('users.reset_token', token= token, _external= True)}
                If you did not make request then simply ignore this email and no changes will be made.
                '''
    mail.send(msg)

def check_token(token):
    # token = request.get_json()['token']  
    if verify_login(token):   
        return json.dumps(Respone(True, {}, "Authorized"))
    return json.dumps(Respone(False, {}, "Unauthorized"))

def verify_login(token):
    user = Account.verify_login_token(token)   
    if user is None: 
        return False
    return True
