"""
Unofficial python wrapper for the WhatsApp Cloud API.
"""
import os
import mimetypes
import requests
import logging
from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Optional, Dict, Any, List, Union, Tuple, Callable


# Setup logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


class WhatsApp(object):
    """ "
    WhatsApp Object
    """

    def __init__(self, token=None, phone_number_id=None):
        """
        Initialize the WhatsApp Object

        Args:
            token[str]: Token for the WhatsApp cloud API obtained from the developer portal
            phone_number_id[str]: Phone number id for the WhatsApp cloud API obtained from the developer portal
        """
        self.token = token
        self.phone_number_id = phone_number_id
        self.base_url = "https://graph.facebook.com/v14.0"
        self.url = f"{self.base_url}/{phone_number_id}/messages"

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {}".format(self.token),
        }

    def send_message(
        self, message, recipient_id, recipient_type="individual", preview_url=True
    ):
        """
         Sends a text message to a WhatsApp user

         Args:
                message[str]: Message to be sent to the user
                recipient_id[str]: Phone number of the user with country code wihout +
                recipient_type[str]: Type of the recipient, either individual or group
                preview_url[bool]: Whether to send a preview url or not

        Example:
            ```python
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_message("Hello World", "5511999999999")
            >>> whatsapp.send_message("Hello World", "5511999999999", preview_url=False)

        """
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient_id,
            "type": "text",
            "text": {"preview_url": preview_url, "body": message},
        }
        logging.info(f"Sending message to {recipient_id}")
        r = requests.post(f"{self.url}", headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Message sent to {recipient_id}")
            return r.json()
        logging.info(f"Message not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return r.json()

    def reply_to_message(
        self, message_id: str, recipient_id: str, message: str, preview_url: bool = True
    ):
        """
        Replies to a message

        Args:
            message_id[str]: Message id of the message to be replied to
            recipient_id[str]: Phone number of the user with country code wihout +
            message[str]: Message to be sent to the user
            preview_url[bool]: Whether to send a preview url or not
        """
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "text",
            "context": {"message_id": message_id},
            "text": {"preview_url": preview_url, "body": message},
        }

        logging.info(f"Replying to {message_id}")
        r = requests.post(f"{self.url}", headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Message sent to {recipient_id}")
            return r.json()
        logging.info(f"Message not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return r.json()

    def send_template(self, template, recipient_id, lang="en_US", components={}):
        """
        Sends a template message to a WhatsApp user, Template messages can either be;
            1. Text template
            2. Media based template
            3. Interactive template

        You can customize the template message by passing a dictionary of components.

        You can find the available components in the documentation.
        https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates

        Args:
            template[str]: Template name to be sent to the user
            recipient_id[str]: Phone number of the user with country code wihout +
            lang[str]: Language of the template message
            components[dict]: Dictionary of components to be sent to the user


        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_template("hello_world", "5511999999999", lang="en_US"))
        """
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {
                "name": template,
                "language": {"code": lang},
                "components": components,
            },
        }
        logging.info(f"Sending template to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Template sent to {recipient_id}")
            return r.json()
        logging.info(f"Template not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return r.json()

    def send_templatev2(self, template, recipient_id, components, lang="en_US"):
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "template",
            "template": {
                "name": template,
                "language": {"code": lang},
                "components": components,
            },
        }
        logging.info(f"Sending template to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Template sent to {recipient_id}")
            return r.json()
        logging.info(f"Template not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return r.json()

    def send_location(self, lat, long, name, address, recipient_id):
        """
        Sends a location message to a WhatsApp user

        Args:
            lat[str]: Latitude of the location
            long[str]: Longitude of the location
            name[str]: Name of the location
            address[str]: Address of the location
            recipient_id[str]: Phone number of the user with country code wihout +

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_location("-23.564", "-46.654", "My Location", "Rua dois, 123", "5511999999999")
        """
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
        logging.info(f"Sending location to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Location sent to {recipient_id}")
            return r.json()
        logging.info(f"Location not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(r.json())
        return r.json()

    def send_image(
        self,
        image,
        recipient_id,
        recipient_type="individual",
        caption=None,
        link=True,
    ):
        """
        Sends an image message to a WhatsApp user

        There are two ways to send an image message to a user, either by passing the image id or by passing the image link.
        Image id is the id of the image uploaded to the cloud api.

        Args:
            image[str]: Image id or link of the image
            recipient_id[str]: Phone number of the user with country code wihout +
            recipient_type[str]: Type of the recipient, either individual or group
            caption[str]: Caption of the image
            link[bool]: Whether to send an image id or an image link, True means that the image is an id, False means that the image is a link


        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_image("https://i.imgur.com/Fh7XVYY.jpeg", "5511999999999")
        """
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
        logging.info(f"Sending image to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Image sent to {recipient_id}")
            return r.json()
        logging.info(f"Image not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(r.json())
        return r.json()

    def send_sticker(self, sticker: str, recipient_id: str, linl=True):
        pass

    def send_audio(self, audio, recipient_id, link=True):
        """
        Sends an audio message to a WhatsApp user
        Audio messages can either be sent by passing the audio id or by passing the audio link.

        Args:
            audio[str]: Audio id or link of the audio
            recipient_id[str]: Phone number of the user with country code wihout +
            link[bool]: Whether to send an audio id or an audio link, True means that the audio is an id, False means that the audio is a link

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3", "5511999999999")
        """
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
        logging.info(f"Sending audio to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Audio sent to {recipient_id}")
            return r.json()
        logging.info(f"Audio not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(f"Response: {r.json()}")
        return r.json()

    def send_video(self, video, recipient_id, caption=None, link=True):
        """ "
        Sends a video message to a WhatsApp user
        Video messages can either be sent by passing the video id or by passing the video link.

        Args:
            video[str]: Video id or link of the video
            recipient_id[str]: Phone number of the user with country code wihout +
            caption[str]: Caption of the video
            link[bool]: Whether to send a video id or a video link, True means that the video is an id, False means that the video is a link

        example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ", "5511999999999")
        """
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
        logging.info(f"Sending video to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Video sent to {recipient_id}")
            return r.json()
        logging.info(f"Video not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(f"Response: {r.json()}")
        return r.json()

    def send_document(self, document, recipient_id, caption=None, link=True):
        """ "
        Sends a document message to a WhatsApp user
        Document messages can either be sent by passing the document id or by passing the document link.

        Args:
            document[str]: Document id or link of the document
            recipient_id[str]: Phone number of the user with country code wihout +
            caption[str]: Caption of the document
            link[bool]: Whether to send a document id or a document link, True means that the document is an id, False means that the document is a link

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_document("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf", "5511999999999")
        """
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

        logging.info(f"Sending document to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Document sent to {recipient_id}")
            return r.json()
        logging.info(f"Document not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(f"Response: {r.json()}")
        return r.json()

    def send_contacts(self, contacts: List[Dict[Any, Any]], recipient_id: str):
        """send_contacts

        Send a list of contacts to a user

        Args:
            contacts(List[Dict[Any, Any]]): List of contacts to send
            recipient_id(str): Phone number of the user with country code wihout +

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> contacts = [{
                "addresses": [{
                    "street": "STREET",
                    "city": "CITY",
                    "state": "STATE",
                    "zip": "ZIP",
                    "country": "COUNTRY",
                    "country_code": "COUNTRY_CODE",
                    "type": "HOME"
                    },
                ....
                }
            ]

        REFERENCE: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/messages#contacts-object
        """

        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "contacts",
            "contacts": contacts,
        }
        logging.info(f"Sending contacts to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Contacts sent to {recipient_id}")
            return r.json()
        logging.info(f"Contacts not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(f"Response: {r.json()}")
        return r.json()

    def upload_media(self, media: str):
        """
        Uploads a media to the cloud api and returns the id of the media

        Args:
            media[str]: Path of the media to be uploaded

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.upload_media("/path/to/media")

        REFERENCE: https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media#
        """
        form_data = {
            "file": (
                media,
                open(os.path.realpath(media), "rb"),
                mimetypes.guess_type(media)[0],
            ),
            "messaging_product": "whatsapp",
            "type": mimetypes.guess_type(media)[0],
        }
        form_data = MultipartEncoder(fields=form_data)
        headers = self.headers.copy()
        headers["Content-Type"] = form_data.content_type
        logging.info(f"Content-Type: {form_data.content_type}")
        logging.info(f"Uploading media {media}")
        r = requests.post(
            f"{self.base_url}/{self.phone_number_id}/media",
            headers=self.headers,
            data=form_data,
        )
        if r.status_code == 200:
            logging.info(f"Media {media} uploaded")
            return r.json()
        logging.info(f"Error uploading media {media}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return None

    def delete_media(self, media_id: str):
        """
        Deletes a media from the cloud api

        Args:
            media_id[str]: Id of the media to be deleted
        """
        logging.info(f"Deleting media {media_id}")
        r = requests.delete(f"{self.base_url}/{media_id}", headers=self.headers)
        if r.status_code == 200:
            logging.info(f"Media {media_id} deleted")
            return r.json()
        logging.info(f"Error deleting media {media_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return None

    def create_button(self, button):
        """
        Method to create a button object to be used in the send_message method.

        This is method is designed to only be used internally by the send_button method.

        Args:
               button[dict]: A dictionary containing the button data
        """
        data = {
            "type": "list",
            "action": button.get("action")
        }
        if button.get("header"):
            data["header"] = {"type": "text", "text": button.get("header")}
        if button.get("body"):
            data["body"] = {"text": button.get("body")}
        if button.get("footer"):
            data["footer"] = {"text": button.get("footer")}
        return data

    def send_button(self, button, recipient_id):
        """
        Sends an interactive buttons message to a WhatsApp user

        Args:
            button[dict]: A dictionary containing the button data(rows-title may not exceed 20 characters)
            recipient_id[str]: Phone number of the user with country code wihout +

        check https://github.com/Neurotech-HQ/heyoo#sending-interactive-reply-buttons for an example.
        """
        data = {
            "messaging_product": "whatsapp",
            "to": recipient_id,
            "type": "interactive",
            "interactive": self.create_button(button),
        }
        logging.info(f"Sending buttons to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Buttons sent to {recipient_id}")
            return r.json()
        logging.info(f"Buttons not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return r.json()

    def send_reply_button(self, button, recipient_id):
        """
        Sends an interactive reply buttons[menu] message to a WhatsApp user

        Args:
            button[dict]: A dictionary containing the button data
            recipient_id[str]: Phone number of the user with country code wihout +

        Note:
            The maximum number of buttons is 3, more than 3 buttons will rise an error.
        """
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient_id,
            "type": "interactive",
            "interactive": button,
        }
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Reply buttons sent to {recipient_id}")
            return r.json()
        logging.info(f"Reply buttons not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return r.json()

    def query_media_url(self, media_id: str):
        """
        Query media url from media id obtained either by manually uploading media or received media

        Args:
            media_id[str]: Media id of the media

        Returns:
            str: Media url

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.query_media_url("media_id")
        """

        logging.info(f"Querying media url for {media_id}")
        r = requests.get(f"{self.base_url}/{media_id}", headers=self.headers)
        if r.status_code == 200:
            logging.info(f"Media url queried for {media_id}")
            return r.json()["url"]
        logging.info(f"Media url not queried for {media_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return None

    def download_media(self, media_url: str, mime_type: str, file_path: str = "temp"):
        """
        Download media from media url obtained either by manually uploading media or received media

        Args:
            media_url[str]: Media url of the media
            mime_type[str]: Mime type of the media
            file_path[str]: Path of the file to be downloaded to. Default is "temp"
                            Do not include the file extension. It will be added automatically.

        Returns:
            str: Media url

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.download_media("media_url", "image/jpeg")
            >>> whatsapp.download_media("media_url", "video/mp4", "path/to/file") #do not include the file extension
        """
        r = requests.get(media_url, headers=self.headers)
        content = r.content
        extension = mime_type.split("/")[1]
        # create a temporary file
        try:

            save_file_here = (
                f"{file_path}.{extension}" if file_path else f"temp.{extension}"
            )
            with open(save_file_here, "wb") as f:
                f.write(content)
            logging.info(f"Media downloaded to {save_file_here}")
            return f.name
        except Exception as e:
            print(e)
            logging.info(f"Error downloading media to {save_file_here}")
            return None

    def preprocess(self, data):
        """
        Preprocesses the data received from the webhook.

        This method is designed to only be used internally.

        Args:
            data[dict]: The data received from the webhook
        """
        return data["entry"][0]["changes"][0]["value"]

    def get_mobile(self, data):
        """
        Extracts the mobile number of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The mobile number of the sender

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> mobile = whatsapp.get_mobile(data)
        """
        data = self.preprocess(data)
        if "contacts" in data:
            return data["contacts"][0]["wa_id"]

    def get_name(self, data):
        """
        Extracts the name of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The name of the sender
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> mobile = whatsapp.get_name(data)
        """
        contact = self.preprocess(data)
        if contact:
            return contact["contacts"][0]["profile"]["name"]

    def get_message(self, data):
        """
        Extracts the text message of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The text message received from the sender
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> message = message.get_message(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["text"]["body"]

    def get_message_id(self, data):
        """
        Extracts the message id of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The message id of the sender
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> message_id = whatsapp.get_message_id(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["id"]

    def get_message_timestamp(self, data):
        """ "
        Extracts the timestamp of the message from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            str: The timestamp of the message
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.get_message_timestamp(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["timestamp"]

    def get_interactive_response(self, data):
        """
         Extracts the response of the interactive message from the data received from the webhook.

         Args:
            data[dict]: The data received from the webhook
        Returns:
            dict: The response of the interactive message

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> response = whatsapp.get_interactive_response(data)
            >>> intractive_type = response.get("type")
            >>> message_id = response[intractive_type]["id"]
            >>> message_text = response[intractive_type]["title"]
        """
        data = self.preprocess(data)
        if "messages" in data:
            if "interactive" in data["messages"][0]:
                return data["messages"][0]["interactive"]

    def get_location(self, data):
        """
        Extracts the location of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook

        Returns:
            dict: The location of the sender

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.get_location(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            if "location" in data["messages"][0]:
                return data["messages"][0]["location"]

    def get_image(self, data):
        """ "
        Extracts the image of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            dict: The image_id of an image sent by the sender

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> image_id = whatsapp.get_image(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            if "image" in data["messages"][0]:
                return data["messages"][0]["image"]

    def get_audio(self, data):
        """
        Extracts the audio of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook

        Returns:
            dict: The audio of the sender

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.get_audio(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            if "audio" in data["messages"][0]:
                return data["messages"][0]["audio"]

    def get_video(self, data):
        """
        Extracts the video of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook

        Returns:
            dict: Dictionary containing the video details sent by the sender

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.get_video(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            if "video" in data["messages"][0]:
                return data["messages"][0]["video"]

    def get_message_type(self, data):
        """
        Gets the type of the message sent by the sender from the data received from the webhook.


        Args:
            data [dict]: The data received from the webhook

        Returns:
            str: The type of the message sent by the sender

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.get_message_type(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            return data["messages"][0]["type"]

    def get_delivery(self, data):
        """
        Extracts the delivery status of the message from the data received from the webhook.
        Args:
            data [dict]: The data received from the webhook

        Returns:
            dict: The delivery status of the message and message id of the message
        """
        data = self.preprocess(data)
        if "statuses" in data:
            return data["statuses"][0]["status"]

    def changed_field(self, data):
        """
        Helper function to check if the field changed in the data received from the webhook.

        Args:
            data [dict]: The data received from the webhook

        Returns:
            str: The field changed in the data received from the webhook

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.changed_field(data)
        """
        return data["entry"][0]["changes"][0]["field"]
