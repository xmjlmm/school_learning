from flask import Blueprint

# /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

# auth/login
@bp.route('/login')
def login():
    return 1