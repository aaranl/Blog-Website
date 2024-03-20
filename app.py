from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from argon2 import PasswordHasher
from datetime import datetime
from argon2.exceptions import VerifyMismatchError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)
ph = PasswordHasher()

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
    
class Accounts(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique = True, nullable = False)
    password_hashed = db.Column(db.String(255), nullable = True)

    def set_password(self, password):
        self.password_hashed = ph.hash(password)

    def verify(self, password):
        return ph.verify(self.password_hashed, password)

# Secret key for session management. Replace with a random key in production.
app.secret_key = 'your_secret_key'


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

        user = Accounts.query.filter_by(username=username).first()

        if user and user.verify(password): 
            return redirect(url_for('login_success')) 
        else:
            flash('Invalid username or password')
        
    return render_template('login.html')

@app.route('/login_success')
def login_success():
    return render_template('login_success.html')

@app.route('/load-more-posts/<int:page>')
def load_more_posts(page):
    paginated_posts = Posts.query.order_by(Posts.date_posted.desc()).paginate(page=page, per_page=10, error_out=False)
    posts = paginated_posts.items
    return jsonify([post.to_dict() for post in posts])


@app.route('/create=post', methods=['POST'])
def create_post():
    title = request.form['title']
    content = request.form['content']
    image = request.files['image']
    image_url = None

    if image and allowed_file(image.filename):
        # add stuff
        pass

    new_post = Posts(title = title, content = content, date_posted = datetime.utcnow(), image_url = image_url)
    db.sessions.add(new_post)
    db.session.commit()
        


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}



with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()