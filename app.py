from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)

# Secret key for session management. Replace with a random key in production.
app.secret_key = 'your_secret_key'

# Dummy user data
users = {'admin': 'password'}

@app.route('/')
def index():
    return render_template('index.html')

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


if __name__ == '__main__':
    app.run(debug=True)