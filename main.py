from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types import GroupCallParticipant
from config import API_ID, API_HASH, STRING_SESSION
import asyncio


app = Client(STRING_SESSION, api_id=API_ID, api_hash=API_HASH)
calls = PyTgCalls(app)

current_level = 10  # default 10/20

def level_to_volume(lvl: int) -> int:
    return max(1, min(20, lvl)) * 10  # 1-20 → 10-200

# ---------------- Commands -----------------

@app.on_message(filters.command("level", prefixes=".") & filters.me)
async def set_level_cmd(_, msg: Message):
    global current_level
    if len(msg.command) < 2:
        await msg.edit(f"Current level: {current_level}/20")
        return
    try:
        new_level = int(msg.command[1])
        if not 1 <= new_level <= 20:
            raise ValueError
    except ValueError:
        await msg.edit("Usage: `.level 1-20`")
        return

    current_level = new_level
    vol = level_to_volume(current_level)
    try:
        await calls.set_my_volume(vol)
        await msg.edit(f"Mic level set: {current_level}/20 → {vol}/200")
    except Exception as e:
        await msg.edit(f"Failed to set volume: {e}")

@app.on_message(filters.command("joinvc", prefixes=".") & filters.me)
async def join_vc(_, msg: Message):
    chat_id = msg.chat.id
    try:
        await calls.join_group_call(chat_id, stream_type="raw")
        await asyncio.sleep(2)
        await calls.set_my_volume(level_to_volume(current_level))
        await msg.edit(f"Joined VC | Mic Level: {current_level}/20")
    except Exception as e:
        await msg.edit(f"Error joining VC: {e}")

@app.on_message(filters.command("leavevc", prefixes=".") & filters.me)
async def leave_vc(_, msg: Message):
    try:
        await calls.leave_group_call(msg.chat.id)
        await msg.edit("Left VC")
    except Exception as e:
        await msg.edit(f"Error leaving VC: {e}")

# ---------------- Auto re-apply volume -----------------
@calls.on_participant_updated()
async def participant_update(_, participant: GroupCallParticipant):
    if participant.user_id == (await app.get_me()).id:
        try:
            await calls.set_my_volume(level_to_volume(current_level))
        except:
            pass

# ---------------- Run -----------------
async def main():
    await app.start()
    await calls.start()
    print("Userbot running! Use .joinvc and .level to boost mic")
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
