"""This module implements the WhatsApp webhook."""

import json
import logging

from flask import Blueprint, current_app, request

from whatsapp_echo_bot.controller import webhook_utils
from whatsapp_echo_bot.controller.whatsapp_client import WhatsAppClient

logger = logging.getLogger(__name__)
webhook_blueprint = Blueprint('webhook', __name__)


@webhook_blueprint.route('/webhook', methods=['POST', 'GET'])
def webhook():
    """Handles incoming requests to the webhook."""
    match request.method:
        case 'GET':
            return handle_get_request()
        case 'POST':
            return handle_post_request()


def handle_get_request():
    """Handles GET requests for webhook verification."""
    logger.info('Received a GET request at webhook endpoint')

    expected_token = current_app.config['WEBHOOK_VERIFICATION_TOKEN']

    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    logger.debug(
        'GET request parameters: mode=%s, token=%s, challenge=%s',
        mode,
        f'{token[:3]}...{token[-3:]}',
        challenge
    )

    if mode == 'subscribe' and token == expected_token:
        logger.info('Webhook verification successful')
        return challenge, 200
    logger.warning('Webhook verification failed. Invalid token or mode')
    return '', 400


def handle_post_request():
    """Handles POST requests to the webhook."""
    logger.info('Received a POST request at webhook endpoint')

    base_url = current_app.config['WA_BASE_URL']
    api_version = current_app.config['WA_CLOUD_API_VERSION']
    api_token = current_app.config['WA_CLOUD_API_ACCESS_TOKEN']
    app_secret = current_app.config['M4D_APP_SECRET']
    phone_id = current_app.config['WA_PHONE_NUMBER_ID']

    wa_client = WhatsAppClient(base_url, api_version, api_token, phone_id)

    if request.headers.get('User-Agent') != 'facebookexternalua':
        logger.warning(
            'Invalid User-Agent: %s', request.headers.get('User-Agent')
        )
        return '', 400

    if not webhook_utils.is_valid_facebook_ipv6(
        request.headers.get('X-Forwarded-For')
    ):
        logger.warning(
            'Invalid IP address: %s', request.headers.get('X-Forwarded-For')
        )
        return '', 400

    if not webhook_utils.verify_signature(
        request.get_data(), request.headers, app_secret
    ):
        logger.warning('Invalid signature')
        return '', 401

    logger.debug(
        'Received JSON payload: %s',
        json.dumps(request.json, indent=4, ensure_ascii=False)
    )

    messages = request.json['entry'][0]['changes'][0]['value'].get('messages')
    if messages:
        webhook_utils.update_message_whatsapp_status(messages[0], wa_client)
        webhook_utils.echo_message_whatsapp(
            messages[0]['from'], messages[0], wa_client
        )
    return '', 200
