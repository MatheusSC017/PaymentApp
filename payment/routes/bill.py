from flask.blueprints import Blueprint
from flask import render_template, request
from payment.payment.bill import Bill

bill_bp = Blueprint('bill', __name__, template_folder='templates')
BILL_PAYMENT = Bill()


@bill_bp.route('/bill/', methods=['POST', ])
def payment():
    form_data = {key: request.form.get(key, '').strip() for key in
                 ['amount', 'description', 'identificationType', 'identificationNumber', 'email', 'returnLink']}

    return render_template('bill/bill.html', **form_data,
                           payment_mp_public_key=BILL_PAYMENT.MP_PUBLIC_KEY,)
