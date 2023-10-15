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
        # print("Processing Reaction")
        if user.bot:
            return
        game = self.games[reaction.message.id]

        # print(game)

        if user.id != game.player_id:
            return
        
        # check game state and process reaction
        if game.game_stage == 'init':
            # print(reaction.emoji)
            if reaction.emoji == '🖐️':
                # print('VALID REACTION')
                game.start_game()

                new_embed = self.game_embed(game)
                await reaction.message.edit(embed = new_embed)

            return
        
        if game.game_stage == 'player_turn':
            if reaction.emoji == '🖐️':
                game.hit()
                # after hit, can be either player_turn or evaluation
                if game.game_stage == 'player_turn':
                    new_embed = self.game_embed(game)
                elif game.game_stage == 'evaluation':
                    game.evaluate_game()
                    new_embed = self.evaluation_embed(game)
                await reaction.message.edit(embed = new_embed)

            if reaction.emoji == '🛑':
                game.stand()
                # after stand, process dealer's turn
                game.play_dealer()
                game.evaluate_game()
                new_embed = self.evaluation_embed(game)
                await reaction.message.edit(embed = new_embed)
            return
        
        if game.game_stage == 'evaluation':
            if reaction.emoji == '🖐️':
                # restart game
                game.reset()
                game.start_game()
                new_embed = self.game_embed(game)
                await reaction.message.edit(embed = new_embed)
                
            if reaction.emoji == '🛑':
                # delete message and delete from dict
                self.games.pop(reaction.message.id)
                await reaction.message.delete()

            return

        
        return
    

    @commands.command(aliases=['bj'])
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
        embed = discord.Embed(color=0x15800b)

        embed.set_author(name='Blackjack')
        embed.set_footer(text='🖐️ to start the game')
        embed.add_field(name='Game', value=f'Welcome {username}')

        return embed
    
    def game_embed(self, game:MessagableGameState):
        embed = discord.Embed(color=0x15800b)

        embed.set_author(name='Blackjack')
        embed.set_footer(text='🖐️ = hit, 🛑 = stand')
        embed.add_field(name='Dealer Hand', value=f'{game.dealer_hand.hand[0]}, Unknown card')
        embed.add_field(name='Player Hand', value=f'{game.player_hand}')

        return embed
    
    def evaluation_embed(self, game:MessagableGameState):
        embed = discord.Embed(color=0x15800b)

        embed.set_author(name='Blackjack')
        embed.set_footer(text='🖐️ = play again, 🛑 = quit game')
        embed.add_field(name='Dealer Hand', value=f'{game.dealer_hand}')
        embed.add_field(name='Player Hand', value=f'{game.player_hand}')
        embed.add_field(name='Winner', value=f'{game.winner}')

        return embed


    
    @tasks.loop(minutes=5)
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