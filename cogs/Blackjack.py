import os, discord
from discord.ext import commands, tasks
import random
from datetime import datetime, timedelta
from CardGame import GameState

class MessagableGameState(GameState):
    def __init__(self, channel_id):
        super().__init__()
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
        self.processReaction(reaction, user)
        return
    
    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        await self.processReaction(reaction, user)
        return


    async def processReaction(self, reaction, user):
        if reaction.message.author.bot:
            return
        
        
        return






    
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