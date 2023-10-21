import os, discord
from discord.ext import commands, tasks
import random
from datetime import datetime, timedelta

class EmbedTest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed_ids = set()
        self.age_check.start()

    def cog_unload(self):
        self.age_check.cancel()


    @commands.command(aliases=['test'])
    async def sendtest(self, ctx):
        embed = discord.Embed(color=0xede4b2)

        embed.set_author(name='LeaBot')
        embed.set_footer(text='The Art of War - Sun Tzu')
        embed.add_field(name='Test', value='This is a test embed')
        embed.add_field(name='Emote', value='Last emote was: NONE')
        card1 = discord.File('./assets/blackjack/PNG-cards-1.3/2_of_diamonds.png', filename='2_of_diamonds.png')
        card2 = discord.File('./assets/blackjack/PNG-cards-1.3/5_of_spades.png')
        embed.set_image(url='attachment://2_of_diamonds.png')

        message = await ctx.send(file=card1, embed=embed)
        id = message.id
        self.embed_ids.add((id, message.channel.id))
        print(f'Current embed ids: {self.embed_ids}')

    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(f'New reaction: {reaction.emoji}')
        print(f'User: {user.name}')

        message = reaction.message
        channel = message.channel

        if (message.id, channel.id) in self.embed_ids:
            print(f'Reacting to a valid embed!')

            embed_dict = message.embeds[0].to_dict()
            embed_dict['fields'][1]['value'] = f'Last emote was: {reaction.emoji}'
            new_embed = discord.Embed.from_dict(embed_dict)

            card2 = discord.File('./assets/blackjack/PNG-cards-1.3/5_of_spades.png')
            new_embed.set_image(url='attachment://5_of_spades.png')

            await message.edit(embed = new_embed)

        return
        




    @tasks.loop(minutes=15)
    async def age_check(self):
        print('Checking ages of embeds')
        to_remove = set()
        for tuple in self.embed_ids:
            embed_id = tuple[0]
            channel_id = tuple[1]
            channel = self.bot.get_channel(channel_id)
            embed = await channel.fetch_message(embed_id)

            # get datetime info to determine age
            if datetime.now(tz=embed.created_at.tzinfo) - embed.created_at > timedelta(minutes=15):
                print(f'Removing embed tuple: {tuple}')
                to_remove.add(tuple)
                
        for tuple in to_remove:
            self.embed_ids.remove(tuple)
            print(f'{tuple} removed')

