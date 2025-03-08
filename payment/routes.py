from flask.blueprints import Blueprint
from flask import render_template, request, jsonify
from payment.payment.card import Card


payment_bp = Blueprint('payment', __name__, template_folder='templates')
CARD_PAYMENT = Card()


@payment_bp.route('/', methods=['POST', ])
def payment():
    form_data = {key: request.form.get(key, '').strip() for key in
                 ['amount', 'description', 'identificationType', 'identificationNumber', 'email']}

    if not CARD_PAYMENT.validate_form_data(form_data):
        return jsonify({'error': 'Invalid parameters'}), 400

    try:
        purchase_identification = CARD_PAYMENT.build_purchase_identification(form_data)
        cipher_purchase = CARD_PAYMENT.encrypt_data(purchase_identification)

        return render_template('index.html', **form_data,
                               payment_mp_public_key=CARD_PAYMENT.MP_PUBLIC_KEY,
                               purchase_identification=cipher_purchase)
    except Exception as e:
        return jsonify({'error': 'Encryption failed', 'details': str(e)}), 500


@payment_bp.route('/process_payment', methods=['POST'])
def handle_payment():
    try:
        if not request.is_json:
            print("Invalid request format. Expected JSON")
            return jsonify({"error": "Invalid request format. Expected JSON"}), 400

        data = request.get_json()
        purchase_identification = CARD_PAYMENT.decrypt_purchase_identification(data["purchase_identification"])

        if not CARD_PAYMENT.validate_purchase_data(purchase_identification, data):
            print("Invalid parameters")
            return jsonify({'error': 'Invalid parameters'}), 400

        payment_response = CARD_PAYMENT.process_payment(data)
        if payment_response.get('status') == "in_process":
            pass

        return jsonify(payment_response), 200
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        print(f"Error processing payment: {e}")
        return jsonify({"error": "Internal server error"}), 500


@payment_bp.route('/payment_response', methods=['GET', ])
def payment_response():
    return render_template('response.html')


@payment_bp.route('/payment_error', methods=['GET', ])
def payment_error():
    return render_template('error.html')


@payment_bp.route('/checkout', methods=['GET', ])
def checkout():
    return render_template('checkout.html')
