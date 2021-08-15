from folioApp import db
from datetime import datetime, date

class Post(db.Model):
    __bind_key__ = 'dbSite'
    id = db.Column(db.Integer,primary_key=True)
    siteSection = db.Column(db.Text)
    article = db.Column(db.Text)
    title= db.Column(db.Text)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)
    attachment = db.Column(db.String(100))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'), default=1)


    def __repr__(self):
        return f"Post('{self.id}','{self.date_posted}')"


class Datatoolspage(db.Model):
    __bind_key__ = 'dbSite'
    id = db.Column(db.Integer,primary_key=True)
    title= db.Column(db.Text, nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)
    

    def __repr__(self):
        return f"DataToolsPage('{self.id}','{self.date_posted}','{self.title}')"

class Blogpage(db.Model):
    __bind_key__ = 'dbSite'
    id = db.Column(db.Integer,primary_key=True)
    title= db.Column(db.Text, nullable=False)
    datePosted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text)

    def __repr__(self):
        return f"BlogPage('{self.id}','{self.date_posted}','{self.title}')"


class User(db.Model):
    __bind_key__ = 'dbSite'
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50), unique=True)
    email = db.Column(db.String(150), unique=True)
    image_file = db.Column(db.String(100))
    password = db.Column(db.String(100))
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}')"