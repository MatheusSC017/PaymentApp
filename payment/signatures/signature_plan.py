import requests
import os


class SignaturePlan:
    BASE_URL = "https://api.mercadopago.com/preapproval_plan/"
    ACCESS_TOKEN = f"Bearer {os.environ.get('PAYMENT_MP_ACCESS_KEY')}"

    def add_signature_plan(self, reason, auto_recurring, back_url):
        headers = {
            "Authorization": self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        data = {
            "reason": reason,
            "auto_recurring": auto_recurring.get_auto_recurring_form(),
            "payment_methods_allowed": {
                "payment_types": [{}],
                "payment_methods": [{}]
            },
            "back_url": back_url
        }

        response = requests.post(self.BASE_URL, json=data, headers=headers)

        if response.status_code == 201:
            return response.json()

        return {}

    def update_signature_plan(self, id, reason, auto_recurring, back_url):
        url = self.BASE_URL + id

        headers = {
            "Authorization": self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        data = {
            "reason": reason,
            "auto_recurring": auto_recurring.get_auto_recurring_form(),
            "payment_methods_allowed": {
                "payment_types": [{}],
                "payment_methods": [{}]
            },
            "back_url": back_url
        }

        response = requests.put(url, json=data, headers=headers)
        if response.status_code == 200:
            return response.json()

        print(response.content)
        return {}

    def get_signature_plans(self):
        url = self.BASE_URL + "search"

        headers = {
            "Authorization": self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()

        print(response.content)
        return {}

    def get_signature_plan(self, id):
        url = self.BASE_URL + id

        headers = {
            "Authorization": self.ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()

        print(response.content)
        return {}


class AutoRecurring:
    frequency = None
    frequency_type = None
    repetitions = None
    billing_day = None
    billing_day_proportional = None
    free_trial_frequency  = None
    transaction_amount = None
    currency_id = None

    def __init__(self, frequency, frequency_type, repetitions, billing_day, billing_day_proportional,
                 free_trial_frequency, transaction_amount, currency_id):
        self.frequency = frequency
        self.frequency_type = frequency_type
        self.repetitions = repetitions
        self.billing_day = billing_day
        self.billing_day_proportional = billing_day_proportional
        self.free_trial_frequency = free_trial_frequency
        self.transaction_amount = transaction_amount
        self.currency_id = currency_id

    def get_auto_recurring_form(self):
        return {
            "frequency": self.frequency,
            "frequency_type": self.frequency_type,
            "repetitions": self.repetitions,
            "billing_day": self.billing_day,
            "billing_day_proportional": self.billing_day_proportional,
            "free_trial": {
                "frequency": self.free_trial_frequency,
                "frequency_type": self.frequency_type,
            },
            "transaction_amount": self.transaction_amount,
            "currency_id": self.currency_id
        }


if __name__ == "__main__":
    auto_reccurring = AutoRecurring(1, "months", 12, 10, True,
                                    1, 10, "BRL")
    signature_plan = SignaturePlan()

    response = signature_plan.add_signature_plan("Yoga Class", auto_reccurring, "https://github.com/MatheusSC017")
    print(response)

    response = signature_plan.get_signature_plans()
    print(response)

    response = signature_plan.update_signature_plan("2c93808495b8594f0195ca2b158e0940", "Box Class", auto_reccurring, "https://github.com/MatheusSC017")
    print(response)

    response = signature_plan.get_signature_plan("2c93808495b8594f0195ca2b158e0940")
    print(response)
