import requests
import mercadopago
import os


class ClientProxy:
    BASE_URL = "https://api.mercadopago.com/v1/customers/"
    ACCESS_TOKEN = f"Bearer {os.environ.get('PAYMENT_MP_ACCESS_KEY')}"

    def add_client(self, client):
        headers = {
            "Authorization": self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        response = requests.post(self.BASE_URL, json=client.get_formatted_data(), headers=headers)

        if response.status_code == 201:
            return response.json()

        print(response.status_code)
        print(response.content)
        return {}

    def update_client(self, id, client):
        url = self.BASE_URL + id
        headers = {
            "Authorization": self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        response = requests.put(url, json=client.get_formatted_data(include_email=False), headers=headers)
        if response.status_code == 200:
            return response.json()

        print(response.status_code)
        print(response.content)
        return {}

    def get_clients(self, email):
        url = self.BASE_URL + "search"
        headers = {
            "Authorization": self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        response = requests.get(url, params={"email": email}, headers=headers)
        if response.status_code == 200:
            return response.json()

        print(response.status_code)
        print(response.content)
        return {}

    def get_client(self, id):
        url = self.BASE_URL + id
        headers = {
            "Authorization": self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()

        print(response.status_code)
        print(response.content)
        return {}


class Client:
    email = None
    first_name = None
    last_name = None
    phone_area_code = None
    phone_number = None
    identification_type = None
    identification_number = None
    default_address = None
    address_id = None
    address_zip_code = None
    address_street_name = None
    address_street_number = None
    address_city = None
    date_registered = None
    description = None
    default_card = None

    def __init__(self, email, first_name, last_name, phone_area_code, phone_number, identification_type,
                 identification_number, default_address, address_id, address_zip_code, address_street_name,
                 address_street_number, address_city, date_registered, description, default_card):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.phone_area_code = phone_area_code
        self.phone_number = phone_number
        self.identification_type = identification_type
        self.identification_number = identification_number
        self.default_address = default_address
        self.address_id = address_id
        self.address_zip_code = address_zip_code
        self.address_street_name = address_street_name
        self.address_street_number = address_street_number
        self.address_city = address_city
        self.date_registered = date_registered
        self.description = description
        self.default_card = default_card

    def get_formatted_data(self, include_email=True):
        formatted_data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": {
                "area_code": self.phone_area_code,
                "number": self.phone_number
            },
            "identification": {
                "type": self.identification_type,
                "number": self.identification_number
            },
            "default_address": self.default_address,
            "address": {
                "id": self.address_id,
                "zip_code": self.address_zip_code,
                "street_name": self.address_street_name,
                "street_number": self.address_street_number,
                "city": self.address_city
            },
            "date_registered": self.date_registered,
            "description": self.description,
            "default_card": self.default_card
        }
        if include_email:
            formatted_data["email"] = self.email
        return formatted_data


if __name__ == "__main__":
    client = Client(
        "test@test.com", "Jhon", "Doe", "55", "991234567", "CPF", "12345678900",
        "Home", "01234567", "01001000", "Rua Exemplo", 123, {},
        "2021-10-20T11:37:30.000-04:00", "Description del user",  None
    )

    client_proxy = ClientProxy()

    # response = client_proxy.add_client(client)
    # print(response)

    # response = client_proxy.get_clients("test@test.com")
    # print(response)

    response = client_proxy.get_client("2356245804-DEYZ4CxwkJKxXv")
    print(response)

    client.last_name = "Smith"
    response = client_proxy.update_client("2356245804-DEYZ4CxwkJKxXv", client)
    print(response)
