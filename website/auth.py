from flask import Blueprint,render_template,request,flash,redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .models import db

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    user = current_user
    if user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in Successfully!',category='sucess')
                login_user(user, remember=True)
                return redirect("/")
            else:
                flash('Incorrect Password! ',category='error')
        else:
            flash("Email Doesn't exist",category='error')
    return render_template("login.html",user=current_user)

@auth.route('/logout')

@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def signup():
    user = current_user
    if user.is_authenticated:
        return redirect("/")
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        role = request.form.get('user_type')
        password1 = request.form.get('password1')
        #password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!',category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        #elif password1 != password2:
        #   flash('Passwords don\'t match.', category='error')
        elif len(password1) < 2:
            flash('Password must be at least 2 characters.', category='error')
        else:
            new_user = User(email=email,username=name,password=generate_password_hash(password1, method='sha256'),role=role)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account Created!",category="success")  
            return redirect(url_for('views.home')) 
    return render_template("signup.html",user=current_user)