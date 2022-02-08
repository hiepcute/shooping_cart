from config import db
from uuid import uuid4
from log.helpper import logger


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(120), nullable=False)
    last_name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(255))
    phone_number = db.Column(db.String(20))

    def __init__(self, email, password, firs_name, last_name, address, phone_number):
        self.user_id = str(uuid4())
        self.email = email
        self.password = password
        self.first_name = firs_name
        self.last_name = last_name
        self.address = address
        self.phone_number = phone_number


if __name__ == '__main__':
    try:
        db.create_all()
        db.session.commit()
        logger.info('Table users created.')
    except Exception as e:
        logger.error(e)
        logger.info('Table users can not be created!!')