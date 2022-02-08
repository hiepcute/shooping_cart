from config import db
from model.product import Product
from log.helpper import logger


def add_product(product_name, unit_price):
    try:
        product = Product(product_name, unit_price)
        db.session.add(product)
        db.session.commit()
        logger.info('New product added')
    except Exception as e:
        logger.error(e)