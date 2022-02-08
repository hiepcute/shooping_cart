from config import db
from uuid import uuid4
from log.helpper import logger
from model.user import User


class Cart(db.Model):
    __tablename__ = 'carts'

    cart_id = db.Column(db.String(255), primary_key=True)
    user_id = db.Column(db.String(255), db.ForeignKey('users.user_id', onupdate='CASCADE', ondelete='CASCADE'))
    subtotal = db.Column(db.Float, default=0)
    vat = db.Column(db.Float, default=0)
    users = db.relationship(User)

    def __init__(self, user_id, subtotal):
        self.cart_id = str(uuid4())
        self.subtotal = subtotal
        self.vat = subtotal * 0.1
        self.user_id = user_id


if __name__ == '__main__':
    try:
        db.create_all()
        db.session.commit()
        logger.info('Table carts created.')
    except Exception as e:
        logger.error(e)
        logger.info('Table carts can not be created!!')