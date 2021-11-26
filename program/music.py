# Copyright (C) 2021 By Veez Music-Project
# Commit Start Date 20/10/2021
# Finished On 28/10/2021

import re
import asyncio

from config import ASSISTANT_NAME, BOT_USERNAME, IMG_1, IMG_2
from driver.filters import command, other_filters
from driver.queues import QUEUE, add_to_queue
from driver.veez import call_py, user
from pyrogram import Client
from pyrogram.errors import UserAlreadyParticipant, UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped
from youtubesearchpython import VideosSearch


def ytsearch(query):
    try:
        search = VideosSearch(query, limit=1)
        for r in search.result()["result"]:
            ytid = r["id"]
            if len(r["title"]) > 34:
                songname = r["title"][:70]
            else:
                songname = r["title"]
            url = f"https://www.youtube.com/watch?v={ytid}"
        return [songname, url]
    except Exception as e:
        print(e)
        return 0


async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "bestaudio",
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


@Client.on_message(command(["play", f"play@{BOT_USERNAME}","تشغيل","شغل","شغلي","/play"]) & other_filters)
async def play(c: Client, m: Message):
    replied = m.reply_to_message
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=" ♬ تـــحـــكـــم ♬", callback_data="cbmenu"),
                InlineKeyboardButton(text="_♬ خــروج ♬_", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("ʏᴏᴜ'ʀᴇ ᴀɴ ᴀɴᴏɴʏᴍᴏᴜs ᴀᴅᴍɪɴ__ \n\n» ʀᴇᴠᴇʀᴛ ʙᴀᴄᴋ ᴛᴏ ᴜsᴇʀ ᴀᴄᴄᴏᴜɴᴛ ғʀᴏᴍ ᴀᴅᴍɪɴ ʀɪɢʜᴛs")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"اسـف حـدث خـطـا ♬.. :\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 لـي اسـتـخـدامي ♬.. ، يـجـب انن اكـون مـشـرف بـي الـصـلاحـيـات الـتـالـيه ↓ : \ n \ n »❌  حذف الرسائل  \ n» ❌  تقييد المستخدمين  \ n »❌ إضافة مستخدمين  \ n» ❌ إدارة محادثة الفيديو \ n \ n يتم تحديث البيانات  تلقائيًا بعد  ترقيتي**"
        )
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **.. ♬ فـي حـد طـرد الـحسـاب الـمـسـاعـد** {m.chat.title}\n\n» **.. ♬ شـيـلـو مـن الـمـحـظـوريـن او كـلـمـنـي هـنـا.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **فـشـل الـبـوت فـي دخـول الـمـجـمـوعـه**\n\n**reason**: `{e}`")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **فـشـل الـبـوت فـي دخـول الـمـجـمـوعـه**\n\n**reason**: `{e}`"
                )

    if replied:
        if replied.audio or replied.voice:
            suhu = await replied.reply("📥 **جـاريـي تـنـزيـل الـمــلـف الـصـوتـي ♬.. **")
            dl = await replied.download()
            link = replied.link
            if replied.audio:
                if replied.audio.title:
                    songname = replied.audio.title[:70]
                else:
                    if replied.audio.file_name:
                        songname = replied.audio.file_name[:70]
                    else:
                        songname = "Audio"
            elif replied.voice:
                songname = "Voice Note"
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname}]({link})\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {m.from_user.mention()}",
                    reply_markup=keyboard,
                )
            else:
             try:
                await suhu.edit("🔄 **لـحـظـه اطـلـع الـكـول ♬.. **")
                await call_py.join_group_call(
                    chat_id,
                    AudioPiped(
                        dl,
                    ),
                    stream_type=StreamType().local_stream,
                )
                add_to_queue(chat_id, songname, dl, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_2}",
                    caption=f"💡 **ᴍᴜsɪᴄ sᴛʀᴇᴀᴍɪɴɢ sᴛᴀʀᴛᴇᴅ**\n\n🏷 **ɴᴀᴍᴇ:** [{songname}]({link})\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n💡 **sᴛᴀᴛᴜs:** `Playing`\n🎧 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                    reply_markup=keyboard,
                )
             except Exception as e:
                await suhu.delete()
                await m.reply_text(f"🚫 اسـف حـدث خـطـا ♬.. :\n\n» {e}")
        else:
            if len(m.command) < 2:
                await m.reply(
                    "» **قـــــم بـي الــرد عـلي مـلـف مـوسـيـقي ♬..
او قــــم بـي كـتـابـة اســم الاغـنـيـه للـبـحـث عـنـهـا ♬..****"
                )
            else:
                suhu = await c.send_message(chat_id, "🔎 **جـــاريي الـبـحـث ♬.. **")
                query = m.text.split(None, 1)[1]
                search = ytsearch(query)
                if search == 0:
                    await suhu.edit("❌ **ɴᴏ ʀᴇsᴜʟᴛs ғᴏᴜɴᴅ**")
                else:
                    songname = search[0]
                    url = search[1]
                    veez, ytlink = await ytdl(url)
                    if veez == 0:
                        await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                    else:
                        if chat_id in QUEUE:
                            pos = add_to_queue(
                                chat_id, songname, ytlink, url, "Audio", 0
                            )
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_1}",
                                caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname}]({url})\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {requester}",
                                reply_markup=keyboard,
                            )
                        else:
                            try:
                                await suhu.edit("🔄 **لـحـظـه اطـلـع الـكـول ♬.. **")
                                await call_py.join_group_call(
                                    chat_id,
                                    AudioPiped(
                                        ytlink,
                                    ),
                                    stream_type=StreamType().local_stream,
                                )
                                add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                                await suhu.delete()
                                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                                await m.reply_photo(
                                    photo=f"{IMG_2}",
                                    caption=f"💡 **ᴍᴜsɪᴄ sᴛʀᴇᴀᴍɪɴɢ sᴛᴀʀᴛᴇᴅ**\n\n🏷 **ɴᴀᴍᴇ:** [{songname}]({url})\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n💡 **sᴛᴀᴛᴜs:** `Playing`\n🎧 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                                    reply_markup=keyboard,
                                )
                            except Exception as ep:
                                await suhu.delete()
                                await m.reply_text(f"🚫 اسـف حـدث خـطـا ♬.. : `{ep}`")

    else:
        if len(m.command) < 2:
            await m.reply(
                "» **قـــــم بـي الــرد عـلي مـلـف مـوسـيـقي♬..
او قـم بـي كـتـابـة اســم الاغـنـيـه للـبـحـث عـنـهـا ♬..**" 
            )
        else:
            suhu = await c.send_message(chat_id, "🔎 **جـــاريي الـبـحـث ♬.. **")
            query = m.text.split(None, 1)[1]
            search = ytsearch(query)
            if search == 0:
                await suhu.edit("❌ **no results found.**")
            else:
                songname = search[0]
                url = search[1]
                veez, ytlink = await ytdl(url)
                if veez == 0:
                    await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
                else:
                    if chat_id in QUEUE:
                        pos = add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                        await suhu.delete()
                        requester = (
                            f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                        )
                        await m.reply_photo(
                            photo=f"{IMG_1}",
                            caption=f"💡 **Track added to queue »** `{pos}`\n\n🏷 **Name:** [{songname}]({url})\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {requester}",
                            reply_markup=keyboard,
                        )
                    else:
                        try:
                            await suhu.edit("🔄 **لـحـظـه اطـلـع الـكـول ♬.. **")
                            await call_py.join_group_call(
                                chat_id,
                                AudioPiped(
                                    ytlink,
                                ),
                                stream_type=StreamType().local_stream,
                            )
                            add_to_queue(chat_id, songname, ytlink, url, "Audio", 0)
                            await suhu.delete()
                            requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                            await m.reply_photo(
                                photo=f"{IMG_2}",
                                caption=f"💡 **ᴍᴜsɪᴄ sᴛʀᴇᴀᴍɪɴɢ sᴛᴀʀᴛᴇᴅ**\n\n🏷 **ɴᴀᴍᴇ:** [{songname}]({url})\n💭 **ᴄʜᴀᴛ:** `{chat_id}`\n💡 **sᴛᴀᴛᴜs:** `Playing`\n🎧 **ʀᴇǫᴜᴇsᴛ ʙʏ:** {requester}",
                                reply_markup=keyboard,
                            )
                        except Exception as ep:
                            await suhu.delete()
                            await m.reply_text(f"🚫 اسـف حـدث خـطـا ♬.. : `{ep}`")


