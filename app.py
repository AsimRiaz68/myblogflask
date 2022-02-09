import datetime
from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from datetime import datetime

import re
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Allah@111'
app.config['MYSQL_DB'] = 'pythonlogin'
db = SQLAlchemy(app)


class CodeSpeedyBlog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    posted_by = db.Column(db.String(20), nullable=False, default='N/A')
    posted_on = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow())
    def __repr__(self):
        return self.title
    app.secret_key = 'your secret key'
# Intialize MySQL
mysql = MySQL(app)
@app.route('/login/', methods=['GET', 'POST'])
def login():
    
    msg = ''
    
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
       
        username = request.form['username']
        password = request.form['password']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
       
        account = cursor.fetchone()
        
        if account:
            
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
           
            return 'Logged in successfully!'
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)


db.create_all()
db.session.commit()
@app.route('/')
@app.route('/home')
@app.route('/CodeSpeedy')
def Welcome():
    return render_template('index.html')

@app.route('/posts',  methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = CodeSpeedyBlog(title=post_title,
                        content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()

        return redirect('/posts')
    else:
        all_posts = CodeSpeedyBlog.query.order_by(CodeSpeedyBlog.posted_on).all()
        return render_template('posts.html', posts=all_posts)

@app.route('/posts/delete/<int:id>')
def delete(id):
    to_delete = CodeSpeedyBlog.query.get_or_404(id)
    db.session.delete(to_delete)
    db.session.commit()
    return redirect('/posts')     

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    to_edit = CodeSpeedyBlog.query.get_or_404(id)
    if request.method == 'POST':
        to_edit.title = request.form['title']
        to_edit.author = request.form['author']
        to_edit.content = request.form['post']
        db.session.commit()
        return redirect('/posts')

    else:
        return render_template('edit.html', post=to_edit)

@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['post']
        post_author = request.form['author']
        new_post = CodeSpeedyBlog(title=post_title,
                        content=post_content, posted_by=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')

if __name__ == "__main__":
    app.run(debug=True)