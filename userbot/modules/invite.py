from asyncio import sleep
from telethon import functions
from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.invite(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return
    to_add_users = event.pattern_match.group(1)
    if event.is_private:
        await event.edit("`.invite` users to a chat, not to a Private Message")
    else:
        if not event.is_channel and event.is_group:
            # https://lonamiwebs.github.io/Telethon/methods/messages/add_chat_user.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(functions.messages.AddChatUserRequest(
                        chat_id=event.chat_id,
                        user_id=user_id,
                        fwd_limit=1000000
                    ))
                except Exception as e:
                    await event.reply(str(e))
            await event.edit("`Invited Unsuccessfully`")
            await sleep(3)
            await event.delete()
        else:
            # https://lonamiwebs.github.io/Telethon/methods/channels/invite_to_channel.html
            for user_id in to_add_users.split(" "):
                try:
                    await event.client(functions.channels.InviteToChannelRequest(
                        channel=event.chat_id,
                        users=[user_id]
                    ))
                except Exception as e:
                    await event.reply(str(e))
            await event.edit("`Invited Successfully`")
            await sleep(3)
            await event.delete()
            
CMD_HELP.update({
    'invite':
    '.invite <username> \
        \nUsage: Invite some user or bots if u want.'
})
