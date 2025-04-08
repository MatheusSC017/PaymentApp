from flask import Blueprint, request, render_template
from payment.clients.client import ClientProxy, Client


client_bp = Blueprint('client', __name__, template_folder='templates')
CLIENT_PROXY = ClientProxy()


@client_bp.route('/client/register/', methods=['GET', 'POST'])
def register_client():
    pass


@client_bp.route('/client/update/', methods=['GET', 'POST'])
def update_client():
    pass


@client_bp.route('/client/search/', methods=['GET', 'POST'])
def get_clients():
    if request.method == "POST":
        email = request.form.get("clientEmail")

        clients = CLIENT_PROXY.get_clients(email)

        return render_template("client/clients.html", clients=clients)
    else:
        return render_template("client/client_search.html")


@client_bp.route('/client/<client_id>/', methods=['GET', ])
def get_client(client_id):
    client = CLIENT_PROXY.get_client(client_id)

    if client is None:
        return render_template('client/response.html', response="error", message="Erro durante busca do cliente.")

    return render_template("client/client.html", client=client)
