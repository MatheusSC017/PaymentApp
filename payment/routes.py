from flask.blueprints import Blueprint
from flask import render_template, request, jsonify
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import mercadopago
import os
import base64

payment_bp = Blueprint('payment', __name__, template_folder='templates')
PRIVATE_KEY = RSA.importKey(os.environ.get("PAYMENT_PRIVATE_KEY").replace('\\n', '\n'))
PRIVATE_CIPHER = PKCS1_OAEP.new(PRIVATE_KEY)
PUBLIC_KEY = RSA.importKey(os.environ.get("PAYMENT_PUBLIC_KEY").replace('\\n', '\n'))
PUBLIC_CIPHER = PKCS1_OAEP.new(PUBLIC_KEY)
MP_PUBLIC_KEY = os.environ.get("PAYMENT_MP_PUBLIC_KEY")


@payment_bp.route('/', methods=['POST', ])
def payment():
    form_data = {key: request.form.get(key, '').strip() for key in
                 ['amount', 'description', 'identificationType', 'identificationNumber', 'email']}

    if not validate_form_data(form_data):
        return jsonify({'error': 'Invalid parameters'}), 400

    try:
        purchase_identification = build_purchase_identification(form_data)
        cipher_purchase = base64.b64encode(encrypt_data(purchase_identification)).decode('utf-8')

        return render_template('index.html', **form_data,
                               payment_mp_public_key=MP_PUBLIC_KEY,
                               purchase_identification=cipher_purchase)
    except Exception as e:
        return jsonify({'error': 'Encryption failed', 'details': str(e)}), 500


def validate_form_data(data):
    return (all(data.values()) and
            data['identificationType'] in ('CPF', 'CNPJ') and
            data['amount'].replace('.', '', 1).isdigit())


def build_purchase_identification(data):
    ordered_fields = [
        data['identificationType'],
        data['identificationNumber'],
        data['email'],
        data['description'],
        data['amount']
    ]
    return ",".join(ordered_fields)


def encrypt_data(purchase_identification):
    return PUBLIC_CIPHER.encrypt(purchase_identification.encode('utf-8'))


@payment_bp.route('/process_payment', methods=['POST'])
def handle_payment():
    try:
        if not request.is_json:
            print("Invalid request format. Expected JSON")
            return jsonify({"error": "Invalid request format. Expected JSON"}), 400

        data = request.get_json()
        purchase_identification = decrypt_purchase_identification(data["purchase_identification"])

        if not validate_purchase_data(purchase_identification, data):
            print("Invalid parameters")
            return jsonify({'error': 'Invalid parameters'}), 400

        payment_response = process_payment(data)
        if payment_response.get('status') == "in_process":
            pass

        return jsonify(payment_response), 200
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        print(f"Error processing payment: {e}")
        return jsonify({"error": "Internal server error"}), 500


def decrypt_purchase_identification(encrypted_data):
    try:
        purchase_identification = PRIVATE_CIPHER.decrypt(base64.b64decode(encrypted_data.encode('utf-8'))).decode("utf8")
        return purchase_identification.split(",")
    except Exception as e:
        raise ValueError(f"Failed to decrypt purchase identification: {e}")


def validate_purchase_data(decrypted_data, request_data):
    expected_data = [
        request_data["payer"]["identification"]["type"],
        request_data["payer"]["identification"]["number"],
        request_data["payer"]["email"],
        request_data["description"],
        str(request_data["transaction_amount"]),
    ]
    return decrypted_data == expected_data


def process_payment(data):
    sdk = mercadopago.SDK(os.getenv("PAYMENT_MP_PRIVATE_KEY"))
    request_options = mercadopago.config.RequestOptions()
    request_options.custom_headers = {'x-idempotency-key': data["purchase_identification"]}

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
                "number": data["payer"]["identification"]["number"],
            },
        },
    }

    response = sdk.payment().create(payment_data, request_options)
    return response["response"]


@payment_bp.route('/payment_response', methods=['GET', ])
def payment_response():
    return render_template('response.html')


@payment_bp.route('/payment_error', methods=['GET', ])
def payment_error():
    return render_template('error.html')


@payment_bp.route('/checkout', methods=['GET', ])
def checkout():
    return render_template('checkout.html')
