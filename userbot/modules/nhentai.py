# Copyright (C) 2020 KeselekPermen69
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.nhentai(?: |$)(.*)")
async def _(hentai):
    if hentai.fwd_from:
        return
    link = hentai.pattern_match.group(1)
    if not link:
        return await hentai.edit("`I can't search nothing`")
    chat = "@nHentaiBot"
    await hentai.edit("```Processing```")
    async with bot.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=424466890))
              msg = await bot.send_message(chat, link)
              response = await response
              """ - don't spam notif - """
              await bot.send_read_acknowledge(conv.chat_id)
          except YouBlockedUserError: 
              await hentai.reply("```Please unblock @nHentaiBot and try again```")
              return
          if response.text.startswith("**Sorry I couldn't get manga from**"):
             await hentai.edit("```I think this is not the right link```")
          else:
             await hentai.delete()
             await bot.send_message(hentai.chat_id, response.message)
             await bot.send_read_acknowledge(hentai.chat_id)
             """ - cleanup chat after completed - """
             await hentai.client.delete_messages(conv.chat_id,
                                                [msg.id, response.id])

CMD_HELP.update({
    "nhentai": 
    ".nhentai <link / code> \
        \nUsage: view nhentai in telegra.ph\n"
    })
