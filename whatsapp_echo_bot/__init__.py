"""WhatsApp Echo Bot module."""

from dynaconf import FlaskDynaconf, Validator  # type: ignore[import-untyped]
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

from whatsapp_echo_bot.controller.webhook import webhook_blueprint
from whatsapp_echo_bot.logging.config import setup_logging


def create_app() -> Flask:
    """Create a Flask application instance."""
    app = Flask(__name__)

    # Register blueprints for routing
    app.register_blueprint(webhook_blueprint)

    # Apply ProxyFix middleware to handle proxy headers
    app.wsgi_app = ProxyFix(  # type: ignore[method-assign]
        app.wsgi_app, x_for=1, x_proto=1, x_host=1
    )

    # Load settings from Dynaconf and validate configuration
    FlaskDynaconf(
        load_dotenv=True,
        app=app,
        validators=[
            Validator(
                'FLASK_LOG_LEVEL',
                default='DEBUG',
                is_in={'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'},
            ),
        ],
    )

    setup_logging()
    return app
