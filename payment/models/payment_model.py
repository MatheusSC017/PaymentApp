class PaymentModel:
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
