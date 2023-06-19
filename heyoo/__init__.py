"""
Unofficial python wrapper for the WhatsApp Cloud API.
"""
from __future__ import annotations
import os
import mimetypes
import requests
import logging
import warnings
from colorama import Fore, Style
from requests_toolbelt.multipart.encoder import MultipartEncoder
from typing import Optional, Dict, Any, List, Union, Tuple, Callable


# Setup logging
logging.getLogger(__name__).addHandler(logging.NullHandler())

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
        self.v15_base_url = "https://graph.facebook.com/v15.0"
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
        logging.error(f"Response: {r.json()}")
        return r.json()

    def send_reaction(
        self, emoji, message_id, recipient_id, recipient_type="individual"
    ):
        """
         Sends a reaction message to a WhatsApp user's message

         Args:
                emoji[str]: Emoji to become a reaction to a message. Ex.: '\uD83D\uDE00' (😀)
                message_id[str]: Message id for a reaction to be attached to
                recipient_id[str]: Phone number of the user with country code without +
                recipient_type[str]: Type of the recipient, either individual or group

        Example:
            ```python
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_reaction("\uD83D\uDE00", "wamid.HBgLM...", "5511999999999")

        """
        data = {
            "messaging_product": "whatsapp",
            "recipient_type": recipient_type,
            "to": recipient_id,
            "type": "reaction",
            "reaction": {"message_id": message_id, "emoji": emoji},
        }
        logging.info(f"Sending reaction to number {recipient_id} message id {message_id}")
        r = requests.post(f"{self.url}", headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Reaction sent to number {recipient_id} message id {message_id}")
            return r.json()
        logging.info(f"Message not sent  to number {recipient_id} message id {message_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(f"Response: {r.json()}")
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
        logging.error(f"Response: {r.json()}")
        return r.json()

    def send_template(self, template, recipient_id, components, lang: str = "en_US"):
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
            components[list]: List of components to be sent to the user  # CHANGE
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
        logging.error(f"Response: {r.json()}")
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

    def send_sticker(self, sticker: str, recipient_id: str, recipient_type="individual", link=True):
        """
        Sends a sticker message to a WhatsApp user

        There are two ways to send a sticker message to a user, either by passing the image id or by passing the sticker link.
        Sticker id is the id of the sticker uploaded to the cloud api.

        Args:
            sticker[str]: Sticker id or link of the sticker
            recipient_id[str]: Phone number of the user with country code wihout +
            recipient_type[str]: Type of the recipient, either individual or group
            link[bool]: Whether to send an sticker id or an sticker link, True means that the sticker is an id, False means that the image is a link


        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_sticker("170511049062862", "5511999999999", link=False)
        """
        if link:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "sticker",
                "sticker": {"link": sticker},
            }
        else:
            data = {
                "messaging_product": "whatsapp",
                "recipient_type": recipient_type,
                "to": recipient_id,
                "type": "sticker",
                "sticker": {"id": sticker},
            }
        logging.info(f"Sending sticker to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Sticker sent to {recipient_id}")
            return r.json()
        logging.info(f"Sticker not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(r.json())
        return r.json()

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

    def send_video(
        self, video, recipient_id, caption=None, link=True
    ) -> Dict[Any, Any]:
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

    def send_custom_json(self, data, recipient_id=None):
        """
        Sends a custom json to a WhatsApp user. This can be used to send custom objects to the message endpoint.

        Args:
            data[dict]: Dictionary that should be send
            recipient_id[str]: Phone number of the user with country code wihout +
        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.send_custom_json({
                    "messaging_product": "whatsapp",
                    "type": "audio",
                    "audio": {"id": audio}}, "5511999999999")
        """

        if recipient_id:
            if "to" in data.keys():
                data_recipient_id = data["to"]
                logging.info(f"Recipient Id is defined in data ({data_recipient_id}) and recipient_id parameter ({recipient_id})")
            else:
                data["to"] = recipient_id

        logging.info(f"Sending custom json to {recipient_id}")
        r = requests.post(self.url, headers=self.headers, json=data)
        if r.status_code == 200:
            logging.info(f"Custom json sent to {recipient_id}")
            return r.json()
        logging.info(f"Custom json not sent to {recipient_id}")
        logging.info(f"Status code: {r.status_code}")
        logging.error(f"Response: {r.json()}")
        return r.json()

    def send_document(
        self, document, recipient_id, caption=None, link=True
    ) -> Dict[Any, Any]:
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

    def send_contacts(
        self, contacts: List[Dict[Any, Any]], recipient_id: str
    ) -> Dict[Any, Any]:
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

    def upload_media(self, media: str) -> Union[Dict[Any, Any], None]:
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
            headers=headers,
            data=form_data,
        )
        if r.status_code == 200:
            logging.info(f"Media {media} uploaded")
            return r.json()
        logging.info(f"Error uploading media {media}")
        logging.info(f"Status code: {r.status_code}")
        logging.info(f"Response: {r.json()}")
        return None

    def delete_media(self, media_id: str) -> Union[Dict[Any, Any], None]:
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

    def mark_as_read(self, message_id: str) -> Dict[Any, Any]:
        """
        Marks a message as read

        Args:
            message_id[str]: Id of the message to be marked as read

        Returns:
            Dict[Any, Any]: Response from the API

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> whatsapp.mark_as_read("message_id")
        """
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json",
        }

        json_data = {
            "messaging_product": "whatsapp",
            "status": "read",
            "message_id": message_id,
        }
        logging.info(f"Marking message {message_id} as read")
        response = requests.post(
            f"{self.v15_base_url}/{self.phone_number_id}/messages",
            headers=headers,
            json=json_data,
        )
        if response.status_code == 200:
            logging.info(f"Message {message_id} marked as read")
            return response.json()
        logging.info(f"Error marking message {message_id} as read")
        logging.info(f"Status code: {response.status_code}")
        logging.info(f"Response: {response.json()}")
        return response

    def create_button(self, button: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Method to create a button object to be used in the send_message method.

        This is method is designed to only be used internally by the send_button method.

        Args:
               button[dict]: A dictionary containing the button data
        """
        data = {"type": "list", "action": button.get("action")}
        if button.get("header"):
            data["header"] = {"type": "text", "text": button.get("header")}
        if button.get("body"):
            data["body"] = {"text": button.get("body")}
        if button.get("footer"):
            data["footer"] = {"text": button.get("footer")}
        return data

    def send_button(self, button: Dict[Any, Any], recipient_id: str) -> Dict[Any, Any]:
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

    def send_reply_button(
        self, button: Dict[Any, Any], recipient_id: str
    ) -> Dict[Any, Any]:
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

    def query_media_url(self, media_id: str) -> Union[str, None]:
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

    def download_media(
        self, media_url: str, mime_type: str, file_path: str = "temp"
    ) -> Union[str, None]:
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
            logging.info(e)
            logging.ERROR(f"Error downloading media to {save_file_here}")
            return None

    def preprocess(self, data: Dict[Any, Any]) -> Dict[Any, Any]:
        """
        Preprocesses the data received from the webhook.

        This method is designed to only be used internally.

        Args:
            data[dict]: The data received from the webhook
        """
        return data["entry"][0]["changes"][0]["value"]

    def is_message(self, data: Dict[Any, Any]) -> bool:
        """is_message checks if the data received from the webhook is a message.

        Args:
            data (Dict[Any, Any]): The data received from the webhook

        Returns:
            bool: True if the data is a message, False otherwise
        """
        data = self.preprocess(data)
        if "messages" in data:
            return True
        else:
            return False

    def get_mobile(self, data: Dict[Any, Any]) -> Union[str, None]:
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

    def get_name(self, data: Dict[Any, Any]) -> Union[str, None]:
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

    def get_message(self, data: Dict[Any, Any]) -> Union[str, None]:
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

    def get_message_id(self, data: Dict[Any, Any]) -> Union[str, None]:
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

    def get_message_timestamp(self, data: Dict[Any, Any]) -> Union[str, None]:
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

    def get_interactive_response(self, data: Dict[Any, Any]) -> Union[Dict, None]:
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
            >>> interactive_type = response.get("type")
            >>> message_id = response[interactive_type]["id"]
            >>> message_text = response[interactive_type]["title"]
        """
        data = self.preprocess(data)
        if "messages" in data:
            if "interactive" in data["messages"][0]:
                return data["messages"][0]["interactive"]

    def get_location(self, data: Dict[Any, Any]) -> Union[Dict, None]:
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

    def get_image(self, data: Dict[Any, Any]) -> Union[Dict, None]:
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

    def get_document(self, data: Dict[Any, Any]) -> Union[Dict, None]:
        """ "
        Extracts the document of the sender from the data received from the webhook.

        Args:
            data[dict]: The data received from the webhook
        Returns:
            dict: The document_id of an image sent by the sender

        Example:
            >>> from whatsapp import WhatsApp
            >>> whatsapp = WhatsApp(token, phone_number_id)
            >>> document_id = whatsapp.get_document(data)
        """
        data = self.preprocess(data)
        if "messages" in data:
            if "document" in data["messages"][0]:
                return data["messages"][0]["document"]

    def get_audio(self, data: Dict[Any, Any]) -> Union[Dict, None]:
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

    def get_video(self, data: Dict[Any, Any]) -> Union[Dict, None]:
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

    def get_message_type(self, data: Dict[Any, Any]) -> Union[str, None]:
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

    def get_delivery(self, data: Dict[Any, Any]) -> Union[Dict, None]:
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

    def changed_field(self, data: Dict[Any, Any]) -> str:
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
