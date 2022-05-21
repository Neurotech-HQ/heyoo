<samp>

# [heyoo](https://pypi.org/project/heyoo/)

[![Made in Tanzania](https://img.shields.io/badge/made%20in-tanzania-008751.svg?style=flat-square)](https://github.com/Tanzania-Developers-Community/made-in-tanzania)
[![Downloads](https://pepy.tech/badge/heyoo)](https://pepy.tech/project/heyoo)
[![Downloads](https://pepy.tech/badge/heyoo/month)](https://pepy.tech/project/heyoo)
[![Downloads](https://pepy.tech/badge/heyoo/week)](https://pepy.tech/project/heyoo)

Unofficial python wrapper to [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)

## Features supported

1. Sending messages
2. Sending  Media (images, audio, video and ducuments)
3. Sending location
4. Sending interactive buttons
5. Sending template messages

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

## Setting up

To get started using this package, you will need **TOKEN** and **TEST WHATSAPP NUMBER** which you can get by from [Facebook Developer Portal](https://developers.facebook.com/)

Here are steps to follow for you to get started

1. [Go to your apps](https://developers.facebook.com/apps)
2. [create an app](https://developers.facebook.com/apps/create/)
3. Select Bussiness >> Bussiness
4. It will prompt you to enter basic app informations
5. It will ask you to add products to your app
    a. Add WhatsApp Messenger
6. Right there you will see a your **TOKEN** and **TEST WHATSAPP NUMBER** and its phone_number_id
7. Lastly verify the number you will be using for testing on the **To** field.

Once you're follow the above procedures, now you're ready to start hacking with the Wrapper.

## Authentication

Here how you authenticate your application, you need to specofy two things the ```TOKEN``` and ```phone_number_id``` of your test number

```python
>>> from heyoo import WhatsApp
>>> messenger = WhatsApp('TOKEN',  phone_number_id='104xxxxxx')
```

Once you have authenticated your app, now you can start using the above mentioned feature as shown above;

## Sending Messanges

Here how to send messages;

```python
>>> messenger.send_message('Your message ', 'Mobile eg: 255757xxxxx')
```

### Example

Here an example

```python
>>> messenger.send_message('Hi there just testiing', '255757902132')
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

## Sending a Template Messages

Here how to send a pre-approved template message;

```python
>>> messenger.send_template("hello_world", "255757xxxxxx")
```

## Webhook

Webhook are useful incase you're wondering how to respond to incoming message send by user, but I have created a [starter webhook](https://github.com/Neurotech-HQ/heyoo/blob/main/hook.py) which you can then customize it according to your own plans.

To learn more about webhook and how to configure in your Facebook developer dashboard please [have a look here](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/set-up-webhooks).

## Issues

If you will face any issue with the usage of this package please raise one so as we can quickly fix it as soon as possible;

## Contributing

This is an opensource project under ```MIT License``` so any one is welcome to contribute from typo, to source code to documentation, ```JUST FORK IT```.

## All the credit

1. [kalebu](https://github.com/Kalebu)
2. All other contributors

</samp>
