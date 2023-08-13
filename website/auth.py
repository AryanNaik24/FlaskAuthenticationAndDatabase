from flask import Blueprint, render_template , request , flash , url_for , redirect
from .models import User
from werkzeug.security import generate_password_hash , check_password_hash , gen_salt
from . import db
from flask_login import login_user , login_required , logout_user , current_user , login_remembered

#blueprint of our application
#stores routes in different file
auth = Blueprint('auth',__name__)


#route for login page
@auth.route("/login",methods=["GET","POST"])
def login():
    if request.method == 'POST':
        #gets email and password from post requests and stores it
        email = request.form.get('email')
        password = request.form.get('password')
        
        #finds user from the database
        user = User.query.filter_by(email=email).first()
        
        #checks if password matches and email exists
        if user:
            if check_password_hash(user.password,password):
                flash("logged in successfully!",category='success')
                #logs in user
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
                
            else:
                flash("Incorrect Password",category='error')
        else:
            flash("Email does not exist",category='error')
            
        
    data = request.form
    return render_template("login.html",user=current_user)

#route for signup page
@auth.route("/signup",methods=["GET","POST"])
def signup():
    
    #checks if method is post i.e data is being sent to server
    if request.method == 'POST':
        #variables to store incoming data
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        #finds user from the database
        user = User.query.filter_by(email=email).first()
        
        #checks for errors
        if user:
            flash('Email already exists!',category='error')
        elif len(email) < 4:
            flash('Email must be atleast 4 characters long',category='error')
            
        elif len(name) < 2:
            flash('Username must be atleast 2 characters long',category='error')

        elif password1 != password2:
            flash('Passwords do not match',category='error')

        elif len(password1) < 8:
            flash('Password must be atleast 8 characters long',category='error')

        else:
            #adds new user
            new_user = User(email=email,password=generate_password_hash(password1,method='sha256'),user_name=name)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created!',category='success')
            
            #logs in user
            login_user(user,remember=True)
            
            
            
            #redirects to home page
            return redirect(url_for('views.home'))


    
    return render_template("signup.html",user=current_user)

#route for logout page
@auth.route("/logout",methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))