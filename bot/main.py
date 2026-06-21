import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from highrise.__main__ import main, BotDefinition
from bot import HighriseBot
from config import HIGHRISE_TOKEN, HIGHRISE_ROOM_ID


def start():
    if not HIGHRISE_TOKEN:
        print("[ERROR] HIGHRISE_TOKEN is not set!")
        sys.exit(1)
    if not HIGHRISE_ROOM_ID:
        print("[ERROR] HIGHRISE_ROOM_ID is not set!")
        sys.exit(1)

    print(f"[BOT] Connecting to room: {HIGHRISE_ROOM_ID}")
    print(f"[BOT] Token: {HIGHRISE_TOKEN[:8]}...")

    definitions = [
        BotDefinition(
            bot=HighriseBot(),
            room_id=HIGHRISE_ROOM_ID,
            api_token=HIGHRISE_TOKEN,
        )
    ]
    asyncio.run(main(definitions))


if __name__ == "__main__":
    start()
