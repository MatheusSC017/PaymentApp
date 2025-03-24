from payment.payment.base import Payment
import mercadopago


class Pix(Payment):
    def process_payment(self, payment_data, purchase_identification):
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {
            'x-idempotency-key': purchase_identification
        }

        payment_response = self.MP_SDK.payment().create(payment_data.get_formatted_data(), request_options)
        return payment_response["status"], payment_response["response"]

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
