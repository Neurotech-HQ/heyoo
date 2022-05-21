"""
Unofficial python wrapper for the WhatsApp Cloud API.
"""

import requests


class WhatsApp(object):
    def __init__(self, token=None, phone_number_id=None):
        self.token = token
        self.url = f"https://graph.facebook.com/v13.0/{phone_number_id}/messages"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token),
        }

    def send_message(
        self, message, recipient_id, recipient_type="individual", preview_url=True
    ):
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient_id,
            "type": "text",
            "text": {"preview_url": preview_url, "body": message},
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

    def send_location(self, lat, long, name, address, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "location",
            "location": {
                "latitude": lat,
                "longitude": long,
                "name": name,
                "address": address,
            },
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_image(
        self,
        image,
        recipient_id,
        recipient_type="individual",
        caption=None,
        link=True,
    ):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"link": image, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "image",
                "image": {"id": image, "caption": caption},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_audio(self, audio, recipient_id, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "audio",
                "audio": {"link": audio},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "audio",
                "audio": {"id": audio},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_video(self, video, recipient_id, caption=None, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "video",
                "video": {"link": video, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "video",
                "video": {"id": video, "caption": caption},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def send_document(self, document, recipient_id, caption=None, link=True):
        if link:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "document",
                "document": {"link": document, "caption": caption},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "to": recipient_id,
                "type": "document",
                "document": {"id": document, "caption": caption},
            }
        r = requests.post(self.url, headers=self.headers, json=data)
        return r.json()

    def create_button(self, button):
        return {
            "type": "list",
            "header": {"type": "text", "text": button.get("header")},
            "body": {"text": button.get("body")},
            "footer": {"text": button.get("footer")},
            "action": button.get("action"),
        }

    def send_button(self, button, recipient_id):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_button(button),
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

    def get_interactive_response(self, data):
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["interactive"]["list_reply"]

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
