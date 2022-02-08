from model.cart_model import Cart
from config import db
from log.helpper import logger
from flask import jsonify
from jwttoken import token_required
from controller.cart_item_controller import get_cart_item


def add_cart(user_id, subtotal):
    try:
        cart = Cart(user_id, subtotal)
        db.session.add(cart)
        db.session.commit()
        logger.info('New cart added')
        return {'Message': 'Success'}
    except Exception as e:
        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500


@token_required
def get_cart(current_user):
    try:
        result = []
        cart = Cart.query.filter_by(user_id=current_user.user_id).first()
        output = {
            'cart id': cart.cart_id,
            'subtotal': round(cart.subtotal, 2),
            'vat': round(cart.vat, 2),
            'total': round(cart.subtotal + cart.vat, 2),
            'cart_item': get_cart_item()['data'],
        }
        result.append(output)
        return {'data': result}
    except Exception as e:

        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500