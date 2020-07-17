# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#

import aiohttp
import os
import time
from github import Github
from datetime import datetime
from userbot.events import register
from userbot import CMD_HELP, GITHUB_ACCESS_TOKEN, GIT_REPO_NAME, bot

GIT_TEMP_DIR = "/One4uBot/temp/"


@register(outgoing=True, pattern=r".git (.*)")
async def github(event):
    username = event.pattern_match.group(1)
    URL = f"https://api.github.com/users/{username}"
    await event.get_chat()
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as request:
            if request.status == 404:
                return await event.reply(f"`{username} not found`")

            result = await request.json()

            url = result.get("html_url", None)
            name = result.get("name", None)
            company = result.get("company", None)
            bio = result.get("bio", None)
            created_at = result.get("created_at", "Not Found")

            REPLY = (
                f"GitHub Info for `{username}`\n"
                f"Username: `{name}`\n"
                f"Bio: `{bio}`\n"
                f"URL: {url}\n"
                f"Company: `{company}`\n"
                f"Created at: `{created_at}`\n"
                f"More info : [Here](https://api.github.com/users/{username}/events/public)")

            if not result.get("repos_url", None):
                return await event.edit(REPLY)
            async with session.get(result.get("repos_url", None)) as request:
                result = request.json
                if request.status == 404:
                    return await event.edit(REPLY)

                result = await request.json()

                REPLY += "\nRepos:\n"

                for nr in range(len(result)):
                    REPLY += f"[{result[nr].get('name', None)}]({result[nr].get('html_url', None)})\n"

                await event.edit(REPLY)


@register(outgoing=True, pattern="^.commit(?: |$)(.*)")
async def download(event):
    if event.fwd_from:
        return
    if GITHUB_ACCESS_TOKEN is None:
        await event.edit("`Please ADD Proper Access Token from github.com`")
        return
    if GIT_REPO_NAME is None:
        await event.edit("`Please ADD Proper Github Repo Name of your userbot`")
        return
    mone = await event.reply("Processing ...")
    if not os.path.isdir(GIT_TEMP_DIR):
        os.makedirs(GIT_TEMP_DIR)
    start = datetime.now()
    reply_message = await event.get_reply_message()
    try:
        time.time()
        print("Downloading to TEMP directory")
        downloaded_file_name = await bot.download_media(
            reply_message.media,
            GIT_TEMP_DIR
        )
    except Exception as e:
        await mone.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
        await event.delete()
        await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
        await mone.edit("Committing to Github....")
        await git_commit(downloaded_file_name, mone)


async def git_commit(file_name, mone):
    content_list = []
    access_token = GITHUB_ACCESS_TOKEN
    g = Github(access_token)
    file = open(file_name, "r", encoding='utf-8')
    commit_data = file.read()
    repo = g.get_repo(GIT_REPO_NAME)
    print(repo.name)
    create_file = True
    contents = repo.get_contents("")
    for content_file in contents:
        content_list.append(str(content_file))
        print(content_file)
    for i in content_list:
        create_file = True
        if i == 'ContentFile(path="' + file_name + '")':
            return await mone.edit("`File Already Exists`")
            create_file = False
    file_name = "userbot/modules/" + file_name
    if create_file:
        file_name = file_name.replace(GIT_TEMP_DIR, "")
        print(file_name)
        try:
            repo.create_file(
                file_name,
                "Uploaded New Plugin",
                commit_data,
                branch="sql-extended")
            print("Committed File")
            ccess = GIT_REPO_NAME
            ccess = ccess.strip()
            await mone.edit(f"`Commited On Your Github Repo`\n\n[Your Modules](https://github.com/{ccess}/tree/sql-extended/userbot/modules/)")
        except BaseException:
            print("Cannot Create Plugin")
            await mone.edit("Cannot Upload Plugin")
    else:
        return await mone.edit("`Committed Suicide`")

CMD_HELP.update({
    "github":
    ".git <username>"
    "\nUsage: Like .whois but for GitHub usernames."
    "\n\n.commit <reply file>"
    "\nUsage: GITHUB File Uploader Plugin for userbot. Heroku Automation should be Enabled."
})
