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
    async def translate(self, ctx, srclang=None, destlang='en', *message):
        """
        Translates the message the invoker replied to

        Note:
            Input languages must be in Google Language Code format (https://developers.google.com/admin-sdk/directory/v1/languages)
        
        Arguments:
            srclang: Language of the original message. Auto detects language if none given
            destlang: Intended destination language. Defaults to English
            message: The message you want to translate. If none specified, will translate the replied-to message
        """

        # print('Translate Command!')
        source_message = " ".join(message)
        if message == ():
            if ctx.message.reference == None:
                await ctx.reply("Error: No message to translate", mention_author=False)
                return
            source = await ctx.fetch_message(ctx.message.reference.message_id)
            source_message = source.content

        


        # must have at least a dest arg
        # may be (dest) or (src, dest)
        if destlang not in LANGUAGES:
            await ctx.reply("Error: Destination language code not valid")
            return

        if srclang == None:
            srclang = self.cog_translator.detect(source_message).lang

        if srclang not in LANGUAGES:
            await ctx.reply("Error: Source language code not valid")
            return


        translated = self.cog_translator.translate(source_message, destlang, srclang)

        # TO DO: embed
        await ctx.reply(translated.text)
        return