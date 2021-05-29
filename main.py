import os
import re
import asyncio

import discord
from discord.ext import commands
import typing
import traceback

TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix=os.getenv('COMMAND_PREFIX') or '!', help_command=None)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


USAGE = client.command_prefix + 'migrate to_channel from_message [to_message] [except_messages_with_this_emoji_reaction]'

@commands.guild_only()
@client.command(name='migrate', aliases=['move'])
async def move_messages(ctx, to_channel: discord.TextChannel, msg_begin: discord.Message, msg_end: typing.Optional[discord.Message]=None, except_emoji: typing.Optional[discord.Emoji]=None):
    await ctx.send(f'We would move the range of messages from {msg_begin} to {msg_end}, excluding those which have this emoji: {except_emoji}, to channel: {to_channel}')


@move_messages.error
async def error(ctx, e):
    print(*traceback.format_exception(None, e, e.__traceback__))
    embed = discord.Embed()
    embed.color = discord.Color.red()
    embed.description = '```\n' + ''.join(traceback.format_exception(None, e, e.__traceback__)[:5500]) + '\n```'
    embed.title = 'Error description for nerds:'
    await ctx.send('There was an error running your command. Please check that you are using the command with the correct arguments:\n```\n' + USAGE + '\n```\n', embed=embed)

client.run(TOKEN)
