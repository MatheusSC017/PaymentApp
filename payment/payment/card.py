from payment.payment.base import Payment
import mercadopago


class Card(Payment):
    def process_payment(self, data):
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

        response = self.MP_SDK.payment().create(payment_data, request_options)
        return response["response"]

    def get_payment(self, payment_id, purchase_identification):
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {'x-idempotency-key': purchase_identification}

        return self.MP_SDK.payment().get(payment_id, request_options)["response"]
