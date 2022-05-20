from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"))

    response = messenger.send_image(
        image="https://i.imgur.com/Fh7XVYY.jpeg",
        recipient_id="255757xxxxxx",
    )

    print(response)