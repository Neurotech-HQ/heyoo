from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv

def test_sending_document():
    load_dotenv()

    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id=getenv("PHONE_NUMBER_ID"))

    response = messenger.send_document(
        document="http://www.africau.edu/images/default/sample.pdf",
        recipient_id=getenv("RECIPIENT_ID"),
    )

    assert(response["contacts"][0]["input"]==getenv("RECIPIENT_ID"))
    assert(response["contacts"][0]["wa_id"]==getenv("RECIPIENT_ID"))
    assert(response["messaging_product"]=="whatsapp")
