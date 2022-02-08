import jwt
from config import app
from functools import wraps
from flask import request, jsonify
from model.user import User
from log.helpper import logger


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = None

        # Check if token is in header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        # Return 401 if token is not in header
        if not token:
            return jsonify({'Message': 'Token is missing!!'}), 401

        try:
            # Decoding token
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(user_id=data['public_id']).first()
            logger.info('user {} verified'.format(current_user.email))
        except Exception as e:
            logger.error(e)
            return jsonify({'message': 'Invalid token!!'}), 401

        # Return the current logging user
        return func(current_user, *args, **kwargs)

    return decorated