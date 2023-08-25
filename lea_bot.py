import os, discord
from dotenv import load_dotenv
from discord.ext import commands, tasks
import logging

from cogs.Translate import Translate
from cogs.Minecraft import Minecraft


load_dotenv()
TOKEN = os.getenv("TOKEN")

INTENTS = discord.Intents.default()
INTENTS.members = True
INTENTS.typing = False
INTENTS.presences = False
INTENTS.message_content = True

PREFIX = "l."

bot = commands.Bot(command_prefix = PREFIX, intents = INTENTS)


@bot.event
async def on_ready():
    print('Adding cogs...')
    await bot.add_cog(Translate(bot))
    await bot.add_cog(Minecraft(bot))

    print('Logged in as {0}!'.format(bot.user))

    return



@bot.event
async def on_message(message):
    # DEBUG REMOVE LATER
    print(str(message.author) + ": " + message.content)

    await bot.process_commands(message)

    return

    


bot.run(TOKEN)