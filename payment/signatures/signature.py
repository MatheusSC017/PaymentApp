import requests
import mercadopago
import os


class Signature:
    MP_SDK = mercadopago.SDK(os.environ.get("PAYMENT_MP_PRIVATE_KEY"))

    def add_signature(self, signature_data):
        response = self.MP_SDK.subscription().create(signature_data.get_signature_form())

        if response["status"] == 201:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return {}

    def update_signature(self, signature_id, signature_data):
        response = self.MP_SDK.subscription().update(signature_id, signature_data.get_signature_form())

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return {}

    def get_signatures(self, payer_email):
        response = self.MP_SDK.subscription().search({"payer_email": payer_email})

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return {}

    def get_signature(self, signature_id):
        response = self.MP_SDK.subscription().get(signature_id)

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return {}


class SignatureData:
    plan_id = None
    reason = None
    external_reference = None
    payer_email = None
    card_token_id = None
    frequency = None
    frequency_type = None
    start_date = None
    end_date = None
    transaction_amount = None
    currency_id = None
    back_url = None
    status = None

    def __init__(self, plan_id, reason, external_reference, payer_email, card_token_id,
                 frequency, frequency_type, start_date, end_date, transaction_amount, currency_id, back_url, status):
        self.plan_id = plan_id
        self.reason = reason
        self.external_reference = external_reference
        self.payer_email = payer_email
        self.card_token_id = card_token_id
        self.frequency = frequency
        self.frequency_type = frequency_type
        self.start_date = start_date
        self.end_date = end_date
        self.transaction_amount = transaction_amount
        self.currency_id = currency_id
        self.back_url = back_url
        self.status = status

    def get_signature_form(self):
        return {
            "preapproval_plan_id": self.plan_id,
            "reason": self.reason,
            "external_reference": self.external_reference,
            "payer_email": self.payer_email,
            "card_token_id": self.card_token_id,
            "auto_recurring": {
                "frequency": self.frequency,
                "frequency_type": self.frequency_type,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "transaction_amount": self.transaction_amount,
                "currency_id": self.currency_id
            },
            "back_url": self.back_url,
            "status": self.status
        }


if __name__ == "__main__":
    signature_data = SignatureData(
        "2c93808495b8594f0195ca2b158e0940", "Box Classes", "YG-12345", "test_user@test_user.com",
        "e3ed6f098462036dd2cbabe314b9de2a", 1, "months", "2020-06-02T13:07:14.260Z", "2022-07-20T15:59:52.581Z",
        10, "BRL", "https://github.com/MatheusSC017", "authorized"
    )

    signature = Signature()

    response = signature.add_signature(signature_data)
    print(response)
