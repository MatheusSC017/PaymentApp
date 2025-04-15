import mercadopago
import os


class SignatureProxy:
    MP_SDK = mercadopago.SDK(os.environ.get("PAYMENT_MP_PRIVATE_KEY"))

    def add_signature(self, signature_data):
        print(signature_data.get_signature_form())
        response = self.MP_SDK.preapproval().create(signature_data.get_signature_form())

        if response["status"] == 201:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def update_signature(self, signature_id, signature_data):
        response = self.MP_SDK.preapproval().update(signature_id, signature_data.get_signature_form())

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def get_signatures(self, payer_email):
        response = self.MP_SDK.preapproval().search({"payer_email": payer_email})

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def get_signature(self, signature_id):
        response = self.MP_SDK.preapproval().get(signature_id)

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None


if __name__ == "__main__":
    from payment.models.signature_model import SignatureModel
    from payment.integrations.card import CardProxy

    card = CardProxy()

    card_token_id = card.get_card_token("5031433215406351", 11, 2030,
                                         "123", "APRO", "CPF", "12345678900")

    signature_data = SignatureModel(
        "2c93808495b8594f0195ca2b158e0940", "Box Classes", "YG-12345", "test@test.com",
        card_token_id, 1, "months", "2025-05-02T13:07:14.260Z", "2026-05-20T15:59:52.581Z",
        10, "BRL", "https://github.com/MatheusSC017", "authorized"
    )

    signature = SignatureProxy()

    response = signature.add_signature(signature_data)
    print(response)
