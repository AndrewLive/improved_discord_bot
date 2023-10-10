import os, discord
from discord.ext import commands
import random

class EmbedTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=['test'])
    async def sendtest(self, ctx):
        embed = discord.Embed(color=0xede4b2)

        embed.set_author(name='LeaBot')
        embed.set_footer(text='The Art of War - Sun Tzu')
        embed.add_field(name='', value='This is a test embed')
        embed.add_field(name='', value='Last emote was: NONE')

        await ctx.send(embed=embed)