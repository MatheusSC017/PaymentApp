import mercadopago
import os


class CardProxy:
    MP_SDK = mercadopago.SDK(os.environ.get("PAYMENT_MP_PRIVATE_KEY"))

    def add_card(self, customer_id, card_data):
        response = self.MP_SDK.card().create(customer_id, card_data)
        if response["status"] == 201:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return {}

    def update_card(self, customer_id, card_id, card_data):
        response = self.MP_SDK.card().update(customer_id, card_id, card_data)
        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return {}

    def delete_card(self, customer_id, card_id):
        response = self.MP_SDK.card().delete(customer_id, card_id)
        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return {}

    def get_card(self, customer_id, card_id):
        response = self.MP_SDK.card().get(customer_id, card_id)
        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return {}

    def get_cards(self, customer_id):
        response = self.MP_SDK.card().list_all(customer_id)
        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return {}


if __name__ == "__main__":
    card_proxy = CardProxy()

    card_data = {
        "token": "af30c6e5a5bae0de91cd1296973e54f5"
    }

    card_response = card_proxy.add_card("2363817186-1wtI295gSu7H7y", card_data)
    print(card_response)

    response = card_proxy.get_cards("2363817186-1wtI295gSu7H7y")
    print(response)

    response = card_proxy.get_card("2363817186-1wtI295gSu7H7y", "1743418873544")
    print(response)

    response = card_proxy.update_card("2363817186-1wtI295gSu7H7y", "1743418873544", card_data)
    print(response)

    response = card_proxy.delete_card("2363817186-1wtI295gSu7H7y", "1743418873544")
    print(response)
