from config import db
from jwttoken import token_required
from model.item_cart import CartItem
from model.cart_model import Cart
from model.product import Product
from log.helpper import logger
from flask import jsonify, request


@token_required
def update_cart(current_user, subtotal):
    try:
        cart = Cart.query.filter_by(user_id=current_user.user_id).first()
        cart.subtotal = round(subtotal, 2)
        cart.vat = round(subtotal*0.1, 2)
        db.session.commit()
        logger.info('Cart total changed.')
    except Exception as e:
        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500


@token_required
def get_cart_item(current_user, cart_item_id=''):
    try:
        result = []
        cart = Cart.query.filter_by(user_id=current_user.user_id).first()
        cart_id = cart.cart_id
        if not cart_item_id:
            cart_items = CartItem.query.filter_by(cart_id=cart_id).all()
            for cart_item in cart_items:
                product = Product.query.filter_by(product_id=cart_item.product_id).first()
                output = {
                    'cart_item_id': cart_item.cart_item_id,
                    'quantity': cart_item.quantity,
                    'product_id': cart_item.product_id,
                    'subtotal':  round(product.unit_price * cart_item.quantity, 2),
                }
                result.append(output)

        else:
            cart_item = CartItem.query.filter(CartItem.cart_id == cart_id,
                                              CartItem.cart_item_id == cart_item_id).first()
            if not cart_item:
                return jsonify({'Message': 'Invalid request!!'}), 401
            product = Product.query.filter_by(product_id=cart_item.product_id).first()
            output = {
                'cart_item_id': cart_item.cart_item_id,
                'quantity': cart_item.quantity,
                'product_id': cart_item.product_id,
                'sub total': product.unit_price * cart_item.quantity
            }
            result.append(output)

        return {'data': result}
    except Exception as e:
        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500


# Function to update cart_item quantity
def update_cart_item(cart_item_id, quantity):
    try:
        cart_item = CartItem.query.filter_by(cart_item_id=cart_item_id).first()
        old_quantity = cart_item.quantity
        cart_item.quantity = quantity
        db.session.commit()
        logger.info('Cart item updated.')

        # Update cart upon updated cart item
        product = Product.query.filter_by(product_id=cart_item.product_id).first()
        unit_price = product.unit_price
        cart = Cart.query.filter_by(cart_id=cart_item.cart_id).first()
        subtotal = cart.subtotal
        price_change = unit_price * (quantity - old_quantity)
        subtotal += price_change
        update_cart(subtotal)
    except Exception as e:
        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500


@token_required
def add_cart_item(current_user):
    try:
        cart_item = request.form
        product_id = cart_item.get('product_id')
        quantity = int(cart_item.get('quantity'))

        # Return 401 for bad input
        if not cart_item or not product_id or not quantity or int(quantity) <= 0:
            return jsonify({'Message': 'Invalid request!!'}), 401

        # Check if product already in cart
        cart = Cart.query.filter_by(user_id=current_user.user_id).first()
        cart_item = CartItem.query.filter(CartItem.product_id == product_id, CartItem.cart_id == cart.cart_id).first()
        if cart_item:
            quantity += cart_item.quantity
            update_cart_item(cart_item.cart_item_id, quantity)

        # Add new cart item
        else:
            cart_item = CartItem(product_id, quantity, cart.cart_id)
            db.session.add(cart_item)
            logger.info('New cart item added.')
            product = Product.query.filter_by(product_id=cart_item.product_id).first()
            unit_price = product.unit_price
            subtotal = cart.subtotal
            subtotal += (unit_price * quantity)
            update_cart(subtotal)

        logger.info('Cart item added.')
        return jsonify({'Message': 'Success.'})
    except Exception as e:
        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500


@token_required
def delete(current_user):
    try:
        delete_cart_item = request.form
        cart_item_id = delete_cart_item.get('cart_item_id')

        cart = Cart.query.filter_by(user_id=current_user.user_id).first()
        cart_item = CartItem.query.filter(CartItem.cart_id == cart.cart_id,
                                          CartItem.cart_item_id == cart_item_id).first()

        if not delete_cart_item or not cart_item_id or not cart_item:
            return jsonify({'Message': 'Invalid request!!'}), 401

        update_cart_item(cart_item_id, 0)
        db.session.delete(cart_item)
        db.session.commit()

        logger.info('Cart item deleted')
        return jsonify({'Message': 'Success.'})
    except Exception as e:
        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500


@token_required
def update(current_user):
    try:
        updating_cart_item = request.form
        quantity = int(updating_cart_item.get('quantity'))
        cart_item_id = updating_cart_item.get('cart_item_id')

        cart = Cart.query.filter_by(user_id=current_user.user_id).first()
        cart_item = CartItem.query.filter(CartItem.cart_item_id == cart_item_id,
                                          CartItem.cart_id == cart.cart_id).first()

        if not updating_cart_item or not cart_item_id or not quantity or int(quantity) <= 0 or not cart_item:
            return jsonify({'Message': 'Invalid request!!'}), 401

        update_cart_item(cart_item.cart_item_id, quantity)

        logger.info('Cart item updated')
        return jsonify({'Message': 'Success.'})
    except Exception as e:
        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500