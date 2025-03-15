from payment.payment.base import Payment
import mercadopago


class Pix(Payment):
    def process_payment(self, data):
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': data["purchase_identification"]
        }

        payment_data = {
            "transaction_amount": float(data["transactionAmount"]),
            "description": data["description"],
            "payment_method_id": "pix",
            "payer": {
                "email": data["email"],
                "first_name": data["payerFirstName"],
                "last_name": data["payerLastName"],
                "identification": {
                    "type": data["identificationType"],
                    "number": data["identificationNumber"],
                },
                "address": {
                    "zip_code": "06233-200",
                    "street_name": "Av. das Nações Unidas",
                    "street_number": "3003",
                    "neighborhood": "Bonfim",
                    "city": "Osasco",
                    "federal_unit": "SP"
                }
            }
        }

        payment_response = self.MP_SDK.payment().create(payment_data, request_options)
        payment = payment_response["response"]

        return payment

    def get_payment(self):
        pass

    @staticmethod
    def validate_purchase_data(decrypted_data, request_data):
        expected_data = [
            request_data["identificationType"],
            request_data["identificationNumber"],
            request_data["email"],
            request_data["description"],
            str(request_data["transactionAmount"]),
        ]
        return decrypted_data == expected_data

    @staticmethod
    def validate_form_data(data):
        return (all(data.values()) and
                data['identificationType'] in ('CPF', 'CNPJ') and
                data['amount'].replace('.', '', 1).isdigit())
