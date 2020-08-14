# Copyright (C) 2020 MoveAngel and MinaProject
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Multifunction memes
#
# Based code + improve from AdekMaulana and aidilaryanto

import asyncio
from asyncio.exceptions import TimeoutError
import re
import random
from telethon import events
import os
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputMediaUploadedDocument,
    InputPeerNotifySettings,
    InputStickerSetID,
    InputStickerSetShortName,
    MessageMediaPhoto)
from userbot import bot, CMD_HELP, TEMP_DOWNLOAD_DIRECTORY
from userbot.events import register


EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+")


@register(outgoing=True, pattern="^.mmf(?: |$)(.*)")
async def mim(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit(
            "`Syntax: reply to an image with .mmf` 'text on top' ; 'text on bottom' "
        )
        return

    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("```reply to a image/sticker/gif```")
        return
    if reply_message.sender.bot:
        await event.edit("```Reply to actual users message.```")
        return
    else:
        await event.edit(
            "```Transfiguration Time! Mwahaha Memifying this image! (」ﾟﾛﾟ)｣ ```"
        )

    chat = "@MemeAutobot"
    async with bot.conversation(chat) as bot_conv:
        try:
            memeVar = event.pattern_match.group(1)
            await silently_send_message(bot_conv, "/start")
            await asyncio.sleep(1)
            await silently_send_message(bot_conv, memeVar)
            await bot.send_file(chat, reply_message.media)
            response = await bot_conv.get_response()
        except YouBlockedUserError:
            await event.reply("```Please unblock @MemeAutobot and try again```")
            return
        if response.text.startswith("Forward"):
            await event.edit(
                "```can you kindly disable your forward privacy settings for good, Nibba?```"
            )
        if "Okay..." in response.text:
            await event.edit(
                "```🛑 🤨 NANI?! This is not an image! This will take sum tym to convert to image... UwU 🧐 🛑```"
            )
            input_str = event.pattern_match.group(1)
            if event.reply_to_msg_id:
                file_name = "meme.png"
                reply_message = await event.get_reply_message()
                downloaded_file_name = os.path.join(
                    TEMP_DOWNLOAD_DIRECTORY, file_name)
                downloaded_file_name = await bot.download_media(
                    reply_message, downloaded_file_name,
                )
                if os.path.exists(downloaded_file_name):
                    await bot.send_file(
                        chat,
                        downloaded_file_name,
                        force_document=False,
                        supports_streaming=False,
                        allow_cache=False,
                    )
                    os.remove(downloaded_file_name)
                else:
                    await event.edit("File Not Found {}".format(input_str))
            response = await bot_conv.get_response()
            files_name = "memes.webp"
            download_file_name = os.path.join(
                TEMP_DOWNLOAD_DIRECTORY, files_name)
            await bot.download_media(
                response.media, download_file_name,
            )
            await bot.send_file(  # pylint:disable=E0602
                event.chat_id,
                download_file_name,
                supports_streaming=False,
                caption="Memifyed",
            )
            await event.delete()
        elif not is_message_image(reply_message):
            await event.edit(
                "Invalid message type. Plz choose right message type u NIBBA."
            )
            return
        else:
            await bot.send_file(event.chat_id, response.media)
            await event.delete()


def is_message_image(message):
    if message.media:
        if isinstance(message.media, MessageMediaPhoto):
            return True
        if message.media.document:
            if message.media.document.mime_type.split("/")[0] == "image":
                return True
        return False
    return False


async def silently_send_message(conv, text):
    await conv.send_message(text)
    response = await conv.get_response()
    await conv.mark_read(message=response)
    return response


@register(outgoing=True, pattern=r"^\.q")
async def quotess(qotli):
    if qotli.fwd_from:
        return
    if not qotli.reply_to_msg_id:
        return await qotli.edit("```Reply to any user message.```")
    reply_message = await qotli.get_reply_message()
    if not reply_message.text:
        return await qotli.edit("```Reply to text message```")
    chat = "@QuotLyBot"
    if reply_message.sender.bot:
        return await qotli.edit("```Reply to actual users message.```")
    await qotli.edit("```Making a Quote```")
    try:
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(
                        incoming=True,
                        from_users=1031952739))
                msg = await bot.forward_messages(chat, reply_message)
                response = await response
                """ - don't spam notif - """
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                return await qotli.reply("```Please unblock @QuotLyBot and try again```")
            if response.text.startswith("Hi!"):
                await qotli.edit("```Can you kindly disable your forward privacy settings for good?```")
            else:
                await qotli.delete()
                await bot.forward_messages(qotli.chat_id, response.message)
                await bot.send_read_acknowledge(qotli.chat_id)
                """ - cleanup chat after completed - """
                await qotli.client.delete_messages(conv.chat_id,
                                                   [msg.id, response.id])
    except TimeoutError:
        await qotli.edit()


