from config import db
from uuid import uuid4
from log.helpper import logger


class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.String(255), primary_key=True)
    product_name = db.Column(db.String(120), nullable=False)
    unit_price = db.Column(db.Float, nullable=False)

    def __init__(self, product_name, unit_price):
        self.product_id = str(uuid4())
        self.product_name = product_name
        self.unit_price = unit_price


if __name__ == '__main__':
    try:
        db.create_all()
        db.session.commit()
        logger.info('Table products created.')
    except Exception as e:
        logger.error(e)
        logger.info('Table products can not be created!!')