# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Port to UserBot by @MoveAngel

from datetime import datetime
from covid import Covid
from userbot import CMD_HELP
from userbot.events import register

@register(outgoing=True, pattern="^.covid (.*)")
async def corona(event):
    await event.edit("`Processing...`")
    country = event.pattern_match.group(1)
    covid = Covid(source="worldometers")
    country_data = covid.get_status_by_country_name(country)
    if country_data:
        output_text =  f"`Confirmed   : {country_data['confirmed']}`\n"
        output_text += f"`Active      : {country_data['active']}`\n"
        output_text += f"`Deaths      : {country_data['deaths']}`\n"
        output_text += f"`Recovered   : {country_data['recovered']}`\n"
        output_text += f"`New Cases   : {country_data['new_cases']}`\n"
        output_text += f"`New Deaths  : {country_data['new_deaths']}`\n"
        output_text += f"`Critical    : {country_data['critical']}`\n"
        output_text += f"`Total Tests : {country_data['total_tests']}`\n\n"
        output_text += f"Data provided by [Worldometer](https://www.worldometers.info/coronavirus/country/{country})"
    else:
        output_text = "No information yet about this country!"
    await event.edit(f"Corona Virus Info in {country}:\n\n{output_text}")


CMD_HELP.update({
        "covid": 
        ".covid <country>"
        "\nUsage: Get an information about data covid-19 in your country.\n"
    })