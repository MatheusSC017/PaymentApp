from flask import Flask
from .routes.pix import pix_bp
from .routes.card import card_bp
from .routes.bill import bill_bp
from .routes.checkout import checkout_bp
from .routes.client import client_bp
from .routes.plan import plan_bp
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    configure_app(app)
    initialize_routes(app)
    return app


def configure_app(app):
    mercado_pago_key = os.getenv('MERCADO_PAGO_KEY')

    if not mercado_pago_key:
        raise ValueError("Missing required configuration values")

    app.config.from_mapping(
        MERCADO_PAGO_KEY=mercado_pago_key
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


def initialize_routes(app):
    app.register_blueprint(card_bp)
    app.register_blueprint(pix_bp)
    app.register_blueprint(bill_bp)
    app.register_blueprint(checkout_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(plan_bp)
