import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate   
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

    def __init__(self, title, subtitle, author, content, date_posted):
        self.title = title
        self.subtitle = subtitle
        self.author = author
        self.content = content
        self.date_posted = date_posted

    def __repr__(self):
        return f'<BlogPost {self.id}>'

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime)

    def __init__(self, name, email, message, date_sent):
        self.name = name
        self.email = email
        self.message = message
        self.date_sent = date_sent

@app.route('/')
def index():
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('index.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']
    new_post = BlogPost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())
    db.session.add(new_post)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_message = Message(name=name, email=email, message=message, date_sent=datetime.now())
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('contact'))
    return render_template('contact.html')

@app.route('/messages')
def messages():
    # Get the password from the URL or use a default
    provided_password = request.args.get('password')
    correct_password = os.getenv('ADMIN_PASSWORD', 'defaultpassword')
    
    if provided_password != correct_password:
        return "Unauthorized access", 403
    
    messages = Message.query.order_by(Message.date_sent.desc()).all()
    return render_template('messages.html', messages=messages)
