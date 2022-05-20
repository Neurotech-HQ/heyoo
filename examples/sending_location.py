from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"))

    response = messenger.send_location(
        lat=1.29,
        long=103.85,
        name="Singapore",
        address="Singapore",
        recipient_id="255757294146",
    )

    print(response)