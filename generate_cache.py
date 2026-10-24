import os
import json
import asyncio
from pyrogram import Client, raw

API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]
SESSION_STRING = os.environ["STRING_SESSIONS"]

async def main():
    app = Client(
        "cache_generator",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING,
        in_memory=True,
    )

    await app.start()

    channels = {}
    users = {}

    try:
        dialogs = await app.invoke(
            raw.functions.messages.GetDialogs(
                offset_date=0,
                offset_id=0,
                offset_peer=raw.types.InputPeerEmpty(),
                limit=100,
                hash=0,
            )
        )

        for chat in getattr(dialogs, "chats", []):
            if isinstance(chat, raw.types.Channel):
                channels[str(chat.id)] = chat.access_hash
            elif isinstance(chat, raw.types.User):
                users[str(chat.id)] = chat.access_hash

        os.makedirs("data", exist_ok=True)

        with open("data/peer_cache.json", "w") as f:
            json.dump({
                "InputChannels": channels,
                "InputUsers": users,
            }, f, indent=2)

        print(f"Saved {len(channels)} channels and {len(users)} users.")

    finally:
        await app.stop()

asyncio.run(main())
