import mercadopago
import os


class SignaturePlanProxy:
    MP_SDK = mercadopago.SDK(os.environ.get("PAYMENT_MP_PRIVATE_KEY"))

    def add_signature_plan(self, reason, auto_recurring, back_url):
        data = {
            "reason": reason,
            "auto_recurring": auto_recurring.get_auto_recurring_form(),
            "payment_methods_allowed": {
                "payment_types": [{}],
                "payment_methods": [{}]
            },
            "back_url": back_url
        }

        response = self.MP_SDK.plan().create(data)

        if response["status"] == 201:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def update_signature_plan(self, id, reason, auto_recurring, back_url):
        data = {
            "reason": reason,
            "auto_recurring": auto_recurring.get_auto_recurring_form(),
            "payment_methods_allowed": {
                "payment_types": [{}],
                "payment_methods": [{}]
            },
            "back_url": back_url
        }

        response = self.MP_SDK.plan().update(id, data)

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def get_signature_plans(self):
        response = self.MP_SDK.plan().search()

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None

    def get_signature_plan(self, id):
        if id == "search":
            return None

        response = self.MP_SDK.plan().get(id)

        if response["status"] == 200:
            return response["response"]

        print(response["status"])
        print(response["response"])
        return None


if __name__ == "__main__":
    from payment.models.auto_recurring_model import AutoRecurringModel
    auto_reccurring = AutoRecurringModel(1, "months", 12, 10, True, 1, 10, "BRL")
    signature_plan = SignaturePlanProxy()

    response = signature_plan.add_signature_plan("Yoga Class", auto_reccurring, "https://github.com/MatheusSC017")
    print(response)

    response = signature_plan.get_signature_plans()
    print(response)

    response = signature_plan.update_signature_plan("2c93808495b8594f0195ca2b158e0940", "Box Class", auto_reccurring, "https://github.com/MatheusSC017")
    print(response)

    response = signature_plan.get_signature_plan("2c93808495b8594f0195ca2b158e0940")
    print(response)
