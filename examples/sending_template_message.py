from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"))

    response = messenger.send_template("hello_world", "255757xxxxxx")

    print(response)