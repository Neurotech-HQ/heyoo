import asyncio
from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv


async def main():
    load_dotenv()
    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id=getenv("PHONE_NUMBER_ID"))

    response = await messenger.send_location(
        lat=1.29,
        long=103.85,
        name="Singapore",
        address="Singapore",
        recipient_id="255757294146",
    )

    print(response)


if __name__ == "__main__":
    asyncio.run(main())
