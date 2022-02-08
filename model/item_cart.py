from config import db
from uuid import uuid4
from log.helpper import logger
from model.cart_model import Cart
from model.product import Product


class CartItem(db.Model):
    __tablename__ = 'cart_item'

    cart_item_id = db.Column(db.String(255), primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    product_id = db.Column(db.String(255), db.ForeignKey('products.product_id', onupdate='CASCADE', ondelete='CASCADE'))
    cart_id = db.Column(db.String(255), db.ForeignKey('carts.cart_id', onupdate='CASCADE', ondelete='CASCADE'))
    products = db.relationship(Product)
    carts = db.relationship(Cart)

    def __init__(self, product_id, quantity, cart_id):
        self.cart_item_id = str(uuid4())
        self.quantity = quantity
        self. product_id = product_id
        self.cart_id = cart_id


if __name__ == '__main__':
    try:
        db.create_all()
        db.session.commit()
        logger.info('Table cart items created.')
    except Exception as e:
        logger.error(e)
        logger.info('Table cart items can not be created!!')