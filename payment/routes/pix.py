from flask.blueprints import Blueprint
from flask import render_template, request, jsonify
from payment.payment.pix import Pix

pix_bp = Blueprint('pix', __name__, template_folder='templates')
PIX_PAYMENT = Pix()


@pix_bp.route('/pix/', methods=['POST', ])
def payment():
    form_data = {key: request.form.get(key, '').strip() for key in
                 ['amount', 'description', 'identificationType', 'identificationNumber', 'email']}

    if not PIX_PAYMENT.validate_form_data(form_data):
        return jsonify({'error': 'Invalid parameters'}), 400

    try:
        purchase_identification = PIX_PAYMENT.build_purchase_identification(form_data)
        cipher_purchase = PIX_PAYMENT.encrypt_data(purchase_identification)

        return render_template('pix.html', **form_data,
                               payment_mp_public_key=PIX_PAYMENT.MP_PUBLIC_KEY,
                               purchase_identification=cipher_purchase)
    except Exception as e:
        return jsonify({'error': 'Encryption failed', 'details': str(e)}), 500

