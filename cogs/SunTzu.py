import os, discord
from discord.ext import commands
import random
from gtts import gTTS


class SunTzu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file = open('sun_tzu.txt', 'r')
        self.lines = self.file.readlines()
        # self.lines.remove('\n')
        self.num_lines = len(self.lines)

    @commands.command(aliases=['st'])
    async def suntzu(self, ctx, channel = 'text'):
        """
        Gives a 100% real totally not made up quote from ancient Chinese general Sun Tzu

        Arguments:
            channel: Whether you want the message to be sent through text or voice (user must be connected to voice channel)
        """

        line = random.choice(self.lines)
        sun_tzu_image = 'https://almabooks.com/wp-content/uploads/2019/08/Sun-Tzu.jpg'

        embed = discord.Embed(color=0xede4b2)

        embed.set_author(name='Sun Tzu', url='https://en.wikipedia.org/wiki/Sun_Tzu', icon_url='https://upload.wikimedia.org/wikipedia/commons/c/cf/%E5%90%B4%E5%8F%B8%E9%A9%AC%E5%AD%99%E6%AD%A6.jpg')
        embed.set_thumbnail(url=sun_tzu_image)
        embed.set_footer(text='The Art of War - Sun Tzu')
        embed.add_field(name='', value=line)


        await ctx.send(embed=embed)

        # create audio file for sun tzu quote
        if channel != 'voice' and channel != 'vc':
            return
        
        audio = gTTS(text = line, lang = 'en', slow = False, tld = "us")
        audio.save("sun_tzu.mp3")
        os.system("mpg321 sun_tzu.mp3")
        return


    @commands.command(aliases=['reloadst', 'rst'])
    async def reloadsuntzu(self, ctx):
        """
        Reloads the list of quotes that Sun Tzu can give (only usable by bot owner)
        """

        if ctx.message.author.id != 389616181331361803:
            # print('not valid user')
            return
        self.file = open('sun_tzu.txt', 'r')
        self.lines = self.file.readlines()
        # self.lines.remove('\n')
        self.num_lines = len(self.lines)
        print('reloaded sun tzu')
        return