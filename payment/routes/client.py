from flask import Blueprint, request, render_template, redirect, url_for
from payment.clients.client import ClientProxy, Client
from datetime import datetime


client_bp = Blueprint('client', __name__, template_folder='templates')
CLIENT_PROXY = ClientProxy()


@client_bp.route('/client/register/', methods=['GET', 'POST'])
def register_client():
    if request.method == "POST":
        data = request.form

        client = Client(
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            phone_area_code=data.get("phone_area_code"),
            phone_number=data.get("phone_number"),
            identification_type=data.get("identification_type"),
            identification_number=data.get("identification_number"),
            default_address=data.get("default_address") == "true",  # Optional handling of bool string
            address_id=data.get("address_id"),
            address_zip_code=data.get("address_zip_code"),
            address_street_name=data.get("address_street_name"),
            address_street_number=int(data.get("address_street_number")),
            address_city={},
            date_registered=data.get("date_registered") or str(datetime.today().date()),
            description=data.get("description"),
            default_card=data.get("default_card")
        )

        response = CLIENT_PROXY.add_client(client)

        if response is None:
            return render_template('client/response.html', response="error", message="Erro durante cadastro do cliente.")

        return redirect(url_for("client.get_client", client_id=response["id"]), 302)
    else:
        return render_template("client/client_register.html")


@client_bp.route('/client/<client_id>/update/', methods=['GET', 'POST'])
def update_client(client_id):
    client = CLIENT_PROXY.get_client(client_id)

    if client is None:
        return render_template('client/response.html', response="error", message="Erro durante busca do cliente.")

    if request.method == "POST":
        data = request.form

        client = Client(
            email=data.get("email"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            phone_area_code=data.get("phone_area_code"),
            phone_number=data.get("phone_number"),
            identification_type=data.get("identification_type"),
            identification_number=data.get("identification_number"),
            default_address=data.get("default_address"),
            address_id=data.get("address_id"),
            address_zip_code=data.get("address_zip_code"),
            address_street_name=data.get("address_street_name"),
            address_street_number=int(data.get("address_street_number")),
            address_city={"name": data.get("address_city")},
            date_registered=data.get("date_registered") or str(datetime.today().date()),
            description=data.get("description"),
            default_card=data.get("default_card")
        )

        response = CLIENT_PROXY.update_client(client_id, client)

        if response is None:
            return render_template('client/response.html', response="error",
                                   message="Erro durante atualização do cliente.")

        return redirect(url_for("client.get_client", client_id=response["id"]), 302)
    else:
        return render_template('client/client_register.html', client=client)


@client_bp.route('/client/search/', methods=['GET', 'POST'])
def get_clients():
    if request.method == "POST":
        email = request.form.get("clientEmail")

        clients = CLIENT_PROXY.get_clients(email)

        if clients is None:
            return render_template('client/response.html', response="error", message="Erro durante busca dos clientes.")

        return render_template("client/clients.html", clients=clients)
    else:
        return render_template("client/client_search.html")


@client_bp.route('/client/<client_id>/', methods=['GET', ])
def get_client(client_id):
    client = CLIENT_PROXY.get_client(client_id)

    if client is None:
        return render_template('client/response.html', response="error", message="Erro durante busca do cliente.")

    return render_template("client/client.html", client=client)
