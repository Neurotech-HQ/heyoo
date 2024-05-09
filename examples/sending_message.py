import asyncio
from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv


async def main():
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id=getenv("PHONE_NUMBER_ID"))

    response = await messenger.send_message(
        message="https://www.youtube.com/watch?v=K4TOrB7at0Y",
        recipient_id="255757xxxxxx",
    )

    print(response)

if __name__ == "__main__":
    asyncio.run(main())
