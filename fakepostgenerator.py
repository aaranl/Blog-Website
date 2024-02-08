from faker import Faker
from app import db, app
from app import Posts

def add_fake_post(num_post=45):
    fake = Faker() 

    with app.app_context():
        for _ in range(num_post):
            title = fake.sentence()
            content = fake.text()
            date_posted = fake.date_time_between(start_date='-1y', end_date='now')
            image_url = fake.image_url()

            post = Posts(title=title, content=content, date_posted=date_posted, image_url=image_url)
            db.session.add(post)

        db.session.commit()

if __name__ == '__main__':
    add_fake_post()