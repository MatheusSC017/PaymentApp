from flask import Blueprint, request, render_template, redirect, url_for
from payment.signatures.signature_plan import SignaturePlan
from payment.signatures.signature import Signature, SignatureData
from payment.clients.card import CardProxy
from datetime import datetime, timezone, timedelta

signature_bp = Blueprint('signature', __name__, template_folder='templates')
SIGNATURE = Signature()
SIGNATURE_PLAN = SignaturePlan()
CARD = CardProxy()


@signature_bp.route("/signature/register/", methods=["GET", "POST"])
def register_signature():
    if request.method == "POST":
        data = request.form
        plan = SIGNATURE_PLAN.get_signature_plan(data.get("plan_id"))

        if plan is None:
            return render_template("signature/response.html", response="error",
                                   message="Erro durante busca do plano de assinatura selecionado.")

        start_date = datetime.now(timezone.utc)
        frequency = plan["auto_recurring"]["frequency"]
        frequency_type = plan["auto_recurring"]["frequency_type"]
        if frequency_type == "days":
            end_date = start_date + timedelta(days=frequency)
        else:
            end_date = start_date + timedelta(days=frequency * 30)

        start_date_iso = start_date.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
        end_date_iso = end_date.isoformat(timespec='milliseconds').replace('+00:00', 'Z')

        expiration_year, expiration_month = data.get("card_expiration_data").split("-")
        card_token_id = CARD.get_card_token(data.get("card_number"), int(expiration_month), int(expiration_year),
                                            data.get("card_security_code"), data.get("card_holder"),
                                            data.get("identification_type"), data.get("identification_number"))

        if card_token_id is None:
            return render_template("signature/response.html", response="error",
                                   message="Erro durante criação do token de cartão.")

        signature_data = SignatureData(
            plan_id=plan["id"],
            reason=plan["reason"],
            external_reference=data.get("external_reference"),
            payer_email=data.get("payer_email"),
            card_token_id=card_token_id,
            frequency=frequency,
            frequency_type=frequency_type,
            start_date=start_date_iso,
            end_date=end_date_iso,
            transaction_amount=plan["auto_recurring"]["transaction_amount"],
            currency_id=plan["auto_recurring"]["currency_id"],
            back_url=plan["back_url"],
            status="authorized"
        )

        subscription = SIGNATURE.add_signature(signature_data)

        if subscription is None:
            return render_template("signature/response.html", response="error",
                                   message="Erro durante cadastramento da assinatura.")

        return render_template("signature/signature.html", subscription=subscription)
    else:
        plans = SIGNATURE_PLAN.get_signature_plans()

        if plans is None:
            return render_template("signature/response.html", response="error",
                                   message="Erro durante busca dos planos de assinaturas.")

        plans = [{"id": p["id"], "reason": p["reason"]} for p in plans["results"]]
        return render_template('signature/signature_register.html', plans=plans)


@signature_bp.route("/signature/<signature_id>/update/", methods=["GET", "POST"])
def update_signature(signature_id):
    return "Signature"


@signature_bp.route("/signature/", methods=["GET", "POST"])
def get_signatures():
    if request.method == "POST":
        subscriptions = SIGNATURE.get_signatures(request.form.get("payerEmail"))

        if subscriptions is None:
            return render_template("signature/response.html", response="error", message="Erro durante busca das assinaturas.")

        return render_template("signature/signatures.html", subscriptions=subscriptions)
    else:
        return render_template("signature/signature_search.html")


@signature_bp.route("/signature/<signature_id>/", methods=["GET",])
def get_signature(signature_id):
    subscription = SIGNATURE.get_signature(signature_id)

    if subscription is None:
        return render_template("signature/response.html", response="error",
                               message="Erro durante busca da assinatura.")

    return render_template("signature/signature.html", subscription=subscription)
