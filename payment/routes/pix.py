from flask.blueprints import Blueprint
from flask import render_template, request, jsonify
from payment.payments.pix import Pix
from payment.payments.base import PaymentData

pix_bp = Blueprint('pix', __name__, template_folder='templates')
PIX_PAYMENT = Pix()


@pix_bp.route('/pix/', methods=['POST', ])
def payment():
    form_data = {key: request.form.get(key, '').strip() for key in
                 ['amount', 'description', 'identificationType', 'identificationNumber', 'email', 'returnLink']}

    if not PIX_PAYMENT.validate_form_data(form_data):
        return jsonify({'error': 'Invalid parameters'}), 400

    try:
        purchase_identification = PIX_PAYMENT.build_purchase_identification(form_data)
        cipher_purchase = PIX_PAYMENT.encrypt_data(purchase_identification)

        return render_template('pix/pix.html', **form_data,
                               payment_mp_public_key=PIX_PAYMENT.MP_PUBLIC_KEY,
                               purchase_identification=cipher_purchase)
    except Exception as e:
        return jsonify({'error': 'Encryption failed', 'details': str(e)}), 500


@pix_bp.route('/pix/process_payment/', methods=['POST', ])
def process_payment():
    if not request.form:
        print('Invalid request format. Expected JSON')
        return render_template('pix/error.html', error='Invalid request format. Expected JSON')

    data = request.form

    try:
        purchase_identification = PIX_PAYMENT.decrypt_purchase_identification(data["purchase_identification"])

        if not PIX_PAYMENT.validate_purchase_data(purchase_identification, data):
            print('Invalid parameters')
            return render_template('pix/error.html', error='Invalid parameters', return_link=data['return_link'])

        payment_data = PaymentData(
            float(data["transactionAmount"]), data["description"], "pix", data["email"],
            data["payerFirstName"], data["payerLastName"], data["identificationType"], data["identificationNumber"],
            data["zipCode"], data["streetName"], data["streetNumber"], data["neighborhood"], data["city"],
            data["federalUnit"]
        )
        payment_status, payment_response = PIX_PAYMENT.process_payment(payment_data, data["purchase_identification"])
        if payment_status != 201:
            print(payment_response)
            return render_template('bill/error.html', error=payment_response['message'], return_link=data['return_link'])

        return render_template('pix/successful.html',
                               qr_code_base64=payment_response['point_of_interaction']['transaction_data']['qr_code_base64'],
                               qr_code=payment_response['point_of_interaction']['transaction_data']['qr_code'], return_link=data['returnLink'])
    except ValueError as e:
        print(e)
        return render_template('pix/error.html', error=e, return_link=data['return_link'])

    except Exception as e:
        print(f"Error processing payment: {e}")
        return render_template('pix/error.html', error=e, return_link=data['return_link'])
