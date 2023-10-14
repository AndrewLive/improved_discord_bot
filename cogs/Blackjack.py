import os, discord
from discord.ext import commands, tasks
import random
from datetime import datetime, timedelta
from modules.CardGame import GameState


# subclass of GameState that has channel_id
class MessagableGameState(GameState):
    def __init__(self, player_id, channel_id):
        super().__init__()
        self.player_id = player_id
        self.channel_id = channel_id
        return
    




class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games: dict[int, MessagableGameState] = {}
        self.age_check.start()
        return
    
    def cog_unload(self):
        self.age_check.cancel()
        return


    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        await self.processReaction(reaction, user)
        return
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.processReaction(reaction, user)
        return


    async def processReaction(self, reaction, user):
        if reaction.message.author.bot:
            return
        
        
        return
    

    @commands.command()
    async def blackjack(self, ctx):
        player_id = ctx.author.id
        channel_id = ctx.channel.id
        new_game = MessagableGameState(player_id, channel_id)

        # send start game embed
        embed = self.init_embed(ctx.author.name)
        message = await ctx.send(embed=embed)

        # store game state in dict for later retrieval
        self.games[message.id] = new_game

        # send reaction controls
        await message.add_reaction('🖐️')
        await message.add_reaction('🛑')
        
        return
    

    def init_embed(self, username) -> discord.Embed:
        embed = discord.Embed(color=0xede4b2)

        embed.set_author(name='Blackjack')
        embed.set_footer(text='The Art of War - Sun Tzu')
        embed.add_field(name='Game', value=f'Welcome {username}')
        embed.add_field(name='Emote', value='Please react with EMOJI to start the game')

        return embed


    
    @tasks.loop(minutes=15)
    async def age_check(self):
        print('Checking ages of embeds')
        to_remove = set()
        for message_id in self.games.keys():
            game = self.games[message_id]
            channel_id = game.channel_id
            channel = self.bot.get_channel(channel_id)
            message = await channel.fetch_message(channel_id)

            # get datetime info to determine age
            if datetime.now(tz=message.created_at.tzinfo) - message.created_at > timedelta(minutes=15):
                print(f'Removing message from consideration: {message_id}')
                to_remove.add(message_id)
                
        for message_id in to_remove:
            self.games.pop(message_id)
            print(f'{message_id} removed')