class AutoRecurringModel:
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
