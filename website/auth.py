from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Create_class, Join_class, User, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from website import db

auth = Blueprint('auth', __name__)




@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                flash(f'Welcome {current_user.fullname}!', category='success')
                return redirect(url_for('views.home'))
 
            else: 
                flash('Incorrect email or password. Try again!', category='danger')
                return redirect(url_for('auth.login'))

        else: 
            flash('Email does not exist! ', category='danger')
            return redirect(url_for('auth.login'))

    return render_template("login.html", user=current_user)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))



@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        fullName = request.form.get('fullName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists. Enter another email address!", category='danger')

        elif len(email)<4:
            flash("Email must be grater than 4 Character", category='danger')

        elif len(fullName)<2:
            flash("Name must be grater than one character", category='danger')

        elif password1 != password2:
            flash("Password don't match", category='danger')

        elif len(password1)<6:
            flash("Password must be atleast 6 Character", category='danger')

        else:
            new_user = User(email=email, fullname=fullName, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Account is successfully created!", category='success')
            return redirect(url_for('auth.login'))



    return render_template("signup.html", user=current_user)



@auth.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Admin.query.filter_by(username=username).first()
        if user:
                return redirect(url_for('auth.admin_panel'))
 
        else: 
            flash('Incorrect username or password. Try again!', category='danger')
            return redirect(url_for('auth.admin'))

    return render_template("admin.html", user=current_user)



@auth.route('/admin-panel', methods=['GET', 'POST'])
def admin_panel():
    users = []
    for user in User.query.all():
        temp = {'id':user.id,
                'email':user.email,
                'password':user.password,
                'fullname': user.fullname,
                'date':user.date,
                }
        users.append(temp)

    classes = []
    for clas in Create_class.query.all():
        temp= {'id':clas.id,
                'coursename':clas.coursename,
                'coursetitle':clas.coursetitle,
                'coursecode': clas.coursecode,
                'description':clas.description,
                'date':clas.date,
                'user_id':clas.user_id
                }
        classes.append(temp)

    joins = []
    for join in Join_class.query.all():
        temp= {'id':clas.id,
                'date':clas.date,
                'user_id':clas.user_id
                }
        joins.append(temp)
    return render_template("admin_panel.html", users=users, classes=classes,joins=joins, user='admin')