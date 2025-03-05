from flask.blueprints import Blueprint
from flask import render_template, request, jsonify
import mercadopago
import hmac
import hashlib
import os

payment_bp = Blueprint('payment', __name__, template_folder='templates')
PRIVATE_KEY = os.environ.get("PAYMENT_PRIVATE_KEY")
PUBLIC_KEY = os.environ.get("PAYMENT_PUBLIC_KEY")
MP_PUBLIC_KEY = os.environ.get("PAYMENT_MP_PUBLIC_KEY")


@payment_bp.route('/', methods=['POST', ])
def index():
    amount = request.form.get('amount')
    description = request.form.get('description')
    identification_type = request.form.get('identificationType')
    identification_number = request.form.get('identificationNumber')
    email = request.form.get('email')

    if (amount == '' or description == '' or identification_type not in ('CPF', 'CNPJ') or
            identification_number == '' or email == ''):
        return jsonify({'error': 'Invalid parameters'}), 400

    return render_template('index.html', amount=amount, description=description, email=email,
                           identification_type=identification_type, identification_number=identification_number,
                           payment_mp_public_key=MP_PUBLIC_KEY)


@payment_bp.route('/payment_response', methods=['GET', ])
def payment_response():
    return render_template('response.html')


@payment_bp.route('/payment_error', methods=['GET', ])
def payment_error():
    return render_template('error.html')


@payment_bp.route('/process_payment', methods=['POST', ])
def payment():
    try:
        sdk = mercadopago.SDK(os.getenv("PAYMENT_MP_PRIVATE_KEY"))

        if not request.is_json:
            return jsonify({"error": "Invalid request format. Expected JSON"}), 400

        data = request.get_json()
        purchase_data = data["payer"]["email"] + "|" + data["description"] + "|" + str(data["transaction_amount"])
        idempotency_key = hmac.new(PRIVATE_KEY.encode("utf-8"), purchase_data.encode("utf-8"), hashlib.sha256)

        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': idempotency_key.hexdigest()
        }

        payment_data = {
            "transaction_amount": float(data["transaction_amount"]),
            "token": data["token"],
            "description": data["description"],
            "installments": int(data["installments"]),
            "payment_method_id": data["payment_method_id"],
            "payer": {
                "email": data["payer"]["email"],
                "identification": {
                    "type": data["payer"]["identification"]["type"],
                    "number": data["payer"]["identification"]["number"]
                }
            }
        }

        payment_response = sdk.payment().create(payment_data, request_options)
        payment_body = payment_response["response"]

        if payment_body['status'] == "in_process":
            pass 

        return jsonify(payment_body), 200
    except Exception as e:
        print(f"Error processing payment: {e}")
        return jsonify({"error": str(e)}), 500


@payment_bp.route('/checkout', methods=['GET', ])
def checkout():
    return render_template('checkout.html', public_key=PUBLIC_KEY)
