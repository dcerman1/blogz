from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://build-a-blog:doitnow@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    post = db.Column(db.String(15000))
    publish = db.Column(db.Boolean)

    def __init__(self, title, post, publish):
        self.title = title
        self.post = post
        self.publish = publish

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

