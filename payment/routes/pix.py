from flask.blueprints import Blueprint
from flask import render_template, request, jsonify

pix_bp = Blueprint('pix', __name__, template_folder='templates')


@pix_bp.route('/pix/', methods=['GET', ])
def payment_response():
    return render_template('pix.html')

