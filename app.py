from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

class Posts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    date_posted = db.Column(db.DateTime, nullable = False)
    image_url = db.Column(db.String(255), nullable=True)

# Secret key for session management. Replace with a random key in production.
app.secret_key = 'your_secret_key'

# Dummy user data 
# TODO: Add in real ecryption login method
users = {'admin': 'password'}

@app.route('/')
def index():
    initial_posts = Posts.query.order_by(Posts.date_posted.desc())
    print(initial_posts)
    return render_template('index.html', posts = initial_posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('login_success'))
        else:
            flash('Invalid credentials!')
    return render_template('login.html')

@app.route('/login_success')
def login_success():
    return render_template('login_success.html')

@app.route('/load-more-posts/<int:page>')
def load_more_posts(page):
    posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page, 1, False).items
    return jsonify([{'title' : post.title, 'content' : post.content, 'image_url' : post.image.url } for post in posts])


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)