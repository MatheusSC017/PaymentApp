import mercadopago
import os


class ClientProxy:
    MP_SDK = mercadopago.SDK(os.environ.get("PAYMENT_MP_PRIVATE_KEY"))

    def add_client(self, client):
        response = self.MP_SDK.customer().create(client.get_formatted_data())

        if response["status"] == 201:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def update_client(self, id, client):
        response = self.MP_SDK.customer().update(id, client.get_formatted_data(include_email=False))

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def get_clients(self, email):
        response = self.MP_SDK.customer().search(filters={"email": email})

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def get_client(self, id):
        response = self.MP_SDK.customer().get(id)

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None


if __name__ == "__main__":
    from payment.models.client_model import ClientModel

    client = ClientModel(
        "test@gmail.com", "Jhon", "Doe", "55", "991234567", "CPF", "12345678900",
        "Home", "01234567", "01001000", "Rua Exemplo", 123, {},
        "2021-10-20T11:37:30.000-04:00", "Description del user",  None
    )

    client_proxy = ClientProxy()

    # response = client_proxy.add_client(client)
    # print(response)

    # response = client_proxy.get_clients("test@test.com")
    # print(response)

    response = client_proxy.get_client("2356245804-D6qA5TtnMTdG3O")
    print(response)

    # client.last_name = "Smith"
    # response = client_proxy.update_client("2356245804-D6qA5TtnMTdG3O", client)
    # print(response)
