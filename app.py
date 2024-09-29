"""Configures and runs the Flask application for the WhatsApp Echo Bot project."""

import logging.config

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from logging_config import LOGGING_CONFIG
from src.controller.whatsapp_webhook import register_routes

logging.config.dictConfig(LOGGING_CONFIG)
app = Flask(__name__, template_folder='./src/view/templates')
app.wsgi_app = ProxyFix(  # type: ignore[method-assign]
    app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1
)
register_routes(app)

if __name__ == '__main__':
    app.run()
