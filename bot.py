import os

import discord
from discord.utils import get
from discord.ext import commands

from dotenv import load_dotenv
from datetime import date

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!")

user_warnings = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != None and before.channel.id == 800203039327649802:
        if after.channel == None or after.channel.id != 800203039327649802:
            role = get(member.guild.roles, name="vc")
            await member.remove_roles(role)
    elif after.channel != None and after.channel.id == 800203039327649802:
            role = get(member.guild.roles, name="vc")
            await member.add_roles(role)

@bot.command(name='days')
async def days(ctx):
    f_date = date(2019, 10, 15)
    l_date = date.today()
    delta = l_date - f_date
    msg = 'It has been ' + str(delta.days) + ' days since PL news.'
    await ctx.channel.send(msg)

@bot.command(name='warnings')
async def warnings(ctx):
    member = ctx.message.author
    admin_role = get(member.guild.roles, name="Administration")
    mod_role = get(member.guild.roles, name="Moderation")
    if admin_role in ctx.author.roles or mod_role in ctx.author.roles:
        if not user_warnings:
            msg = 'No warnings!'
            await ctx.channel.send(msg)
        else:
            msg = ''
            for entry in user_warnings:
                warnings = user_warnings[entry]
                if len(warnings) != 0:
                    for warning in warnings:
                        msg = msg + entry + ': ' + warning + '\n'  
            await ctx.channel.send(msg)

@bot.command(name='addwarning')
async def addwarning(ctx, *args):
    member = ctx.message.author
    admin_role = get(member.guild.roles, name="Administration")
    mod_role = get(member.guild.roles, name="Moderation")
    if admin_role in member.roles or mod_role in member.roles:
        if len(args) == 2:
            if args[0] in user_warnings:
                warnings = user_warnings[args[0]]
                warnings.append(args[1])
                user_warnings[args[0]] = warnings
                msg = 'Added warning ' + args[1] + ' to user ' + args[0]
                await ctx.channel.send(msg)
            else:
                warnings = [args[1]]
                user_warnings[args[0]] = warnings
                msg = 'Added warning ' + args[1] + ' to user ' + args[0]
                await ctx.channel.send(msg)
        else:
            msg = 'You need exactly two arguments, first being username and second being the warning.'
            await ctx.channel.send(msg)

@bot.command(name='removewarning')
async def removewarning(ctx, *args):
    member = ctx.message.author
    admin_role = get(member.guild.roles, name="Administration")
    mod_role = get(member.guild.roles, name="Moderation")
    if admin_role in member.roles or mod_role in member.roles:
        if len(args) == 2:
            if args[0] in user_warnings:
                warnings = user_warnings[args[0]]
                if int(args[1]) <= len(warnings) and int(args[1]) > 0:
                    if len(warnings) == 1:
                        warn = warnings[0]
                        del user_warnings[args[0]]
                        msg ='Removed ' + warn + ' from user ' + args[0]
                    else:
                        removed_warning = warnings.pop(int(args[1]) - 1)
                        user_warnings[args[0]] = warnings
                        msg ='Removed ' + removed_warning + ' from user ' + args[0]
                    await ctx.channel.send(msg)
                else:
                    msg = 'Warning index not within bounds.  Please use number between 1 and ' + str(len(warnings))
                    await ctx.channel.send(msg)
            else:
                msg = 'User has no warnings!'
                await ctx.channel.send(msg)
        else:
            msg = 'You need exactly two arguments, first being username and second being the index of warning to remove.'
            await ctx.channel.send(msg)




bot.run(TOKEN)
