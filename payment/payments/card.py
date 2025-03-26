from payment.payments.base import Payment
import mercadopago


class Card(Payment):
    def process_payment(self, payment_data, purchase_identification):
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {'x-idempotency-key': purchase_identification}

        response = self.MP_SDK.payment().create(payment_data.get_formatted_data(), request_options)
        return response["response"]

    def get_payment(self, payment_id, purchase_identification):
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {'x-idempotency-key': purchase_identification}

        return self.MP_SDK.payment().get(payment_id, request_options)["response"]

    @staticmethod
    def validate_purchase_data(decrypted_data, request_data):
        expected_data = [
            request_data["payer"]["identification"]["type"],
            request_data["payer"]["identification"]["number"],
            request_data["payer"]["email"],
            request_data["description"],
            str(request_data["transaction_amount"]),
        ]
        return decrypted_data == expected_data

    @staticmethod
    def validate_form_data(data):
        return (all(data.values()) and
                data['identificationType'] in ('CPF', 'CNPJ') and
                data['amount'].replace('.', '', 1).isdigit())


class PaymentData:
    transaction_amount = None
    token = None
    description = None
    installments = None
    payment_method_id = None
    email = None
    identification_type = None
    identification_number = None

    def __init__(self, transaction_amount, token, description, installments, payment_method_id, email,
                 identification_type, identification_number):
        self.transaction_amount = transaction_amount
        self.token = token
        self.description = description
        self.installments = installments
        self.payment_method_id = payment_method_id
        self.email = email
        self.identification_type = identification_type
        self.identification_number = identification_number

    def get_formatted_data(self):
        return {
            "transaction_amount": self.transaction_amount,
            "token": self.token,
            "description": self.description,
            "installments": self.installments,
            "payment_method_id": self.payment_method_id,
            "payer": {
                "email": self.email,
                "identification": {
                    "type": self.identification_type,
                    "number": self.identification_number,
                },
            },
        }
