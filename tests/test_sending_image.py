from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter, Retry
from unittest.mock import patch

def test_sending_image():
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"),phone_number_id=getenv("PHONE_NUMBER_ID"))

    response = messenger.send_image(
        image="https://i.imgur.com/Fh7XVYY.jpeg",
        recipient_id=getenv("RECIPIENT_ID"),
    )

    assert(response["contacts"][0]["input"]==getenv("RECIPIENT_ID"))
    assert(response["contacts"][0]["wa_id"]==getenv("RECIPIENT_ID"))
    assert(response["messaging_product"]=="whatsapp")

@patch.object(requests.Session, 'send')
def test_send_image_retries(mock_send):
    mock_send.side_effect = [requests.exceptions.RequestException] * 2 + [requests.Response()]
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id=getenv("PHONE_NUMBER_ID"))

    response = messenger.send_image(
        image="https://i.imgur.com/Fh7XVYY.jpeg",
        recipient_id=getenv("RECIPIENT_ID"),
    )

    assert mock_send.call_count == 3
