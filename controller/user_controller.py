import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from flask import request, make_response, jsonify
from config import app, db
from model.user import User
from log.helpper import logger
from controller.cart_controller import add_cart, get_cart
from jwttoken import token_required


def login():
    auth = request.form
    email = auth.get('email')
    password = auth.get('password')

    # Return 401 if email or password is missing
    if not auth or not email or not password:
        return make_response(
            'Could not verify!!', 401,
            {'WWW-Authenticate': 'Basic realm="Login required!!"'}
        )

    user = User.query.filter_by(email=email).first()

    # Return 401 if user is not exist
    if not user:
        return make_response(
            'Email in correct!!', 401,
            {'WWW-Authenticate': 'Basic realm="User does not exist!!"'}
        )

    # Return token if password is correct
    if check_password_hash(user.password, password):
        token = jwt.encode({
            'public_id': user.user_id,
            'exp': datetime.utcnow() + timedelta(minutes=300)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        logger.info('user {} has login.'.format(user.email))
        return jsonify({'token': token}), 200

    # Return if password is wrong
    return make_response(
        'Wrong password!!', 403,
        {'WWW-Authenticate': 'Basic realm="Wrong password!!"'}
    )


def add_user(email, password, first_name, last_name, address, phone_number):
    try:
        password = generate_password_hash(password)
        user = User(email, password, first_name, last_name, address, phone_number)
        db.session.add(user)
        db.session.commit()
        logger.info('New user added')

        # add new cart for the new user
        user = User.query.filter_by(email=email).first()
        user_id = user.user_id
        add_cart(user_id, 0)
        return {'Message': 'Success'}
    except Exception as e:
        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500


@token_required
def get_user(current_user):
    try:
        result = []
        user = User.query.filter_by(user_id=current_user.user_id).first()
        output = {
            'user id': user.user_id,
            'first name': user.first_name,
            'last name': user.last_name,
            'email': user.email,
            'address': user.address,
            'phone': user.phone_number,
            'cart': get_cart()['data'],
        }
        result.append(output)
        return {'data': result}
    except Exception as e:
        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500


@token_required
def delete(current_user):
    try:
        user = User.query.filter_by(user_id=current_user.user_id).first()
        db.session.delete(user)
        db.session.commit()
        logger.info('Delete user {}'.format(user.email))
    except Exception as e:
        logger.error(e)
        return jsonify({'Message': 'Server error!!'}), 500