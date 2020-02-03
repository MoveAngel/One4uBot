# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module containing commands related to the \
    Information Superhighway (yes, Internet). """

from datetime import datetime
import io
import speedtest
from telethon import functions
from userbot import CMD_HELP, bot
from userbot.events import register


@register(outgoing=True, pattern="^.speedtest(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    as_text = False
    as_document = True
    if input_str == "image":
        as_document = False
    elif input_str == "file":
        as_document = True
    elif input_str == "text":
        as_text = True
    await event.edit("Calculating my internet speed. Please wait!")
    start = datetime.now()
    s = speedtest.Speedtest()
    s.get_best_server()
    s.download()
    s.upload()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    response = s.results.dict()
    download_speed = response.get("download")
    upload_speed = response.get("upload")
    ping_time = response.get("ping")
    client_infos = response.get("client")
    i_s_p = client_infos.get("isp")
    i_s_p_rating = client_infos.get("isprating")
    reply_msg_id = event.message.id
    if event.reply_to_msg_id:
        reply_msg_id = event.reply_to_msg_id
    try:
        response = s.results.share()
        speedtest_image = response
        if as_text:
            await event.edit("""**SpeedTest** completed in {} seconds
Download: {}
Upload: {}
Ping: {}
Internet Service Provider: {}
ISP Rating: {}""".format(ms, convert_from_bytes(download_speed), convert_from_bytes(upload_speed), ping_time, i_s_p, i_s_p_rating))
        else:
            await bot.send_file(
                event.chat_id,
                speedtest_image,
                caption="**SpeedTest** completed in {} seconds".format(ms),
                force_document=as_document,
                reply_to=reply_msg_id,
                allow_cache=False
            )
            await event.delete()
    except Exception as exc:
        await event.edit("""**SpeedTest** completed in {} seconds
Download: {}
Upload: {}
Ping: {}

__With the Following ERRORs__
{}""".format(ms, convert_from_bytes(download_speed), convert_from_bytes(upload_speed), ping_time, str(exc)))


def convert_from_bytes(size):
    power = 2**10
    n = 0
    units = {
        0: "",
        1: "kilobytes",
        2: "megabytes",
        3: "gigabytes",
        4: "terabytes"
    }
    while size > power:
        size /= power
        n += 1
    return f"{round(size, 2)} {units[n]}"


@register(outgoing=True, pattern="^.dc$")
async def neardc(event):
    """ For .dc command, get the nearest datacenter information. """
    result = await event.client(functions.help.GetNearestDcRequest())
    await event.edit(f"Country : `{result.country}`\n"
                     f"Nearest Datacenter : `{result.nearest_dc}`\n"
                     f"This Datacenter : `{result.this_dc}`")


@register(outgoing=True, pattern="^.ping$")
async def pingme(pong):
    """ For .ping command, ping the userbot from any chat.  """
    start = datetime.now()
    await pong.edit("`Pong!`")
    end = datetime.now()
    duration = (end - start).microseconds / 1000
    await pong.edit("`Pong!\n%sms`" % (duration))


CMD_HELP.update(
    {"speed": ".speed\
    \nUsage: Does a speedtest and shows the results."})
CMD_HELP.update(
    {"dc": ".dc\
    \nUsage: Finds the nearest datacenter from your server."})
CMD_HELP.update(
    {"ping": ".ping\
    \nUsage: Shows how long it takes to ping your bot."})
