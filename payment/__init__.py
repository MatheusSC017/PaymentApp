from flask import Flask
from .routes import payment_bp
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
    app.register_blueprint(payment_bp)
