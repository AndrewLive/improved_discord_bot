import os, discord
from discord.ext import commands
import random
from asyncio import sleep

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['SHITYOURSELF'])
    async def shityourself(self, ctx):
        """
        Shit yourself
        """

        await ctx.reply(":poop: :poop: :poop: :poop: :poop: :poop: :poop:")

        # enter voice channel and play audio
        if ctx.message.author.voice == None:
            return
        
        channel = ctx.message.author.voice.channel
        voice_client = await channel.connect()

        source = discord.FFmpegPCMAudio('assets/misc/shit.mp3')
        if not voice_client.is_playing():
            voice_client.play(source, after = lambda e: print('DONE'))

            while voice_client.is_playing():
                await sleep(0.1)

            await voice_client.disconnect()