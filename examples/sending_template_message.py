import asyncio
from os import getenv
from heyoo import WhatsApp
from dotenv import load_dotenv


async def main():
    load_dotenv()

    messenger = WhatsApp(token=getenv("TOKEN"), phone_number_id=getenv("PHONE_NUMBER_ID"))
    response = await messenger.send_template("hello_world", "255757xxxxxx", components=[], lang="en_US")

    print(response)


if __name__ == "__main__":
    asyncio.run(main())
