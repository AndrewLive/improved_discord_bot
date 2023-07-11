import os, discord
from discord.ext import commands
from googletrans import Translator
from googletrans import LANGUAGES

# NOTE: Use googletrans 3.1.0a0 or later to resolve "'None' type has no member 'Group'" error

class Translate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cog_translator = Translator()

    @commands.command()
    async def translate(self, ctx, *args):
        print('Translate Command!')
        if ctx.message.reference == None:
            await ctx.reply("Error: No message to translate", mention_author=False)
            return
        
        if len(args) > 3:
            await ctx.reply("Error: Too many arguments specified")
            return

        source = await ctx.fetch_message(ctx.message.reference.message_id)


        # must have at least a dest arg
        # may be (dest) or (src, dest)
        destlang = "en"
        if len(args) != 0:
            destlang = args[len(args) - 1]
        if destlang not in LANGUAGES:
            await ctx.reply("Error: Destination language code not valid")
            return

        srclang = None
        if len(args) == 2:
            srclang = args[0]
        if srclang == None:
            srclang = self.cog_translator.detect(source.content).lang

        if srclang not in LANGUAGES:
            await ctx.reply("Error: Source language code not valid")
            return


        destination = self.cog_translator.translate(source.content, destlang, srclang)
        await ctx.reply(destination.text)
        return