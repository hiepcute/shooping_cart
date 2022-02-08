from flask import Blueprint
from controller.cart_controller import get_cart


cart_bp = Blueprint('cart_bp', __name__)
cart_bp.route('/', methods=['GET'])(get_cart)