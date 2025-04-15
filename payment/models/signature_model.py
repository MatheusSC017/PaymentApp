class SignatureModel:
    plan_id = None
    reason = None
    external_reference = None
    payer_email = None
    card_token_id = None
    frequency = None
    frequency_type = None
    start_date = None
    end_date = None
    transaction_amount = None
    currency_id = None
    back_url = None
    status = None

    def __init__(self, plan_id, reason, external_reference, payer_email, card_token_id,
                 frequency, frequency_type, start_date, end_date, transaction_amount, currency_id, back_url, status):
        self.plan_id = plan_id
        self.reason = reason
        self.external_reference = external_reference
        self.payer_email = payer_email
        self.card_token_id = card_token_id
        self.frequency = frequency
        self.frequency_type = frequency_type
        self.start_date = start_date
        self.end_date = end_date
        self.transaction_amount = transaction_amount
        self.currency_id = currency_id
        self.back_url = back_url
        self.status = status

    def get_signature_form(self):
        return {
            "preapproval_plan_id": self.plan_id,
            "reason": self.reason,
            "external_reference": self.external_reference,
            "payer_email": self.payer_email,
            "card_token_id": self.card_token_id,
            "auto_recurring": {
                "frequency": self.frequency,
                "frequency_type": self.frequency_type,
                "start_date": self.start_date,
                "end_date": self.end_date,
                "transaction_amount": self.transaction_amount,
                "currency_id": self.currency_id
            },
            "back_url": self.back_url,
            "status": self.status
        }
