"""Docstring."""

import hashlib
import hmac
import logging

from whatsapp_echo_bot.controller.whatsapp_client import WhatsAppClient

logger = logging.getLogger(__name__)


def echo_message_whatsapp(  # noqa: C901, PLR0912, PLR0915
        user_phone: str, user_message: dict, wa_client: WhatsAppClient
) -> None:
    """Repeats the message received from a user on WhatsApp."""
    message_type = user_message['type']
    message = {'type': message_type}

    if user_message.get('context'):
        message.update(
            {'context': {'message_id': user_message['context']['id']}}
        )

    match message_type:
        case 'text':
            message.update({message_type: user_message[message_type]})
            message[message_type].update({'preview_url': True})
            wa_client.send_whatsapp_message(user_phone, message)
        case 'image':
            message.update(
                {message_type: {'id': user_message[message_type]['id']}}
            )
            if user_message[message_type].get('caption'):
                message[message_type].update(
                    {'caption': user_message[message_type]['caption']}
                )
            wa_client.send_whatsapp_message(user_phone, message)
        case 'audio':
            message.update(
                {message_type: {'id': user_message[message_type]['id']}}
            )
            wa_client.send_whatsapp_message(user_phone, message)
        case 'video':
            message.update(
                {message_type: {'id': user_message[message_type]['id']}}
            )
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
                message[message_type].update(
                    {'caption': user_message[message_type]['caption']}
                )
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
                        'body': ('Desculpe, o tipo da mensagem que você enviou'
                                 ' não é suportado.')
                    }
                }
            )
            wa_client.send_whatsapp_message(user_phone, message)


def update_message_whatsapp_status(
        user_message: dict, wa_client: WhatsAppClient
) -> None:
    """Docstring."""
    if user_message['type'] != 'unsupported':
        wa_client.update_message_whatsapp_status(user_message['id'])


def verify_signature(data: bytes, headers: dict, app_secret_key: str) -> bool:
    """Docstring."""
    signature_sha1 = headers.get('X-Hub-Signature', '').split('=')[1]
    signature_sha256 = headers.get('X-Hub-Signature-256', '').split('=')[1]

    generated_sha1 = hmac.new(
        app_secret_key.encode('utf-8'),
        data,
        hashlib.sha1
    ).hexdigest()
    generated_sha256 = hmac.new(
        app_secret_key.encode('utf-8'),
        data,
        hashlib.sha256
    ).hexdigest()

    is_signature_sha1_valid = hmac.compare_digest(
        generated_sha1, signature_sha1
    )
    is_signature_sha256_valid = hmac.compare_digest(
        generated_sha256, signature_sha256
    )

    return is_signature_sha1_valid and is_signature_sha256_valid


def is_valid_facebook_ipv6(client_ip: str) -> bool:
    """Docstring."""
    return client_ip.startswith('2a03:2880:')
