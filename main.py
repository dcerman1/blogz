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

    def __init__(self, title, post):
        self.title = title
        self.post = post
        self.publish = False

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        new_title = request.form['title']
        new_post = request.form['post']
        publish = True
        new_blog = Blog(new_title, new_post)
   
        db.session.add(new_blog)
        db.session.commit()
    
    posts = Blog.query.filter_by(publish=False).all()
    return render_template('mainblog.html',title="MY BLOG", 
        posts=posts)
    
if __name__ == '__main__':
    app.run()

"""       blog_id = int(request.form['blog-id'])
        blog = Task.query.get(blog_id)
        blog.publish = True"""
