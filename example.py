from os import getenv, getenv
from urllib import response
from heyoo import WhatsApp
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"))
    # response = messenger.send_template("hello_world", "255757294146")
    response = messenger.send_template("sample_happy_hour_announcement", "255757294146")
    print(response)