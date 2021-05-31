import os

import discord
from discord.utils import get

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel != None and before.channel.id == 800203039327649802:
        if after.channel == None or after.channel.id != 800203039327649802:
            role = get(member.guild.roles, name="vc")
            await member.remove_roles(role)
    elif after.channel != None and after.channel.id == 800203039327649802:
            role = get(member.guild.roles, name="vc")
            await member.add_roles(role)



client.run(TOKEN)