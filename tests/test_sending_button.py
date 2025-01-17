from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv
import pytest


@pytest.mark.asyncio
async def test_sending_button():
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id=getenv("PHONE_NUMBER_ID"))

    response = await messenger.send_button(
        recipient_id=getenv("RECIPIENT_ID"),
        button={
            "header": "Header Testing",
            "body": "Body Testing",
            "footer": "Footer Testing",
            "action": {
                "button": "Button Testing",
                "sections": [
                    {
                        "title": "iBank",
                        "rows": [
                            {"id": "row 1", "title": "Send Money", "description": ""},
                            {
                                "id": "row 2",
                                "title": "Withdraw money",
                                "description": "",
                            },
                        ],
                    }
                ],
            },
        },
    )

    assert (response["contacts"][0]["input"] == getenv("RECIPIENT_ID"))
    assert (response["contacts"][0]["wa_id"] == getenv("RECIPIENT_ID"))
    assert (response["messaging_product"] == "whatsapp")
