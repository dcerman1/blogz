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

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'post', 'static']
    if request.endpoint not in allowed_routes and 'user' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['user'] = username
            return redirect('/addpost')
        elif user:
            flash('Password Incorrect. Please try again', 'error')
            return redirect("/login")
        else:
            flash('Username Not Found', 'error')
            return redirect("/login")

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify'] 
        
        #USERNAME ERRORS
        if len(username) < 3 or len(request.form['username']) > 20:
            flash('Usernames must be atleast 3 characters long','error')
            return redirect('/signup')
        if " " in username:
            flash('Spaces are not permitted in usernames', 'error')
            return redirect('/signup')
        username_db_count = User.query.filter_by(username=username).count()
        if username_db_count > 0:
            flash(username + ' already exists. Please enter a new username.', 'error')
            return redirect('/signup')
        
        #PASSWORD ERRORS
        if password != verify:
            flash('Passwords do not match', 'error')
            return redirect('/signup')
        if len(password) < 8:
            flash('Password must be longer than 8 characters', 'error')
        if " " in password:
            flash('Spaces are not permitted in passwords.' 'error')
        
        #USERNAME & PASSWORD PASS TESTS
        user = User(username, password)
        db.session.add(user)
        db.session.commit()
        session['user'] = username
        return redirect("/post")
    else:
        return render_template('signup.html')

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    del session['user']
    return redirect('/blog')

@app.route('/', methods=['POST','GET'])
def index():   
    #users = User.query.all()
    users = User.query.filter(User.posts.any()).all()
    return render_template('index.html',title="CONTRIBUTORS", 
        users=users)

@app.route('/author', methods=['GET'])
def author():
    if request.method == 'GET':
        id = request.args.get('id')
        user = User.query.filter_by(id=id).first()
        posts = Blog.query.filter_by(owner_id=id).all()
        return render_template('author.html', posts=posts, user=user)

@app.route('/blog', methods=['GET'])
def blog():   
    posts = Blog.query.filter_by(publish=True).all()
    return render_template('mainblog.html',title="My Blog", id=id, posts=posts, author=author)

@app.route('/post', methods=['GET'])
def view_post():
    if request.method == 'GET':
        id = request.args.get('id')
        blog = Blog.query.filter_by(id=id).first()
        author = User.query.filter_by(id=blog.owner_id).first()
        return render_template('post.html', id=id, blog=blog, author=author)

@app.route('/addpost', methods=['POST', 'GET'])
def add_post():
    #new parameter(owner_id) consider when creating a blog entry.
    if request.method == 'POST':
        new_title = request.form['title']
        new_post = request.form['post']
        blog = Blog.query.get(new_title)
        owner = User.query.filter_by(username=session['user']).first()
        new_blog = Blog(new_title, new_post, True, owner)
        
        db.session.add(new_blog)
        db.session.commit()
        blog = Blog.query.filter_by(title=new_title).first()
        return redirect ('/post?id='+str(blog.id))
 
    return render_template('addpost.html')

if __name__ == '__main__':
    app.run()

