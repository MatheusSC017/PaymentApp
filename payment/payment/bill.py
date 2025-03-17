from payment.payment.base import Payment


class Bill(Payment):
    def process_payment(self, data):
        pass

    def get_payment(self):
        pass

    @staticmethod
    def validate_purchase_data(decrypted_data, request_data):
        pass

    @staticmethod
    def validate_form_data(data):
        pass
