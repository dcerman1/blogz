from flask import Flask, request, redirect, render_template, flash, session
from flask_sqlalchemy import SQLAlchemy
from hashutils import make_pw_hash, check_pw_hash
import os

app = Flask(__name__)
app.config['DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://blogz:password@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'y337kGcys&zP3B'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(15000))
    publish = db.Column(db.Boolean)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, post, publish, owner):
        self.title = title
        self.post = post
        self.publish = publish
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    pw_hash = db.Column(db.String(15000))
    posts = db.relationship('Blog', backref='owner')
    
    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            flash("Logged in")
            return redirect('/addpost')
        else:
            flash('Username Does Not Exist', 'error')
            return redirect("/login")


@app.route('/', methods=['GET'])
def index():   
    posts = Blog.query.filter_by(publish=True).all()
    return render_template('mainblog.html',title="My Blog", 
        posts=posts)


@app.route('/post', methods=['GET'])
def view_post():
    if request.method == 'GET':
        id = request.args.get('id')
        blog = Blog.query.filter_by(id=id).first()
        return render_template('post.html', id=id, blog=blog)

@app.route('/addpost', methods=['POST', 'GET'])
def add_post():
    #new parameter(owner_id) consider when creating a blog entry.
    if request.method == 'POST':
        new_title = request.form['title']
        new_post = request.form['post']
        blog = Blog.query.get(new_title)
        new_blog = Blog(new_title, new_post, True)
        
        db.session.add(new_blog)
        db.session.commit()
        blog = Blog.query.filter_by(title=new_title).first()
        return redirect ('/post?id='+str(blog.id))
 
    return render_template('addpost.html')
    

if __name__ == '__main__':
    app.run()

