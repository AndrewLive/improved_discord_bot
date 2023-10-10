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

        message = await ctx.send(embed=embed)
        id = message.id
        self.embed_ids.add((id, message.channel.id))
        print(f'Current embed ids: {self.embed_ids}')


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        debug_channel = self.bot.get_channel('970507801539543101')

        print(f'New reaction: {event.emoji}')
        print(f'User: {event.member.name}')

        if (event.message_id, event.channel_id) in self.embed_ids:
            print(f'Reacting to a valid embed!')

            channel = self.bot.get_channel(event.channel_id)
            message = await channel.fetch_message(event.message_id)

            embed_dict = message.embeds[0].to_dict()
            embed_dict['fields'][1]['value'] = f'Last emote was: {event.emoji}'
            new_embed = discord.Embed.from_dict(embed_dict)

            print(message.embeds)
            print(embed_dict)


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

