from flask import Blueprint
from flask import render_template, url_for, redirect, flash, request, abort, session,\
    Response, current_app, send_from_directory
from folioApp import db
from folioApp.modelsSite import Post
from sqlalchemy import func, desc


main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template('index.html')

@main.route("/blog")
def blog():
    return render_template('blog.html')

@main.route("/blog/webHostingFlask", methods=['POST','GET'])
def webHostingFlask():
    posts = Post.query.order_by(desc(Post.id)).all()
    if request.method == 'POST':
        formDict = request.form.to_dict()
        # print(formDict)
        newPost=Post(content=formDict.get('textareaEntry'))
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for("main.webHostingFlask"))
    return render_template('webHosting1flask.html', posts=posts)

@main.route("/blog/webHostingAWS")
def webHostingAWS():
    posts = Post.query.order_by(desc(Post.id)).all()
    if request.method == 'POST':
        formDict = request.form.to_dict()
        newPost=Post(content=formDict.get('textareaEntry'))
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for("main.webHostingAWS"))
    return render_template('webHosting2aws.html', posts=posts)
    
@main.route("/blog/webHostingPuttyWinscp")
def webHostingPuttyWinscp():
    posts = Post.query.order_by(desc(Post.id)).all()
    if request.method == 'POST':
        formDict = request.form.to_dict()
        # print(formDict)
        newPost=Post(content=formDict.get('textareaEntry'))
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for("main.webHostingPuttyWinscp"))
    return render_template('webHosting3puttyWinscp.html', posts=posts)
    
@main.route("/blog/webHostingVmEnvironment")
def webHostingVmEnvironment():
    posts = Post.query.order_by(desc(Post.id)).all()
    if request.method == 'POST':
        formDict = request.form.to_dict()
        # print(formDict)
        newPost=Post(content=formDict.get('textareaEntry'))
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for("main.webHostingVmEnvironment"))
    return render_template('webHosting4vmEnvironment.html', posts=posts)

    
@main.route("/blog/webHostingDomain")
def webHostingDomain():
    posts = Post.query.order_by(desc(Post.id)).all()
    if request.method == 'POST':
        formDict = request.form.to_dict()
        # print(formDict)
        newPost=Post(content=formDict.get('textareaEntry'))
        db.session.add(newPost)
        db.session.commit()
        return redirect(url_for("main.webHostingDomain"))
    return render_template('webHosting5domain.html', posts=posts)


@main.route("/blog/blog20210528")
def blog20210528():

    return render_template('blog20210528.html')




