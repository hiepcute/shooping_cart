from flask import Blueprint
from controller.cart_item_controller import get_cart_item, add_cart_item, delete, update


cart_item_bp = Blueprint('cart_item_bp', __name__)
cart_item_bp.route('/',methods=['GET'])(get_cart_item)
cart_item_bp.route('/<string:cart_item_id>', methods=['GET'])(get_cart_item)
cart_item_bp.route('/', methods=['POST'])(add_cart_item)
cart_item_bp.route('/', methods=['DELETE'])(delete)
cart_item_bp.route('/', methods=['PUT'])(update)