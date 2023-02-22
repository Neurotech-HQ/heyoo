<samp>

# [heyoo](https://pypi.org/project/heyoo/)

[![Made in Tanzania](https://img.shields.io/badge/made%20in-tanzania-008751.svg?style=flat-square)](https://github.com/Tanzania-Developers-Community/made-in-tanzania)
[![Downloads](https://pepy.tech/badge/heyoo)](https://pepy.tech/project/heyoo)
[![Downloads](https://pepy.tech/badge/heyoo/month)](https://pepy.tech/project/heyoo)
[![Downloads](https://pepy.tech/badge/heyoo/week)](https://pepy.tech/project/heyoo)

Unofficial python wrapper to [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)

## Features supported

1. Sending messages
2. Marking messages as read
3. Sending  Media (images, audio, video and documents)
4. Sending location
5. Sending interactive buttons
6. Sending template messages
7. Parsing messages and media received

## Getting started

To get started with **heyoo**, you have to firstly install the libary either directly or using *pip*.

### Installation directly

Use git to clone or you can also manually download the project repository just as shown below;

```bash
$ git clone https://github.com/Neurotech-HQ/heyoo
$ cd heyoo
heyoo $ python setup.py install 
```

### Installing from pip

```bash
# For Windows 

pip install  --upgrade heyoo

#For Linux | MAC 

pip3 install --upgrade heyoo
```

### Running on Docker
To run an instance in docker run the commands below
```bash
$ docker compose build
$ docker compose up
```

## Setting up

To get started using this package, you will need **TOKEN** and **TEST WHATSAPP NUMBER** which you can get by from [Facebook Developer Portal](https://developers.facebook.com/)

Here are steps to follow for you to get started

1. [Go to your apps](https://developers.facebook.com/apps)
2. [create an app](https://developers.facebook.com/apps/create/)
3. Select Business >> Business
4. It will prompt you to enter basic app informations
5. It will ask you to add products to your app
    a. Add WhatsApp Messenger
6. Right there you will see a your **TOKEN** and **TEST WHATSAPP NUMBER** and its phone_number_id
7. Lastly verify the number you will be using for testing on the **To** field.

Once you're follow the above procedures, now you're ready to start hacking with the Wrapper.

## Authentication

Here how you authenticate your application, you need to specify two things the ```TOKEN``` and ```phone_number_id``` of your test number

```python
>>> from heyoo import WhatsApp
>>> messenger = WhatsApp('TOKEN',  phone_number_id='104xxxxxx')
```

Once you have authenticated your app, now you can start using the above mentioned feature as shown above;

> Apparently it is only possible to send messages other than templates after the target phone responds to an initial message. Reference: <https://developers.facebook.com/community/threads/425605939396247/>

## Logging

You can configure your own log level. This is an example to set the log level to info. By default only Error messages are logged.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
```

## Sending Messanges

Use this method to send text message to a WhatsApp number.

```python
>>> messenger.send_message('Your message ', 'Mobile eg: 255757xxxxx')
```

## Marking messages as read

Use this method to mark a previously sent text message as read.

```python
>>> messenger.mark_as_read('Message ID')
```
    
## Sending Images

When sending media(image, video, audio, gif and document ), you can either specify a link containing  the media or specify object id, you can do this using the same method.

By default all media methods assume you're sending link containing media but you can change this by specifying the ```link=False```.

Here an example;

```python
>>> messenger.send_image(
        image="https://i.imgur.com/Fh7XVYY.jpeg",
        recipient_id="255757xxxxxx",
    )
```

> Note: You can also send media from your local machine but you have to upload it first to Whatsapp Cloud API, you can do this using the ```upload_media``` method. and then use the returned object id to send the media.

Here an example;

```python
>>> media_id = messenger.upload_media(
        media='path/to/media',
    )['id']
>>> messenger.send_image(
        image=media_id,
        recipient_id="255757xxxxxx",
        link=False
    )
```

> Note: Don't forget to set the link to False, and also you can use the same technique for sending video, audio, gif and document from your local machine.

## Sending Video

Here an example;

```python

>>> messenger.send_video(
        video="https://www.youtube.com/watch?v=K4TOrB7at0Y",
        recipient_id="255757xxxxxx",
    )
```

## Sending Audio

Here an example;

```python
>>> messenger.send_audio(
        audio="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
        recipient_id="255757xxxxxx",
    )
```

## Sending Document

Here an example;

```python
>>> messenger.send_document(
        document="http://www.africau.edu/images/default/sample.pdf",
        recipient_id="255757xxxxxx",
    )
```

## Sending Location

Here an example;

```python
>>> messenger.send_location(
        lat=1.29,
        long=103.85,
        name="Singapore",
        address="Singapore",
        recipient_id="255757xxxxxx",
    )
```

## Sending Interactive buttons

Here an example;

> Note: row button title may not exceed 20 characters otherwise your message will not be sent to the target phone.

```python
>>> messenger.send_button(
        recipient_id="255757xxxxxx",
        button={
            "header": "Header Testing",
            "body": "Body Testing",
            "footer": "Footer Testing",
            "action": {
                "button": "Button Testing",
                "sections": [
                    {
                        "title": "iBank",
                        "rows": [
                            {"id": "row 1", "title": "Send Money", "description": ""},
                            {
                                "id": "row 2",
                                "title": "Withdraw money",
                                "description": "",
                            },
                        ],
                    }
                ],
            },
        },
    )
```

## Sending Interactive reply buttons

Here an example;

> Send reply button only displays three reply buttons, if it exceeds three reply buttons, it will raise an error and your message will not be sent.

```python
>>> messenger.send_reply_button(
        recipient_id="255757xxxxxx",
        button={
            "type": "button",
            "body": {
                "text": "This is a test button"
            },
            "action": {
                "buttons": [
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b1",
                            "title": "This is button 1"
                        }
                    },
                    {
                        "type": "reply",
                        "reply": {
                            "id": "b2",
                            "title": "this is button 2"
                        }
                    }
                ]
            }
      },
    )
```

## Sending a Template Messages

Here how to send a pre-approved template message, Template messages can either be;

1. Text template
2. Media based template
3. Interactive template

You can customize the template message by passing a dictionary of components.

    
IMPORTANT: components are also known as variable parameters (like `{{0}}` or `{{1}}`) which are used to include variables into a message.
You can find the available components in the documentation.
<https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates>

```python
>>> messenger.send_template("hello_world", "255757xxxxxx", components=[])
```

## Webhook

Webhook are useful incase you're wondering how to respond to incoming message send by user, but I have created a [starter webhook](https://github.com/Neurotech-HQ/heyoo/blob/main/hook.py) which you can then customize it according to your own plans.

Here an example on how you can use webhook to respond to incoming messages;

```python
  # Handle Webhook Subscriptions
    data = request.get_json()
    logging.info("Received webhook data: %s", data)
    changed_field = messenger.changed_field(data)
    if changed_field == "messages":
        new_message = messenger.get_mobile(data)
        if new_message:
            mobile = messenger.get_mobile(data)
            name = messenger.get_name(data)
            message_type = messenger.get_message_type(data)
            logging.info(
                f"New Message; sender:{mobile} name:{name} type:{message_type}"
            )
            if message_type == "text":
                message = messenger.get_message(data)
                name = messenger.get_name(data)
                logging.info("Message: %s", message)
                messenger.send_message(f"Hi {name}, nice to connect with you", mobile)

            elif message_type == "interactive":
                message_response = messenger.get_interactive_response(data)
                intractive_type = message_response.get("type")
                message_id = message_response[intractive_type]["id"]
                message_text = message_response[intractive_type]["title"]
                logging.info(f"Interactive Message; {message_id}: {message_text}")

            elif message_type == "location":
                message_location = messenger.get_location(data)
                message_latitude = message_location["latitude"]
                message_longitude = message_location["longitude"]
                logging.info("Location: %s, %s", message_latitude, message_longitude)

            elif message_type == "image":
                image = messenger.get_image(data)
                image_id, mime_type = image["id"], image["mime_type"]
                image_url = messenger.query_media_url(image_id)
                image_filename = messenger.download_media(image_url, mime_type)
                print(f"{mobile} sent image {image_filename}")
                logging.info(f"{mobile} sent image {image_filename}")

            elif message_type == "video":
                video = messenger.get_video(data)
                video_id, mime_type = video["id"], video["mime_type"]
                video_url = messenger.query_media_url(video_id)
                video_filename = messenger.download_media(video_url, mime_type)
                print(f"{mobile} sent video {video_filename}")
                logging.info(f"{mobile} sent video {video_filename}")

            elif message_type == "audio":
                audio = messenger.get_audio(data)
                audio_id, mime_type = audio["id"], audio["mime_type"]
                audio_url = messenger.query_media_url(audio_id)
                audio_filename = messenger.download_media(audio_url, mime_type)
                print(f"{mobile} sent audio {audio_filename}")
                logging.info(f"{mobile} sent audio {audio_filename}")

            elif message_type == "document":
                file = messenger.get_document(data)
                file_id, mime_type = file["id"], file["mime_type"]
                file_url = messenger.query_media_url(file_id)
                file_filename = messenger.download_media(file_url, mime_type)
                print(f"{mobile} sent file {file_filename}")
                logging.info(f"{mobile} sent file {file_filename}")
            else:
                print(f"{mobile} sent {message_type} ")
                print(data)
        else:
            delivery = messenger.get_delivery(data)
            if delivery:
                print(f"Message : {delivery}")
            else:
                print("No new message")
    return "ok"
```

Incase you want a hustle free automatic deployment of the webhook to the Heroku platform, then we have made it simpler for you. With Just a click of a button you can deploy your webhook to Heroku.

## steps to Deploy webhook to Heroku

1. Click the deploy button and the Heroku webpage will open for authentication, after authentication sit back and relax for deployment to finish.
                             [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/JAXPARROW/whatsapi-flask-webhook)

2. From Heroku settings configure your Environment varibles of your WhatsAapp application.
3. Setup and verify your webhook url and token then subscribe to messages.

To learn more about webhook and how to configure in your Facebook developer dashboard please [have a look here](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/set-up-webhooks).


## Issues

If you will face any issue with the usage of this package please raise one so as we can quickly fix it as soon as possible;

## Contributing

This is an opensource project under ```MIT License``` so any one is welcome to contribute from typo, to source code to documentation, ```JUST FORK IT```.

## References

1. [WhatsApp Cloud API official documentation](https://developers.facebook.com/docs/whatsapp/cloud-api/)
2. [Programming WhatsApp is now even easier for Python Developers](https://mr-collins-llb.medium.com/programming-whatsapp-is-now-even-easier-for-python-developers-e1a4343deed6)
3. [Meet Heyoo — an Open-source Python Wrapper for WhatsApp Cloud API](https://betterprogramming.pub/programming-whatsapp-is-now-even-easier-for-python-developers-e1a4343deed6)
4. [Whatsapp Cloud API: How to send WhatsApp messages from Python?](https://medium.com/@today.rafi/whatsapp-cloud-api-how-to-send-whatsapp-messages-from-python-9baa03c93b5d)

## Related

1. [WhatsApp Cloud API PHP Wrapper](https://github.com/pro-cms/whatsappcloud-php)
2. [Heyoo Javascript](https://github.com/JS-Hub-ZW/heyooh)

## All the credit

1. [kalebu](https://github.com/Kalebu)
2. All other contributors
</samp>
