# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to userbot by @MoveAngel

import datetime
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from userbot import bot, CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.sg(?: |$)(.*)")
async def lastname(steal):
    if steal.fwd_from:
        return 
    if not steal.reply_to_msg_id:
       await steal.edit("```Reply to any user message.```")
       return
    reply_message = await steal.get_reply_message() 
    if not reply_message.text:
       await steal.edit("```reply to text message```")
       return
    chat = "@SangMataInfo_bot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await steal.edit("```Reply to actual users message.```")
       return
    await steal.edit("```Sit tight while I steal some data from NASA```")
    async with bot.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=461843263))
              await bot.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await steal.reply("```Please unblock @sangmatainfo_bot and try again```")
              return
          if response.text.startswith("Forward"):
             await steal.edit("```can you kindly disable your forward privacy settings for good?```")
          else: 
             await steal.edit(f"{response.message.message}")




@register(outgoing=True, pattern="^.fakemail(?: |$)(.*)")
async def pembohong(fake):
    if fake.fwd_from:
        return 
    if not fake.reply_to_msg_id:
       await fake.edit("```Reply to any user message.```")
       return
    reply_message = await fake.get_reply_message() 
    if not reply_message.text:
       await fake.edit("```reply to text message```")
       return
    chat = "@fakemailbot"
    sender = reply_message.sender
    if reply_message.sender.bot:
       await fake.edit("```Reply to actual users message.```")
       return
    await fake.edit("```Sit tight while I sending some data from Microsoft```")
    async with bot.conversation(chat) as conv:
          try:     
              response = conv.wait_event(events.NewMessage(incoming=True,from_users=177914997))
              await bot.forward_messages(chat, reply_message)
              response = await response 
          except YouBlockedUserError: 
              await fake.reply("```Please unblock @fakemailbot and try again```")
              return
          if response.text.startswith("send"):
             await fake.edit("```can you kindly disable your forward privacy settings for good?```")
          else: 
             await fake.edit(f"{response.message.message}")

CMD_HELP.update({
        "mata mata": 
        ".sg \
          \nUsage: Steal ur or friend name.\
          \n\n.fakemail\
          \nUsage: Fake an email to ur friends or someone."
    })