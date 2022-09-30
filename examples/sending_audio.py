from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"),phone_number_id=getenv("PHONE_NUMBER_ID"))

    response = messenger.send_audio(
        audio="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        recipient_id="255757xxxxxx",
    )

    print(response)
