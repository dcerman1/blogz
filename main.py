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
    body = db.Column(db.String(15000))
    publish = db.Column(db.Boolean())

    def __init__(self,title):
        self.title = title
        self.body = body

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        post_name = request.form['post']
        new_post = Blog(post_name)
        db.session.add(new_post)
        db.session.commit()

    posts = Blog.query.filter_by(publish=True).all()
    published_posts = Blog.query.filter_by(publish=True).all()
    
    return render_template('blogposts.html',title="My Blog!", 
    posts=posts, published_posts=published_posts)

@app.route('/delete-blog', methods=['POST'])
def delete_task():
    blog_id = int(request.form['blog-id'])
    blog = Blog.query.get(blog_id)
    blog.publish = True
    db.session.add(task)
    db.session.commit()

    return redirect ('/')

if __name__ == '__main__':
    app.run()