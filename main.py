import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputAudioStream
from pytgcalls.types.input_stream.quality import HighQualityAudio
from pytgcalls.types import Update
from pytgcalls.types.stream import StreamAudioEnded
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID

app = Client(
    "vc-assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

pytg = PyTgCalls(app)


def owner_only(_, __, message):
    return message.from_user and message.from_user.id == OWNER_ID


owner_filter = filters.create(owner_only)


#VOLUME INCREASE FUNCTION

@app.on_message(filters.command("level") & owner_filter)
async def set_volume(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /level 1-20")
        return

    try:
        level = int(message.command[1])

        if level < 1 or level > 20:
            await message.reply("Level must be between 1 and 20.")
            return

        volume = level * 5  # converts 1-20 → 5-100

        await pytg.change_volume_call(
            message.chat.id,
            volume
        )

        await message.reply(f"Volume set to Level {level}")

    except Exception as e:
        await message.reply(f"Error: {e}")

@app.on_message(filters.command("join") & owner_filter)
async def join_vc(client, message):
    if len(message.command) < 2:
        await message.reply("Usage: /join <chat_id>")
        return

    chat_id = int(message.command[1])

    try:
        await pytg.join_group_call(
            chat_id,
            InputAudioStream(
                "sample_audio.mp3",
                HighQualityAudio()
            )
        )
        await message.reply("Joined VC successfully.")
    except Exception as e:
        await message.reply(f"Error: {e}")


@app.on_message(filters.command("mute") & owner_filter)
async def mute_vc(client, message):
    chat_id = message.chat.id
    try:
        await pytg.mute_stream(chat_id)
        await message.reply("VC muted.")
    except Exception as e:
        await message.reply(f"Error: {e}")


@app.on_message(filters.command("unmute") & owner_filter)
async def unmute_vc(client, message):
    chat_id = message.chat.id
    try:
        await pytg.unmute_stream(chat_id)
        await message.reply("VC unmuted.")
    except Exception as e:
        await message.reply(f"Error: {e}")


@app.on_message(filters.command("leaveplay") & owner_filter)
async def leave_play(client, message):
    chat_id = message.chat.id
    try:
        await pytg.leave_group_call(chat_id)
        await message.reply("Left voice chat.")
    except Exception as e:
        await message.reply(f"Error: {e}")


@app.on_message(filters.command("leaverecord") & owner_filter)
async def leave_record(client, message):
    chat_id = message.chat.id
    try:
        await pytg.leave_group_call(chat_id)
        await message.reply("Left control VC.")
    except Exception as e:
        await message.reply(f"Error: {e}")


@app.on_message(filters.command("shutdown") & owner_filter)
async def shutdown_bot(client, message):
    await message.reply("Shutting down...")
    await pytg.stop()
    await app.stop()


@pytg.on_update()
async def stream_end_handler(_, update: Update):
    if isinstance(update, StreamAudioEnded):
        await pytg.leave_group_call(update.chat_id)


async def main():
    await app.start()
    await pytg.start()
    print("VC Assistant Bot Started")
    await idle()


from pyrogram.idle import idle

asyncio.get_event_loop().run_until_complete(main())
