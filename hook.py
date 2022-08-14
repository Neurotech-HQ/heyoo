import os
import json
from platform import python_version_tuple
from heyoo import WhatsApp
from dotenv import load_dotenv
from flask import Flask, request, make_response

# Initialize Flask App
app = Flask(__name__)

# Load .env file
load_dotenv()
<<<<<<< HEAD
messenger = WhatsApp(os.getenv("TOKEN"), phone_number_id=os.getenv("PHONE_NUMBER_ID"))
=======

messenger = WhatsApp(os.getenv("TOKEN"),phone_number_id='104xxxxxx')
>>>>>>> dd85c2baf3ce2f83023a69f08f89e242bf29d6ed
VERIFY_TOKEN = "30cca545-3838-48b2-80a7-9e43b1ae8ce4"


@app.route("/", methods=["GET", "POST"])
def hook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            response = make_response(request.args.get("hub.challenge"), 200)
            response.mimetype = "text/plain"
            return response
        return "Invalid verification token"

    data = request.get_json()
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            message_type = messenger.get_message_type(data)

            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                print(f"{name} with this {mobile} number sent  {message}")
                messenger.send_message(f"Hi {name}, nice to connect with you", mobile)

            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                print(message_response)

            else:
                pass
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"


if __name__ == "__main__":
    app.run(port=5000, debug=True)
