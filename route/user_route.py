from flask import Blueprint
from controller.user_controller import login, get_user

user_bp = Blueprint('user_bp', __name__)
user_bp.route('/login', methods=['POST'])(login)
user_bp.route('/', methods=['GET'])(get_user)