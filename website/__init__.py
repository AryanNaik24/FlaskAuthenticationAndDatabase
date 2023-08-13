from flask import Flask
from dotenv import load_dotenv
from os import path
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#initailise database
db = SQLAlchemy()
#database name
DB_NAME = "database.db"

#loads .env file
load_dotenv('.env')

#gets passwords and username from env fole and stores in variable
key: str = os.getenv('SECRETKEY')



def create_app():
    #initialise flask application
    app=Flask(__name__)
    #configure app
    app.config['SECRET_KEY'] = key
    #tells falsh that database stored at this location
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    #initialise database by giving flask app
    db.init_app(app)
    

    
    #imports blueprints from auth and views
    from .views import views
    from .auth import auth
    
    #registers blueprints
    app.register_blueprint(views , url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    #imports different models
    from .models import User,Note
    
    #creates database
    createDatabase(app)
    
    #initialises login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

#function to create database and check is one already exists
def createDatabase(app):

    with app.app_context():
        if not path.exists('website/' + DB_NAME):
            db.create_all()
            print('Created Database!')