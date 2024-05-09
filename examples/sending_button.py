import asyncio
from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv


async def main():
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id=getenv("PHONE_NUMBER_ID"))

    response = await messenger.send_button(
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

    print(response)


if __name__ == "__main__":
    asyncio.run(main())
