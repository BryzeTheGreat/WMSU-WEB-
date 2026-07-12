#EXTENSIONS
from flask import Flask
from flask_mail import Mail
import os
from dotenv import load_dotenv

#LOAD DOTENV
load_dotenv()

#CONNECTIONS MODULE
from connections.extensions import engine, session, Base, mail
from connections.models import Users, ApplicationForm


#ROUTES
from routes.frontpage_bp import frontpage
from routes.homepage_bp import homepage
main = Flask(__name__)

#DATABASE 
Base.metadata.create_all(engine)

#CONFIGS
main.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
main.config['MAIL_SERVER'] = 'smtp.gmail.com'
main.config['MAIL_PORT'] = 587
main.config['MAIL_USE_TLS'] = True
main.config['MAIL_USE_SSL'] = False
main.config['MAIL_USERNAME'] = 'blizzliz12345@gmail.com'
main.config['MAIL_PASSWORD'] = os.environ.get('GMAIL_PASSWORD')
main.config['MAIL_DEFAULT_SENDER'] = 'noreplyWMSU@gmail.com'

#MAIL
mail.init_app(main)

#REGISTER ROUTES

main.register_blueprint(frontpage)
main.register_blueprint(homepage)

if __name__ == "__main__":
    main.run()
