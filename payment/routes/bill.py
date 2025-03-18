from flask.blueprints import Blueprint
from flask import render_template, request, jsonify
from payment.payment.bill import Bill

bill_bp = Blueprint('bill', __name__, template_folder='templates')
BILL_PAYMENT = Bill()


@bill_bp.route('/bill/', methods=['POST', ])
def payment():
    form_data = {key: request.form.get(key, '').strip() for key in
                 ['amount', 'description', 'identificationType', 'identificationNumber', 'email', 'returnLink']}

    if not BILL_PAYMENT.validate_form_data(form_data):
        return jsonify({'error': 'Invalid parameters'}), 400

    try:
        purchase_identification = BILL_PAYMENT.build_purchase_identification(form_data)
        cipher_purchase = BILL_PAYMENT.encrypt_data(purchase_identification)

        return render_template('bill/bill.html', **form_data,
                               payment_mp_public_key=BILL_PAYMENT.MP_PUBLIC_KEY,
                               purchase_identification=cipher_purchase)
    except Exception as e:
        return jsonify({'error': 'Encryption failed', 'details': str(e)}), 500


@bill_bp.route('/bill/process_payment/', methods=['POST', ])
def process_payment():
    if not request.form:
        print('Invalid request format. Expected JSON')
        return render_template('pix/error.html', error='Invalid request format. Expected JSON')

    data = request.form

    try:
        purchase_identification = BILL_PAYMENT.decrypt_purchase_identification(data["purchase_identification"])

        if not BILL_PAYMENT.validate_purchase_data(purchase_identification, data):
            print('Invalid parameters')
            return render_template('bill/error.html', error='Invalid parameters', return_link=data['return_link'])

        payment_status, payment_response = BILL_PAYMENT.process_payment(data)

        if payment_status != 201:
            print(payment_response)
            return render_template('bill/error.html', error=payment_response['message'], return_link=data['return_link'])

        return render_template('bill/successful.html')
    except ValueError as e:
        print(e)
        return render_template('bill/error.html', error=e, return_link=data['return_link'])

    except Exception as e:
        print(f"Error processing payment: {e}")
        return render_template('bill/error.html', error=e, return_link=data['return_link'])