@register(outgoing=True, pattern=r'^.hz(:? |$)(.*)?')
async def hazz(hazmat):
    await hazmat.edit("`Sending information...`")
    level = hazmat.pattern_match.group(2)
    if hazmat.fwd_from:
        return
    if not hazmat.reply_to_msg_id:
        await hazmat.edit("`WoWoWo Capt!, we are not going suit a ghost!...`")
        return
    reply_message = await hazmat.get_reply_message()
    if not reply_message.media:
        await hazmat.edit("`Word can destroy anything Capt!...`")
        return
    if reply_message.sender.bot:
        await hazmat.edit("`Reply to actual user...`")
        return
    chat = "@hazmat_suit_bot"
    await hazmat.edit("```Suit Up Capt!, We are going to purge some virus...```")
    message_id_to_reply = hazmat.message.reply_to_msg_id
    msg_reply = None
    async with hazmat.client.conversation(chat) as conv:
        try:
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/hazmat {level}"
                msg_reply = await conv.send_message(
                    m,
                    reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            elif reply_message.gif:
                m = f"/hazmat"
                msg_reply = await conv.send_message(
                    m,
                    reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            else:
                response = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await hazmat.reply("`Please unblock` @hazmat_suit_bot`...`")
            return
        if response.text.startswith("I can't"):
            await hazmat.edit("`Can't handle this GIF...`")
            await hazmat.client.delete_messages(
                conv.chat_id,
                [msg.id, response.id, r.id, msg_reply.id])
            return
        else:
            downloaded_file_name = await hazmat.client.download_media(
                response.media,
                TEMP_DOWNLOAD_DIRECTORY
            )
            await hazmat.client.send_file(
                hazmat.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply
            )
            """ - cleanup chat after completed - """
            if msg_reply is not None:
                await hazmat.client.delete_messages(
                    conv.chat_id,
                    [msg.id, msg_reply.id, r.id, response.id])
            else:
                await hazmat.client.delete_messages(conv.chat_id,
                                                    [msg.id, response.id])
    await hazmat.delete()
    return os.remove(downloaded_file_name)


@register(outgoing=True, pattern=r'^.df(:? |$)([1-8])?')
async def fryerrr(fry):
    await fry.edit("`Sending information...`")
    level = fry.pattern_match.group(2)
    if fry.fwd_from:
        return
    if not fry.reply_to_msg_id:
        await fry.edit("`Reply to any user message photo...`")
        return
    reply_message = await fry.get_reply_message()
    if not reply_message.media:
        await fry.edit("`No image found to fry...`")
        return
    if reply_message.sender.bot:
        await fry.edit("`Reply to actual user...`")
        return
    chat = "@image_deepfrybot"
    message_id_to_reply = fry.message.reply_to_msg_id
    async with fry.client.conversation(chat) as conv:
        try:
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/deepfry {level}"
                msg_level = await conv.send_message(
                    m,
                    reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            else:
                response = await conv.get_response()
            """ - don't spam notif - """
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await fry.reply("`Please unblock` @image_deepfrybot`...`")
            return
        if response.text.startswith("Forward"):
            await fry.edit("`Please disable your forward privacy setting...`")
        else:
            downloaded_file_name = await fry.client.download_media(
                response.media,
                TEMP_DOWNLOAD_DIRECTORY
            )
            await fry.client.send_file(
                fry.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply
            )
            """ - cleanup chat after completed - """
            try:
                msg_level
            except NameError:
                await fry.client.delete_messages(conv.chat_id,
                                                 [msg.id, response.id])
            else:
                await fry.client.delete_messages(
                    conv.chat_id,
                    [msg.id, response.id, r.id, msg_level.id])
    await fry.delete()
    return os.remove(downloaded_file_name)


@register(outgoing=True, pattern="^.sg(?: |$)(.*)")
async def lastname(steal):
    if steal.fwd_from:
        return
    if not steal.reply_to_msg_id:
        await steal.edit("```Reply to any user message.```")
        return
    message = await steal.get_reply_message()
    chat = "@SangMataInfo_bot"
    user_id = message.sender.id
    id = f"/search_id {user_id}"
    if message.sender.bot:
        await steal.edit("```Reply to actual users message.```")
        return
    await steal.edit("```Sit tight while I steal some data from NASA```")
    async with bot.conversation(chat) as conv:
        try:
            msg = await conv.send_message(id)
            r = await conv.get_response()
            response = await conv.get_response()
        except YouBlockedUserError:
            await steal.reply("```Please unblock @sangmatainfo_bot and try again```")
            return
        if response.text.startswith("No records"):
            await steal.edit("```No records found for this user```")
            await steal.client.delete_messages(
                conv.chat_id,
                [msg.id, r.id, response.id])
            return
        else:
            respond = await conv.get_response()
            await steal.edit(f"{response.message}")
        await steal.client.delete_messages(
            conv.chat_id,
            [msg.id, r.id, response.id, respond.id])


@register(outgoing=True, pattern="^.waifu(?: |$)(.*)")
async def waifu(animu):
    text = animu.pattern_match.group(1)
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await animu.answer("`No text given, hence the waifu ran away.`")
            return
    animus = [20, 32, 33, 40, 41, 42, 58]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}")
    await sticcers[0].click(animu.chat_id,
                            reply_to=animu.reply_to_msg_id,
                            silent=True if animu.is_reply else False,
                            hide_via=True)
    await animu.delete()


def deEmojify(inputString: str) -> str:
    return re.sub(EMOJI_PATTERN, '', inputString)


CMD_HELP.update({
    "memify":
        ".mmf texttop ; textbottom\
            \nUsage: Reply a sticker/image/gif and send with cmd."
})

CMD_HELP.update({
    "quotly":
        ".q \
          \nUsage: Enhance ur text to sticker."
})

CMD_HELP.update({
    "hazmat":
        ".hz or .hz [flip, x2, rotate (degree), background (number), black]"
    "\nUsage: Reply to a image / sticker to suit up!"
    "\n@hazmat_suit_bot"
})

CMD_HELP.update({
    "deepfry":
        ".df or .df [level(1-8)]"
    "\nUsage: deepfry image/sticker from the reply."
    "\n@image_deepfrybot"
})


CMD_HELP.update({
    "sangmata":
        ".sg \
          \nUsage: Steal ur or friend name."
})


CMD_HELP.update({
    "waifu":
        ".waifu \
          \nUsage: Enchance your text with beautiful anime girl templates. \
          \n@StickerizerBot"
})
