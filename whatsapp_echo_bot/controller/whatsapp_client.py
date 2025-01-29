"""Module that defines the WhatsAppClient class to send messages."""

import json
import logging

import requests

logger = logging.getLogger(__name__)


class WhatsAppClient:
    """WhatsApp API client for sending messages and updating statuses."""

    def __init__(self, base_url: str, api_version: str, api_token: str,
                 phone_id: int) -> None:
        """Inicializa o cliente com o token da API e o ID do telefone."""
        self.api_url = f'{base_url}/{api_version}/{phone_id}/messages'
        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'Content-Type': 'application/json'
        }

    def send_whatsapp_message(self, user_phone: str, message: dict):
        """Sends a WhatsApp message to the specified user."""
        data = {
            'messaging_product': 'whatsapp',
            'to': user_phone
        }
        data.update(message)

        logger.info(
            '(%s) Sending WhatsApp message to user: %s',
            self.__class__.__name__,
            user_phone
        )
        logger.debug(
            '(%s) Message payload: %s',
            self.__class__.__name__,
            json.dumps(data, indent=4, ensure_ascii=False)
        )

        try:
            response = requests.post(
                self.api_url, headers=self.headers, json=data, timeout=10
            )
            if response.ok:
                logger.info(
                    '(%s) Received successful response with status code: %d',
                    self.__class__.__name__,
                    response.status_code
                )
            else:
                logger.warning(
                    ('(%s) Received non-successful response with status code: '
                     '%d'),
                    self.__class__.__name__,
                    response.status_code
                )
            logger.debug(
                '(%s) Response JSON: %s',
                self.__class__.__name__,
                json.dumps(response.json(), indent=4, ensure_ascii=False)
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            logger.exception(
                '(%s) Failed to send WhatsApp message to user: %s.',
                self.__class__.__name__,
                user_phone
            )

    def update_message_whatsapp_status(self, message_id: str):
        """Updates the status of a message as read on WhatsApp."""
        data = {
            'messaging_product': 'whatsapp',
            'status': 'read',
            'message_id': message_id
        }

        logger.info(
            '(%s) Updating the message status: %s',
            self.__class__.__name__,
            message_id
        )
        logger.debug(
            '(%s) Status update payload: %s',
            self.__class__.__name__,
            json.dumps(data, indent=4, ensure_ascii=False)
        )

        try:
            response = requests.post(
                self.api_url, headers=self.headers, json=data, timeout=10
            )
            if response.ok:
                logger.info(
                    '(%s) Received successful response with status code: %d',
                    self.__class__.__name__,
                    response.status_code
                )
            else:
                logger.warning(
                    ('(%s) Received non-successful response with status code: '
                     '%d'),
                    self.__class__.__name__,
                    response.status_code
                )
            logger.debug(
                '(%s) Response JSON: %s',
                self.__class__.__name__,
                json.dumps(response.json(), indent=4, ensure_ascii=False)
            )
            response.raise_for_status()
        except requests.exceptions.RequestException:
            logger.exception(
                '(%s) Failed to update message status: %s.',
                self.__class__.__name__,
                message_id
            )
