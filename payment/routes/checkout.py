from flask.blueprints import Blueprint
from flask import render_template

checkout_bp = Blueprint('checkout', __name__, template_folder='templates')


@checkout_bp.route('/', methods=['GET', ])
def checkout():
    return render_template('checkout.html')
