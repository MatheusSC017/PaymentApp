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
        return None

    def update_card(self, customer_id, card_id, card_data):
        response = self.MP_SDK.card().update(customer_id, card_id, card_data)
        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def delete_card(self, customer_id, card_id):
        response = self.MP_SDK.card().delete(customer_id, card_id)
        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def get_card_token(self, card_number, expiration_month, expiration_year, security_code, card_holder,
                       identification_type, identification_number):
        card_data = {
            "card_number": card_number,
            "expiration_month": expiration_month,
            "expiration_year": expiration_year,
            "security_code": security_code,
            "cardholder": {
                "name": card_holder,
                "identification": {
                    "type": identification_type,
                    "number": identification_number
                }
            }
        }

        card_token_response = self.MP_SDK.card_token().create(card_data)
        if card_token_response["status"] == 201:
            card_token = card_token_response["response"]["id"]
            return card_token

        print(card_token_response["status"])
        print(card_token_response["response"])
        return None

    def get_card(self, customer_id, card_id):
        response = self.MP_SDK.card().get(customer_id, card_id)
        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def get_cards(self, customer_id):
        response = self.MP_SDK.card().list_all(customer_id)
        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None


if __name__ == "__main__":
    card_proxy = CardProxy()

    card_data = {
        "token": "af30c6e5a5bae0de91cd1296973e54f5"
    }

    # card_response = card_proxy.add_card("2363817186-1wtI295gSu7H7y", card_data)
    # print(card_response)
    #
    # response = card_proxy.get_cards("2363817186-1wtI295gSu7H7y")
    # print(response)
    #
    # response = card_proxy.get_card("2363817186-1wtI295gSu7H7y", "1743418873544")
    # print(response)
    #
    # response = card_proxy.update_card("2363817186-1wtI295gSu7H7y", "1743418873544", card_data)
    # print(response)
    #
    # response = card_proxy.delete_card("2363817186-1wtI295gSu7H7y", "1743418873544")
    # print(response)

    response = card_proxy.get_card_token("5031433215406351", 11, 2030,
                                         "123", "APRO", "CPF", "12345678909")
    print(response)
