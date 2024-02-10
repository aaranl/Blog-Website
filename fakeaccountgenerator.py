from app import db, app
from app import Accounts

def add_fake_account():

    with app.app_context():
        
        new_user = Accounts(username='admin3')
        new_user.set_password('password')
        db.session.add(new_user)
        db.session.commit()

if __name__ == '__main__':
    add_fake_account()