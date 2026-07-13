from connections.extensions import session
from connections.models import Users, ApplicationForm
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from flask_mail import Message
import random
from flask import current_app


def register_new_user(username, password, name, email):
    uid = str(uuid.uuid4())
    hash_password = generate_password_hash(password)

    new_user = Users(userid=uid, username=username, password=hash_password, name=name, status="None", email_account=email)

    try:
        session.add(new_user)
        session.commit()
        return True
    except Exception as e:
        return False


#SEND THE CODE TO THE USERS GMAIL ACCOUNT
def send_auth_code(email, code):
    mail = current_app.extensions['mail']
    msg = Message(f'WMSU Verification Code', recipients=[email])
    msg.body = f"Hello {email}!, This is your Verification Code for your WMSU Account! {code}"
    mail.send(msg)
    return True


#USED FOR GENERATING 6 LONG CODE FOR ACCOUNT VERIFICATION
def code_generator():
    choice = '1234567890'
    code = ''
    for i in range(6):
        num = random.choice(choice)
        code += num
    return code    

#ONLY USED AFTER A SUCCESSFUL REGISTRY
def get_user_id(username):
    result = session.query(Users).filter_by(username=username).first()
    id = result.userid
    return id


#CHECKS IF THE SESSION USERID IS VALID AND NOT TAMPERED
def verify_user(userid):
    result = session.query(Users).filter_by(userid=userid).first()

    if result:
        return True
    else:
        return False

def login(username, password):
    user = session.query(Users).filter_by(username=username).first()

    if check_password_hash(user.password, password):
        return True
    else:
        return False

  

