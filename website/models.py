from website import db 
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    email =  db.Column(db.String(150), unique=True)
    password =  db.Column(db.String(150))
    fullname = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    create_class = db.relationship('Create_class')
    join_class = db.relationship('Join_class')
    review = db.relationship('Review')


class Create_class(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    coursename =  db.Column(db.String(150))
    coursetitle =  db.Column(db.String(150))
    coursecode = db.Column(db.String(100), unique=True)
    courseprice = db.Column(db.Integer)
    description = db.Column(db.String(150), default='This is a Good Course')
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    join_class = db.relationship('Join_class')
    assignment = db.relationship('Assignment')
    suubmit = db.relationship('Submit')
    review = db.relationship('Review')


class Join_class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_class_id = db.Column(db.Integer, db.ForeignKey('create_class.id'))


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    comment =  db.Column(db.String(150))
    data = db.Column(db.LargeBinary)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    create_class_id = db.Column(db.Integer, db.ForeignKey('create_class.id'))

    suubmit = db.relationship('Submit')


class Submit(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date = db.Column(db.DateTime(timezone=True), default=func.now())

    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'))
    create_class_id = db.Column(db.Integer, db.ForeignKey('create_class.id'))


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_class_id = db.Column(db.Integer, db.ForeignKey('create_class.id'))



class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(150), unique=True, default='xyz')
    password =  db.Column(db.String(150), default='123')

