"""Module that manages the WhatsApp webhook, receiving and processing messages."""

import os
import json
import logging

from flask import Flask, request, render_template
from dotenv import load_dotenv

from logging_config import LOGGER_NAME
from src.model.whatsapp_client import WhatsAppClient

load_dotenv('./config/.env')
logger = logging.getLogger(f'{LOGGER_NAME}.{__name__}')

api_token = os.environ['WHATSAPP_API_TOKEN']
verify_token = os.environ['WHATSAPP_VERIFICATION_TOKEN']
phone_id = os.environ['WHATSAPP_BUSINESS_PHONE_NUMBER_ID']

wa_client = WhatsAppClient(api_token, phone_id)


def register_routes(app: Flask):
    """Registers the webhook routes and the privacy policy and terms of service pages."""
    app.route('/webhook', methods=['POST', 'GET'])(webhook)
    app.route('/privacy_policy')(privacy_policy)
    app.route('/terms_of_service')(terms_of_service)


def echo_message_whatsapp(user_phone: str, user_message: dict):
    """Repeats the message received from a user on WhatsApp."""
    message_type = user_message['type']
    message = {'type': message_type}
    if user_message.get('context'):
        message.update({'context': {'message_id': user_message['context']['id']}})
    match message_type:
        case 'text':
            message.update({message_type: user_message[message_type]})
            message[message_type].update({'preview_url': True})
            wa_client.send_whatsapp_message(user_phone, message)
        case 'image':
            message.update({message_type: {'id': user_message[message_type]['id']}})
            if user_message[message_type].get('caption'):
                message[message_type].update({'caption': user_message[message_type]['caption']})
            wa_client.send_whatsapp_message(user_phone, message)
        case 'audio':
            message.update({message_type: {'id': user_message[message_type]['id']}})
            wa_client.send_whatsapp_message(user_phone, message)
        case 'video':
            message.update({message_type: {'id': user_message[message_type]['id']}})
            caption = user_message[message_type].get('caption')
            if caption:
                message[message_type].update({'caption': caption})
            wa_client.send_whatsapp_message(user_phone, message)
        case 'document':
            message.update(
                {
                    message_type: {
                        'id': user_message[message_type]['id'],
                        'filename': user_message[message_type]['filename']
                    }
                }
            )
            if user_message[message_type].get('caption'):
                message[message_type].update({'caption': user_message[message_type]['caption']})
            wa_client.send_whatsapp_message(user_phone, message)
        case 'contacts':
            message.update({message_type: user_message[message_type]})
            wa_client.send_whatsapp_message(user_phone, message)
        case 'sticker':
            message.update(
                {
                    'recipient_type': 'individual',
                    message_type: {'id': user_message[message_type]['id']}
                }
            )
            wa_client.send_whatsapp_message(user_phone, message)
        case 'location':
            message.update(
                {
                    message_type: {
                        'latitude': user_message[message_type]['latitude'],
                        'longitude': user_message[message_type]['longitude']
                    }
                }
            )
            name = user_message[message_type].get('name')
            if name:
                message[message_type].update({'name': name})
            address = user_message[message_type].get('address')
            if address:
                message[message_type].update({'address': address})
            wa_client.send_whatsapp_message(user_phone, message)
        case 'reaction':
            message.update({message_type: user_message[message_type]})
            wa_client.send_whatsapp_message(user_phone, message)
        case 'unsupported':
            message['type'] = 'text'
            # TODO: Add multi-language support.
            message.update(
                {
                    'text': {
                        'body': 'Desculpe, o tipo da mensagem que você enviou não é suportado.'
                    }
                }
            )
            wa_client.send_whatsapp_message(user_phone, message)


def webhook():  # pylint: disable=inconsistent-return-statements
    """Handles incoming requests to the webhook."""
    if request.method == 'GET':
        logger.info('Received a GET request at webhook endpoint')

        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')

        logger.debug(
            'GET request parameters: mode=%s, token=%s, challenge=%s',
            mode,
            token,
            challenge
        )

        if mode == 'subscribe' and token == verify_token:
            logger.info('Webhook verification successful')
            return challenge, 200
        logger.warning('Webhook verification failed. Invalid token or mode')
        return '', 400
    if request.method == 'POST':
        logger.info('Received a POST request at webhook endpoint')
        logger.debug(
            'Received JSON payload: %s',
            json.dumps(request.json, indent=4, ensure_ascii=False)
        )

        messages = request.json['entry'][0]['changes'][0]['value'].get('messages')
        if messages:
            if messages[0]['type'] != 'unsupported':
                wa_client.update_message_whatsapp_status(messages[0]['id'])
            echo_message_whatsapp(messages[0]['from'], messages[0])
        return '', 200


def privacy_policy():
    """Returns to the privacy policy page."""
    return render_template('privacy_policy.html')


def terms_of_service():
    """Returns to the terms of service page."""
    return render_template('terms_of_service.html')
