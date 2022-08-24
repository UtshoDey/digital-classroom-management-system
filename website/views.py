from ast import Assign
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from website import db
from website.auth import login
from website.models import Assignment, Create_class, Join_class, User
from werkzeug.utils import secure_filename

views = Blueprint('views', __name__)


@views.route('/home')
@login_required
def home():
    temps = Create_class.query.all()
    courses = temps[:]
    for temp in range(len(temps)):
        if temps[temp].user_id == current_user.id:
            courses.remove(temps[temp])
    print(courses)
    
    return render_template('home.html', user=current_user, name=current_user.fullname, courses=courses)

@views.route('/')
@views.route('/index')
def index():
    courses = Create_class.query.all()
    
    return render_template('index.html', user=current_user, courses=courses)




@views.route('/addcourse', methods=['GET', 'POST'])
@login_required
def addcourse():
    if request.method == 'POST':
        coursename = request.form.get('coursename')
        coursetitle = request.form.get('coursetitle')
        coursecode = request.form.get('coursecode')
        courseprice = request.form.get('courseprice')

        create_class = Create_class(coursename=coursename, coursetitle=coursetitle, coursecode=coursecode, courseprice=courseprice, user_id=current_user.id)

        db.session.add(create_class)
        db.session.commit()
        flash("Course is successfully added!", category='success')
        return redirect(url_for('views.home'))

    return render_template('addcourse.html', user=current_user, name=current_user.fullname)


@views.route('/joincourse', methods=['GET', 'POST'])
@login_required
def joincourse():
    if request.method == 'POST':
        coursecode = request.form.get('coursecode')
        coursetitle = request.form.get('coursetitle')
        validate = Create_class.query.filter_by(coursecode=coursecode).first() and Create_class.query.filter_by(coursetitle=coursetitle).first()
        if validate:
            join = Join_class(create_class_id=validate.id, user_id=current_user.id)
            db.session.add(join) 
            db.session.commit()
            flash("Course is successfully joined!", category='success')
            return redirect(url_for('views.home'))
        
        else: 
            flash("Course Code and Course Title didnot match. Try Again!", category='danger')
            return redirect(url_for('views.joincourse'))

        

    return render_template('joincourse.html', user=current_user, name=current_user.fullname)



@views.route('/profile/<username>')
@login_required
def profile(username):
    temp = []
    for course in current_user.join_class:
        temp.append(course.create_class_id)

    temp2 = Create_class.query.all()
    temp3 = temp2.copy()
    for i in temp2:
        if i.id not in temp:
            temp3.remove(i)

    print(temp3)

    return render_template('profile.html', user=current_user, name=current_user.fullname, join=temp3)


@views.route('/profile/<username>/<coursename>', methods=['GET', 'POST'])
@login_required
def teacherview(username,coursename):
    if request.method == "POST":
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part', category='success')
            return redirect(url_for('views.teacherview'))

        file = request.files['file']
        
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file', category='success')
            return redirect(url_for('views.teacherview'))

        if file:
            filename = secure_filename(file.filename)
            upload = Assignment(data=file.read(),create_class_id=current_user.id)
            db.session.add(upload)
            db.session.commit()
            flash(f"{filename} is Upload Successfully!", category='success')
            return render_template('teacherview.html', user=current_user,name=current_user.fullname)

    return render_template('teacherview.html', user=current_user,name=current_user.fullname)



@views.route('/profile/<username>/<coursename>/<assignment>', methods=['GET', 'POST'])
@login_required
def studentview(username,coursename,assignment):
    # temp = User.query.all()
    # user = None
    # print(coursename,username)
    # for t in temp:
    #     if t.id == current_user.id:
    #         user = t.id

    # temp2 = Create_class.query.all()
    # classes = []
    # for t in temp2:
    #     if t.assignment_id == user:
    #         classes.append(t.id)

    # print(user)
    # print(classes)


        

    return render_template('studentview.html', user=current_user,name=current_user.fullname,)


