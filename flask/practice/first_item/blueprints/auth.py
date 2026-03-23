from flask import Blueprint
from flask import render_template

# /auth
bp = Blueprint('auth', __name__, url_prefix='/auth')

# auth/login
@bp.route('/register')
def register():
    return render_template('register.html')