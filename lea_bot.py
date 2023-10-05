import os, discord
from typing import Any, List, Mapping, Optional
from discord.ext.commands.cog import Cog
from discord.ext.commands.core import Command, Group
from dotenv import load_dotenv
from discord.ext import commands, tasks
import logging

from CustomHelpCommand import CustomHelpCommand

from cogs.Translate import Translate
from cogs.Minecraft import Minecraft
from cogs.SunTzu import SunTzu


load_dotenv()
TOKEN = os.getenv("TOKEN")

INTENTS = discord.Intents.default()
INTENTS.members = True
INTENTS.typing = False
INTENTS.presences = False
INTENTS.message_content = True

PREFIX = "l."

bot = commands.Bot(command_prefix = PREFIX, intents = INTENTS, help_command=commands.DefaultHelpCommand(show_parameter_descriptions=False))


@bot.event
async def on_ready():
    print('Adding cogs...')
    await bot.add_cog(Translate(bot))
    print('Translate Cog added successfully!')
    # await bot.add_cog(Minecraft(bot))
    # print('Minecraft Cog added successfully!')
    await bot.add_cog(SunTzu(bot))
    print('Sun Tzu Cog added successfully!')

    print('Logged in as {0}!'.format(bot.user))

    return



@bot.event
async def on_message(message):
    # DEBUG REMOVE LATER
    # print(str(message.author) + ": " + message.content)

    await bot.process_commands(message)

    return

    


bot.run(TOKEN)