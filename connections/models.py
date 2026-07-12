from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from connections.extensions import Base

class Users(Base):
    __tablename__ = 'accounts'

    userid = Column(String, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    status = Column(String, nullable=False)
    email_account = Column(String, nullable=False)
    application = relationship('ApplicationForm' , back_populates='student')


class ApplicationForm(Base):
    __tablename__ = 'form'

    formid = Column(String, primary_key=True)  
    firstname = Column(String, nullable=False)    
    middlename = Column(String, nullable=False)    
    lastname = Column(String, nullable=False)    
    age =  Column(Integer, nullable=False)    
    sex = Column(String, nullable=False)    
    province = Column(String, nullable=False)    
    city = Column(String, nullable=False)    
    barangay = Column(String, nullable=False)      
    contact_number = Column(Integer, nullable=False)    
    mothers_name = Column(String, nullable=False)    
    fathers_name = Column(String, nullable=False)    
    guardian = Column(String, nullable=False)    
    college = Column(String, nullable=False)
    course = Column(String, nullable=False)
    owner = Column(ForeignKey('accounts.userid'))
    student = relationship('Users', back_populates='application')