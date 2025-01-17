from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv
import pytest


@pytest.mark.asyncio
async def test_sending_location():
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id=getenv("PHONE_NUMBER_ID"))

    response = await messenger.send_location(
        lat=1.29,
        long=103.85,
        name="Singapore",
        address="Singapore",
        recipient_id=getenv("RECIPIENT_ID"),
    )

    assert (response["contacts"][0]["input"] == getenv("RECIPIENT_ID"))
    assert (response["contacts"][0]["wa_id"] == getenv("RECIPIENT_ID"))
    assert (response["messaging_product"] == "whatsapp")
