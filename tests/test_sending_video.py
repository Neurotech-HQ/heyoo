from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv
import pytest


@pytest.mark.asyncio
async def test_sending_video_successful():
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id=getenv("PHONE_NUMBER_ID"))

    response = await messenger.send_video(
        video="https://www.youtube.com/watch?v=K4TOrB7at0Y",
        recipient_id=getenv("RECIPIENT_ID"),
    )

    assert (response["contacts"][0]["input"] == getenv("RECIPIENT_ID"))
    assert (response["contacts"][0]["wa_id"] == getenv("RECIPIENT_ID"))
    assert (response["messaging_product"] == "whatsapp")
