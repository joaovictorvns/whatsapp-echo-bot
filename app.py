"""Configures and runs the Flask application for the WhatsApp Echo Bot project."""

import logging.config

from flask import Flask

from logging_config import LOGGING_CONFIG
from src.controller.whatsapp_webhook import register_routes

logging.config.dictConfig(LOGGING_CONFIG)
app = Flask(__name__, template_folder='./src/view/templates')
register_routes(app)

if __name__ == '__main__':
    app.run()
