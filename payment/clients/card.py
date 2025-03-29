import mercadopago
import os


class CardProxy:
    MP_SDK = mercadopago.SDK(os.environ.get("PAYMENT_MP_PRIVATE_KEY"))

    def add_card(self, customer_id, card_data):
        card_response = self.MP_SDK.card().create(customer_id, card_data)
        card = card_response["response"]
        return card

    def update_card(self):
        pass

    def delete_card(self):
        pass

    def get_cards(self):
        pass

    def get_card(self):
        pass


if __name__ == "__main__":
    card_proxy = CardProxy()

    sdk = mercadopago.SDK(os.environ.get("PAYMENT_MP_PRIVATE_KEY"))

    customer_data = {
        "email": "test_payer_1234567@gmail.com"
    }
    customer_response = sdk.customer().create(customer_data)
    customer = customer_response["response"]

    card_data = {
        "token": "af30c6e5a5bae0de91cd1296973e54f5"
    }

    response = card_proxy.add_card(customer["id"], card_data)
    print(response)