# stream is used for live streaming only


@Client.on_message(command(["stream", f"stream@{BOT_USERNAME}", "يوتيوب","رابط","y"]) & other_filters)
async def stream(c: Client, m: Message):
    chat_id = m.chat.id
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="_♬ تـــحـــكـــم ♬_", callback_data="cbmenu"),
                InlineKeyboardButton(text="_♬ خــروج ♬_", callback_data="cls"),
            ]
        ]
    )
    if m.sender_chat:
        return await m.reply_text("you're an __Anonymous Admin__ !\n\n» revert back to user account from admin rights.")
    try:
        aing = await c.get_me()
    except Exception as e:
        return await m.reply_text(f"اسـف حـدث خـطـا ♬.. :\n\n{e}")
    a = await c.get_chat_member(chat_id, aing.id)
    if a.status != "administrator":
        await m.reply_text(
            f"💡 لـي اسـتـخـدامي ♬.. ، يـجـب انن اكـون مـشـرف بـي الـصـلاحـيـات الـتـالـيه ↓ : \ n \ n »❌  حذف الرسائل  \ n» ❌  تقييد المستخدمين  \ n »❌ إضافة مستخدمين  \ n» ❌ إدارة محادثة الفيديو \ n \ n يتم تحديث البيانات  تلقائيًا بعد  ترقيتي**"
        )
        return
    try:
        ubot = await user.get_me()
        b = await c.get_chat_member(chat_id, ubot.id)
        if b.status == "kicked":
            await m.reply_text(
                f"@{ASSISTANT_NAME} **.. ♬ فـي حـد طـرد الـحسـاب الـمـسـاعـد** {m.chat.title}\n\n» **.. ♬ شـيـلـو مـن الـمـحـظـوريـن او كـلـمـنـي هـنـا.**"
            )
            return
    except UserNotParticipant:
        if m.chat.username:
            try:
                await user.join_chat(m.chat.username)
            except Exception as e:
                await m.reply_text(f"❌ **فـشـل الـبـوت فـي دخـول الـمـجـمـوعـه**\n\n**reason**: `{e}`")
                return
        else:
            try:
                pope = await c.export_chat_invite_link(chat_id)
                pepo = await c.revoke_chat_invite_link(chat_id, pope)
                await user.join_chat(pepo.invite_link)
            except UserAlreadyParticipant:
                pass
            except Exception as e:
                return await m.reply_text(
                    f"❌ **فـشـل الـبـوت فـي دخـول الـمـجـمـوعـه**\n\n**reason**: `{e}`"
                )

    if len(m.command) < 2:
        await m.reply("» give me a live-link/m3u8 url/youtube link to stream.")
    else:
        link = m.text.split(None, 1)[1]
        suhu = await c.send_message(chat_id, "🔄 **ᴘʀᴏᴄᴇssɪɴɢ sᴛʀᴇᴀᴍ...**")

        regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(regex, link)
        if match:
            veez, livelink = await ytdl(link)
        else:
            livelink = link
            veez = 1

        if veez == 0:
            await suhu.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
        else:
            if chat_id in QUEUE:
                pos = add_to_queue(chat_id, "Radio", livelink, link, "Audio", 0)
                await suhu.delete()
                requester = f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                await m.reply_photo(
                    photo=f"{IMG_1}",
                    caption=f"💡 **Track added to queue »** `{pos}`\n\n💭 **Chat:** `{chat_id}`\n🎧 **Request by:** {requester}",
                    reply_markup=keyboard,
                )
            else:
                try:
                    await suhu.edit("🔄 **لـحـظـه اطـلـع الـكـول ♬.. **")
                    await call_py.join_group_call(
                        chat_id,
                        AudioPiped(
                            livelink,
                        ),
                        stream_type=StreamType().live_stream,
                    )
                    add_to_queue(chat_id, "Radio", livelink, link, "Audio", 0)
                    await suhu.delete()
                    requester = (
                        f"[{m.from_user.first_name}](tg://user?id={m.from_user.id})"
                    )
                    await m.reply_photo(
                        photo=f"{IMG_2}",
                        caption=f"💡 **[Music live]({link}) stream started.**\n\n💭 **Chat:** `{chat_id}`\n💡 **Status:** `Playing`\n🎧 **Request by:** {requester}",
                        reply_markup=keyboard,
                    )
                except Exception as ep:
                    await suhu.delete()
                    await m.reply_text(f"🚫 اسـف حـدث خـطـا ♬.. : `{ep}`")
