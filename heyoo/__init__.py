"""
Unofficial python wrapper for the WhatsApp Cloud API.
"""

import requests

# {
#     "object": "whatsapp_business_account",
#     "entry": [
#         {
#             "id": "115653644479878",
#             "changes": [
#                 {
#                     "value": {
#                         "messaging_product": "whatsapp",
#                         "metadata": {
#                             "display_phone_number": "15550650797",
#                             "phone_number_id": "104469288944395"
#                         },
#                         "contacts": [
#                             {
#                                 "profile": {
#                                     "name": "Jordan Kalebu"
#                                 },
#                                 "wa_id": "255757294146"
#                             }
#                         ],
#                         "messages": [
#                             {
#                                 "from": "255757294146",
#                                 "id": "wamid.HBgMMjU1NzU3Mjk0MTQ2FQIAEhggMEFCRkVCRDlEQzdDQzAwQjNDOTI0QUY5OTk0RTkxNTMA",
#                                 "timestamp": "1653048643",
#                                 "text": {
#                                     "body": "Hi"
#                                 },
#                                 "type": "text"
#                             }
#                         ]
#                     },
#                     "field": "messages"
#                 }
#             ]
#         }
#     ]
# }


class WhatsApp(object):
    def __init__(self, token=None):
        self.token = token
        self.url = "https://graph.facebook.com/v13.0/104469288944395/messages"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token),
        }

    def send_message(self, message, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "text",
            "text": {"body": message},
        }
        r = requests.post(f"{self.url}", headers=self.headers, json=data)
        return r.json()

    def send_template(self, template, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": template,
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_image(self, image_url, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "image",
            "image": {"url": image_url},
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_audio(self, audio_url, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "audio",
            "audio": {"url": audio_url},
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_video(self, video_url, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "video",
            "video": {"url": video_url},
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_file(self, file_url, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "file",
            "file": {"url": file_url},
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_button(self, text, buttons, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {"text": text, "buttons": buttons},
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_generic(self, elements, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {"elements": elements},
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def preprocess(self, data):
        return data["entry"][0]["changes"][0]["value"]

    def get_mobile(self, data):
        data = self.preprocess(data)
        if "contacts" in data:
            return data["contacts"][0]["wa_id"]

    def get_name(self, data):
        contact = self.preprocess(data)
        if contact:
            return contact["contacts"][0]["profile"]["name"]

    def get_message(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["text"]["body"]

    def get_message_id(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["id"]

    def get_message_timestamp(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["timestamp"]

    def get_message_type(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["type"]

    def get_delivery(self, data):
        data = self.preprocess(data)
        if "statuses" in data:
            return data["statuses"][0]["status"]

    def changed_field(self, data):
        return data["entry"][0]["changes"][0]["field"]
