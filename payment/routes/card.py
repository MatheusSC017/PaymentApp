from flask.blueprints import Blueprint
from flask import render_template, request, jsonify
from payment.payments.card import Card, PaymentData
from payment.clients.client import ClientProxy
from payment.clients.card import CardProxy
from time import sleep
import mercadopago
import os


card_bp = Blueprint('card', __name__, template_folder='templates')
MP_SDK = mercadopago.SDK(os.environ.get("PAYMENT_MP_PRIVATE_KEY"))
CARD_PAYMENT = Card()
CARD_PROXY = CardProxy()
CLIENT_PROXY = ClientProxy()


@card_bp.route('/card/', methods=['POST', ])
def payment():
    form_data = {key: request.form.get(key, '').strip() for key in
                 ['amount', 'description', 'identificationType', 'identificationNumber', 'email']}

    if not CARD_PAYMENT.validate_form_data(form_data):
        return jsonify({'error': 'Invalid parameters'}), 400

    try:
        purchase_identification = CARD_PAYMENT.build_purchase_identification(form_data)
        cipher_purchase = CARD_PAYMENT.encrypt_data(purchase_identification)

        return render_template('card/payment_card.html', **form_data,
                               payment_mp_public_key=CARD_PAYMENT.MP_PUBLIC_KEY,
                               purchase_identification=cipher_purchase)
    except Exception as e:
        return jsonify({'error': 'Encryption failed', 'details': str(e)}), 500


@card_bp.route('/card/process_payment/', methods=['POST'])
def process_payment():
    try:
        if not request.is_json:
            print("Invalid request format. Expected JSON")
            return jsonify({"error": "Invalid request format. Expected JSON"}), 400

        data = request.get_json()
        purchase_identification = CARD_PAYMENT.decrypt_purchase_identification(data["purchase_identification"])

        if not CARD_PAYMENT.validate_purchase_data(purchase_identification, data):
            print("Invalid parameters")
            return jsonify({'card/error': 'Invalid parameters'}), 400

        payment_data = PaymentData(
            float(data["transaction_amount"]), data["token"], data["description"], int(data["installments"]),
            data["payment_method_id"], data["payer"]["email"], data["payer"]["identification"]["type"],
            data["payer"]["identification"]["number"],
        )
        payment_response = CARD_PAYMENT.process_payment(payment_data, data["purchase_identification"])

        i = 0
        while payment_response.get('status') == "in_process" or i == 5:
            sleep(1)
            i += 1
            payment_response = CARD_PAYMENT.get_payment(payment_response.get('id'), data["purchase_identification"])

        return jsonify(payment_response), 200
    except ValueError as e:
        print(e)
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        print(f"Error processing payment: {e}")
        return jsonify({"error": "Internal server error"}), 500


@card_bp.route('/card/payment_successful/', methods=['GET', ])
def payment_successful():
    return render_template('card/successful.html')


@card_bp.route('/card/payment_error/', methods=['GET', ])
def payment_error():
    return render_template('card/error.html')


@card_bp.route('/card/register/', methods=['GET', 'POST'])
def register_card():
    if request.method == "POST":
        data = request.get_json()

        response = CLIENT_PROXY.get_clients(data["email"])
        client = response["results"]

        if len(client) == 0:
            return jsonify({"Error": f"Client with e-mail {request.form.get('cardHolderEmail')} not found"}), 404

        card_data = {
            "token": data["token"]
        }
        card = CARD_PROXY.add_card(client[0]["id"], card_data)

        return jsonify(card), 200
    else:
        return render_template('card/card_register.html', payment_mp_public_key=CARD_PAYMENT.MP_PUBLIC_KEY)


@card_bp.route('/card/search/', methods=['GET', 'POST'])
def get_cards():
    if request.method == "POST":
        response = CLIENT_PROXY.get_clients(request.form.get("cardHolderEmail"))
        client = response["results"]

        if len(client) == 0:
            return jsonify({"Error": f"Client with e-mail {request.form.get('cardHolderEmail')} not found"}), 404

        cards = CARD_PROXY.get_cards(client[0]["id"])
        return render_template('card/cards.html', cards=cards)
    else:
        return render_template('card/card_search.html')
