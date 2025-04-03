from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def home():
    return 'Backend running!'

@dashboard_bp.route('/login', methods=['OPTIONS'])
def handle_options():
    return '', 200

