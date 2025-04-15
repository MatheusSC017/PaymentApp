class CardPaymentModel:
    transaction_amount = None
    token = None
    description = None
    installments = None
    payment_method_id = None
    email = None
    identification_type = None
    identification_number = None

    def __init__(self, transaction_amount, token, description, installments, payment_method_id, email,
                 identification_type, identification_number):
        self.transaction_amount = transaction_amount
        self.token = token
        self.description = description
        self.installments = installments
        self.payment_method_id = payment_method_id
        self.email = email
        self.identification_type = identification_type
        self.identification_number = identification_number

    def get_formatted_data(self):
        return {
            "transaction_amount": self.transaction_amount,
            "token": self.token,
            "description": self.description,
            "installments": self.installments,
            "payment_method_id": self.payment_method_id,
            "payer": {
                "email": self.email,
                "identification": {
                    "type": self.identification_type,
                    "number": self.identification_number,
                },
            },
        }
