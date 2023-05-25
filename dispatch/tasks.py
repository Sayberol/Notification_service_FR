from celery import shared_task
import requests
from dispatch.models import Client
import logging

token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU5MjgxNzQsImlzcyI6ImZhYnJpcXVlIiwibmFtZSI6Imh0dHBzOi8vdC5tZS9zYXliZXJvbCJ9.Xg-JRSBLlx1z-pUzqFPYcTxnpLk1tKA9dZbUh9vPWqk'

logger = logging.getLogger(__name__)


@shared_task
def send_message_async(client_id, message):
    try:
        client = Client.objects.get(id=client_id)
        phone_number = client.phone_number

        url = 'https://probe.fbrq.cloud/v1/send/'
        headers = {
            "Authorization": f'Bearer {token}',
            'Content_Type': 'application/json',
        }
        payload = {
            'phone_number': phone_number,
            'message': message
        }
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            status = response_data.get('status')
            message_id = response_data.get('message_id')

            #Обновление статуса собщения
            client.last_message_status = status
            client.last_message_id = message_id
            client.save()
        else:
            error_message = response.text
            logger.error(f'Ошибка при отправке SMS-сообщения: {error_message}')

    except Client.DoesNotExist:
        logger.warning("Клиент не найден")
