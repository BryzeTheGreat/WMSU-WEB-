from flask import Blueprint, session, redirect, url_for, render_template, jsonify, request
from authentications.getdata.get_user_data import get_user_info, register_form

homepage = Blueprint('homepage', __name__)

@homepage.route('/home', methods=["POST", "GET"])
def main():
    user = session.get('userID')
    data = get_user_info(user)
    if not data:
        return redirect(url_for('homepage.logout'))

    return render_template('Homepage/homepage_main.html', data=data)

#GET DATA FROM JS TO REGISTER FORM
@homepage.route('/apply_form', methods=["POST", "GET"])
def apply_form():
    data = request.json

    firstname = data.get('firstname')
    middlename = data.get('middlename')
    lastname = data.get('lastname')
    contact_number = data.get('contact_number')
    mothersname = data.get('mothersname')
    fathersname = data.get('fathersname')
    guardian = data.get('guardian')
    sex = data.get('sex')
    age = data.get('age')
    province = data.get('province')
    city = data.get('city')
    barangay = data.get('barangay')
    college = data.get('college')
    course = data.get('course')
    userid = session.get('userID')

    send_form = register_form(firstname, middlename, lastname, age ,sex, province, city, barangay, contact_number, mothersname, fathersname, guardian, college, course, userid)
    if send_form:
        status = { "message": "Success", "error": "none" }
    else:
        status = {"message": "Something went Wrong", "error": "none"}
    return jsonify(status)


#SEND STATUS TO JS
@homepage.route('/user_status', methods=["POST", "GET"])
def get_status():
    userid = session.get('userID')
    info = get_user_info(userid)
    if not info:
        user_info = {
            'error': 'Something went Wrong'
        }
    else:
        user_info = {
            'status': info.status,
            'error': 'None'
        }
    return jsonify(user_info)

@homepage.route('/logout', methods=["POST", 'GET'])
def logout():
    session.clear()
    return redirect(url_for('frontpage.loginpage'))