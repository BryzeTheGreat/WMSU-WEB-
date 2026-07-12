from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from authentications.RegisterAuth.register_auth import register_new_user, code_generator, send_auth_code, get_user_id, verify_user, login

frontpage = Blueprint('frontpage', __name__)


#WELL JUST OL' NORMAL LOGIN
@frontpage.route('/', methods=['POST', 'GET'])
def loginpage():
    error = None
    if session.get('logged_in') == True:
        id = session.get('userID')
        if verify_user(id):
            return redirect(url_for('homepage.main'))
        else:
            return redirect(url_for('frontpage.logout'))
    else:
        print(session.get('logged_in'))

        
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if login(username, password):
            id = get_user_id(username)
            session['logged_in'] = True
            session['userID'] = id
            print('YAR')
            return redirect(url_for('homepage.main'))
        else:
            error = 'Wrong Password or Username'
            return render_template('login.html', error=error)
    
    return render_template('Frontpage/login.html', error=error)


#USERNAME AND PASSWORD MAKING
@frontpage.route('/register', methods=["POST", "GET"])
def registerpage():
    error = None
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        verify_password = request.form.get('verify-password')

        if verify_password != password:
            error = "Wrong Password"
            return render_template('register.html', error=error)

        if not username or password == "":
            error = "Something went Wrong"
            return render_template('register.html', error=error)

        session['username'] = username
        session['password'] = password
        session['finalizing'] = True
        return redirect(url_for('frontpage.finalizing_registering'))

    return render_template('Frontpage/register.html', error=error)


#FINALIZING THE NEEDED THINGS BEFORE ACCOUNT CREATION
@frontpage.route('/register/finalizing-registering', methods=["POST", "GET"])
def finalizing_registering():
    if not session.get('finalizing'):
        return redirect(url_for('frontpage.registerpage'))
    

    error = None

    if request.method == "POST":
        firstname = request.form.get('firstname')
        middlename = request.form.get('middlename')
        lastname = request.form.get('lastname')
        email = request.form.get('email')

        if firstname == "" or lastname == "" or email == "":
            error = "Something went Wrong"
            return render_template('finalizing_registering.html', error=error)
        if middlename:    
            name = f"{firstname} {middlename} {lastname}"
        else:
            name = f"{firstname} {lastname}"    

        session['fullname'] = name
        session['email'] = email    
        session['final_authentication'] = True

        #GENERATING THE CODE FOR VERIFICATION
        code = code_generator()
        session['code'] = code

        if send_auth_code(email, code):
            return redirect(url_for('frontpage.final_authentication_code'))

    return render_template('Frontpage/finalizing_registering.html', error=error)

#IF MAIL CODE WASNT SEND
@frontpage.route('/resend-code', methods=["POST", "GET"])
def resend():
    email = session.get('email')
    code = code_generator()
    if send_auth_code(email, code):
        session['code'] = code
        print(session.get('code'))
        print(session.get('fullname'))
        print(session.get('username'))
        print(session.get('password'))
        print(session.get('email'))
        return redirect(url_for('frontpage.final_authentication_code'))
    else:   
        return redirect(url_for('frontpage.final_authentication_code'))
        

#FINAL AUTHENTICATION CODE BEFORE GOING TO MAIN PAGE/HOME PAGE
@frontpage.route('/register/final_authentication_code', methods=["POST", "GET"])
def final_authentication_code():
    error = None
    if not session.get('final_authentication'):
        return redirect(url_for('frontpage.finalizing_registering'))
    

    if request.method == "POST":
        verification_code = request.form.get('code')
        final_code = session.get('code')

        if verification_code == final_code:
            username = session.get('username')
            password = session.get('password')
            name = session.get('fullname')
            email = session.get('email')
            new_account = register_new_user(username, password, name, email)

            if new_account:
                userid = get_user_id(session.get('username'))
                session['logged_in'] = True
                session['userID'] = userid
                session.clear()
                return redirect(url_for('homepage.main'))
            
            else:
                error = "Something Went Wrong"
                return render_template('final_auth_code.html', error=error)
            
        else:
            error = "Wrong Verification Code"
            return render_template('final_auth_code.html', error=error)
    return render_template('Frontpage/final_auth_code.html', error=error)


@frontpage.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('frontpage.loginpage'))