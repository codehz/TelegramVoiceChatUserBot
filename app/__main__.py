import re
import ffmpeg
from config import Config
from pyrogram import Client, idle, filters
from pytgcalls import GroupCallFactory
from youtube_dl import YoutubeDL


client = Client(
    Config.SESSION_STRING,
    Config.API_ID,
    Config.API_HASH,
)
ytdl = YoutubeDL({
    "quiet": True,
    "geo_bypass": True,
    "nocheckcertificate": True,
})
print("login successfully")

group_call = None
base_filter = filters.outgoing & ~filters.forwarded & ~filters.edited
yt_regex = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"


def init_group_call(func):
    async def wrapper(client, message):
        global group_call
        if not group_call:
            group_call = GroupCallFactory(client).get_group_call()
        await message.delete()
        return await func(client, message)
    return wrapper


async def send_log(content):
    await client.send_message(Config.CHAT_ID, content, disable_notification=True, disable_web_page_preview=True)


@client.on_message(filters.command("stream", "") & base_filter)
@init_group_call
async def stop_stream(_, m):
    if group_call:
        group_call.leave()

@client.on_message(filters.command("stream", "") & base_filter)
@init_group_call
async def start_stream(_, m):
    if ' ' not in m.text:
        return
    query = m.text.split(' ', 1)[1]
    print(query)
    link = query
    match = re.match(yt_regex, query)
    if match:
        await send_log("Got YouTube link: " + query)
        try:
            meta = ytdl.extract_info(query, download=False)
            formats = meta.get('formats', [meta])
            for f in formats:
                link = f['url']
                if f['format_note'] == '1080p':
                    break
        except Exception as e:
            await send_log(f"**YouTube Download Error!** \n\nError: `{e}`")
            print(e)
            return
    await send_log(f"Got video link: {link}")
    try:
        if not group_call.is_connected:
            await group_call.join(m.chat.id)
        await group_call.start_video(link, with_audio=True)
        await send_log(f"starting {link}")
    except Exception as e:
        await send_log(f"**An Error Occoured!** \n\nError: `{e}`")
        print(e)
        return


client.start()
idle()
client.stop()
