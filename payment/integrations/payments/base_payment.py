from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import mercadopago
import base64
import os


class PaymentProxy:
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
