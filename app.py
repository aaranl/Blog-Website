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

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "date_posted": self.date_posted.strftime("%Y-%m-%d %H:%M:%S"),
            "image_url": self.image_url
        }

# Secret key for session management. Replace with a random key in production.
app.secret_key = 'your_secret_key'

# Dummy user data 
# TODO: Add in real ecryption login method
users = {'admin': 'password'}

@app.route('/')
def index():
    initial_posts = Posts.query.order_by(Posts.date_posted.desc()).limit(10).all()
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
    paginated_posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=10, error_out=False)
    posts = paginated_posts.items
    return jsonify([post.to_dict() for post in posts])


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)