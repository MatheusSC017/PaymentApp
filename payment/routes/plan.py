from flask import Blueprint, request, render_template, redirect, url_for
from payment.integrations.signatures.signature_plan import SignaturePlanProxy
from payment.models.auto_recurring_model import AutoRecurringModel

plan_bp = Blueprint('plan', __name__, template_folder='templates')
SIGNATURE_PLAN = SignaturePlanProxy()


@plan_bp.route('/plan/register/', methods=['GET', 'POST'])
def register_plan():
    if request.method == "POST":
        data = request.form

        auto_reccurring = AutoRecurringModel(
            frequency=data.get("frequency"),
            frequency_type=data.get("frequency_type"),
            repetitions=data.get("repetitions"),
            billing_day=data.get("billing_day"),
            billing_day_proportional=data.get("billing_day_proportional"),
            free_trial_frequency=data.get("free_trial_frequency"),
            transaction_amount=data.get("transaction_amount"),
            currency_id=data.get("currency_id")
        )

        response = SIGNATURE_PLAN.add_signature_plan(
            reason=data.get("reason"),
            auto_recurring=auto_reccurring,
            back_url=data.get("back_url")
        )

        if response is None:
            return render_template("plan/response.html", response="error", message="Erro durante cadastramento do plano.")

        return redirect(url_for("plan.get_plan", plan_id=response['id']), 302)
    else:
        return render_template("plan/plan_register.html")


@plan_bp.route('/plan/<plan_id>/update/', methods=['GET', 'POST'])
def update_plan(plan_id):
    plan = SIGNATURE_PLAN.get_signature_plan(plan_id)

    if plan is None:
        return render_template("plan/response.html", response="error", message="Erro durante busca do plano.")

    if request.method == "POST":
        data = request.form

        auto_reccurring = AutoRecurringModel(
            frequency=data.get("frequency"),
            frequency_type=data.get("frequency_type"),
            repetitions=data.get("repetitions"),
            billing_day=data.get("billing_day"),
            billing_day_proportional=data.get("billing_day_proportional"),
            free_trial_frequency=data.get("free_trial_frequency"),
            transaction_amount=data.get("transaction_amount"),
            currency_id=data.get("currency_id")
        )

        response = SIGNATURE_PLAN.update_signature_plan(
            id=plan_id,
            reason=data.get("reason"),
            auto_recurring=auto_reccurring,
            back_url=data.get("back_url")
        )

        if response is None:
            return render_template("plan/response.html", response="error",
                                   message="Erro durante atualização do plano.")

        return redirect(url_for("plan.get_plan", plan_id=response['id']), 302)
    else:
        return render_template("plan/plan_register.html", plan=plan)


@plan_bp.route('/plan/', methods=['GET', ])
def get_plans():
    plans = SIGNATURE_PLAN.get_signature_plans()

    if plans is None:
        return render_template("plan/response.html", response="error", message="Erro durante busca dos planos.")

    return render_template("plan/plans.html", subscriptions=plans)


@plan_bp.route('/plan/<plan_id>/', methods=['GET', ])
def get_plan(plan_id):
    plan = SIGNATURE_PLAN.get_signature_plan(plan_id)
    print(plan)
    if plan is None:
        return render_template("plan/response.html", response="error", message="Erro durante busca do plano.")

    return render_template("plan/plan.html", subscription=plan)
