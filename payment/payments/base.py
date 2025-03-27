from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import mercadopago
import base64
import os


class Payment:
    PRIVATE_KEY = RSA.importKey(os.environ.get("PAYMENT_PRIVATE_KEY").replace('\\n', '\n'))
    PRIVATE_CIPHER = PKCS1_OAEP.new(PRIVATE_KEY)

    PUBLIC_KEY = RSA.importKey(os.environ.get("PAYMENT_PUBLIC_KEY").replace('\\n', '\n'))
    PUBLIC_CIPHER = PKCS1_OAEP.new(PUBLIC_KEY)

    MP_SDK = mercadopago.SDK(os.environ.get("PAYMENT_MP_PRIVATE_KEY"))
    MP_PUBLIC_KEY = os.environ.get("PAYMENT_MP_PUBLIC_KEY")

    def process_payment(self):
        pass

    def get_payment(self):
        pass

    def encrypt_data(self, purchase_identification):
        cipher_purchase = self.PUBLIC_CIPHER.encrypt(purchase_identification.encode('utf-8'))
        return base64.b64encode(cipher_purchase).decode('utf-8')

    def decrypt_purchase_identification(self, encrypted_data):
        try:
            purchase_identification = self.PRIVATE_CIPHER.decrypt(base64.b64decode(encrypted_data.encode('utf-8'))).decode(
                "utf8")
            return purchase_identification.split(",")
        except Exception as e:
            raise ValueError(f"Failed to decrypt purchase identification: {e}")

    @staticmethod
    def build_purchase_identification(data):
        ordered_fields = [
            data['identificationType'],
            data['identificationNumber'],
            data['email'],
            data['description'],
            data['amount']
        ]
        return ",".join(ordered_fields)


class PaymentData:
    transaction_amount = None
    description = None
    payment_method_id = None
    email = None
    first_name = None
    last_name = None
    identification_type = None
    identification_number = None

    def __init__(self, transaction_amount, description, payment_method_id, email, first_name, last_name,
                 identification_type, identification_number, zip_code, street_name, street_number, neighborhood,
                 city, federal_unit):
        self.transaction_amount = transaction_amount
        self.description = description
        self.payment_method_id = payment_method_id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.identification_type = identification_type
        self.identification_number = identification_number
        self.zip_code = zip_code
        self.street_name = street_name
        self.street_number = street_number
        self.neighborhood = neighborhood
        self.city = city
        self.federal_unit = federal_unit

    def get_formatted_data(self):
        return {
            "transaction_amount": self.transaction_amount,
            "description": self.description,
            "payment_method_id": self.payment_method_id,
            "payer": {
                "email": self.email,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "identification": {
                    "type": self.identification_type,
                    "number": self.identification_number,
                },
                "address": {
                    "zip_code": self.zip_code,
                    "street_name": self.street_name,
                    "street_number": self.street_number,
                    "neighborhood": self.neighborhood,
                    "city": self.city,
                    "federal_unit": self.federal_unit,
                }
            },
        }
