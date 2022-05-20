from os import getenv, getenv
from urllib import response
from heyoo import WhatsApp
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"))
    # response = messenger.send_template("hello_world", "255757294146")
    # response = messenger.send_template("sample_happy_hour_announcement", "255757294146")
    # response = messenger.send_image(
    #     image="https://i.imgur.com/Fh7XVYY.jpeg",
    #     recipient_id="255757294146",
    # )
    # response = messenger.send_location(
    #     lat=1.29,
    #     long=103.85,
    #     name="Singapore",
    #     address="Singapore",
    #     recipient_id="255757294146",
    # )
    # response = messenger.send_audio(
    #     audio="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
    #     recipient_id="255757294146",
    # )

    # response = messenger.send_button(
    #     recipient_id="255757294146",
    #     button={
    #         "header": "Header Testing",
    #         "body": "Body Testing",
    #         "footer": "Footer Testing",
    #         "action": {
    #             "button": "Button Testing",
    #             "sections": [
    #                 {
    #                     "title": "iBank",
    #                     "rows": [
    #                         {"id": "row 1", "title": "Send Money", "description": ""},
    #                         {
    #                             "id": "row 2",
    #                             "title": "Withdraw money",
    #                             "description": "",
    #                         },
    #                     ],
    #                 }
    #             ],
    #         },
    #     },
    # )

    # response = messenger.send_document(
    #     document="http://www.africau.edu/images/default/sample.pdf",
    #     recipient_id="255757294146",
    # )

    # response = messenger.send_video(
    #     video="https://www.youtube.com/watch?v=K4TOrB7at0Y",
    #     recipient_id="255757294146",
    # )
    # response = messenger.send_message(
    #     message="https://www.youtube.com/watch?v=K4TOrB7at0Y",
    #     recipient_id="255757294146",
    # )
    print(response)