from connections.models import Users, ApplicationForm
from connections.extensions import session
import uuid

def get_user_info(userid):
    user = session.query(Users).filter_by(userid=userid).first()

    if user is None:
        return False
    else:
        return user
 

def register_form(firstname, middlename, lastname, age ,sex, province, city, barangay, contact_number, mothersname, fathersname, guardian, college, course, userid):
    uid = str(uuid.uuid4())
    user = ApplicationForm(
        formid=uid, 
        firstname=firstname, 
        middlename=middlename,
        lastname=lastname,
        age=age,
        sex=sex,
        province=province,
        city=city,
        barangay=barangay,
        contact_number=contact_number,
        mothers_name=mothersname,
        fathers_name=fathersname,
        guardian=guardian,
        college=college,
        course=course,
        owner=userid
        )
    
    session.add(user)
    session.commit()

    return True