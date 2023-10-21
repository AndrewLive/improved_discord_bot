import os, discord
from discord.ext import commands, tasks
import random
from datetime import datetime, timedelta
from modules.CardGame import GameState, StandardCard


# subclass of GameState that has channel_id
class MessagableGameState(GameState):
    def __init__(self, player_id, channel_id):
        super().__init__()
        self.player_id = player_id
        self.channel_id = channel_id
        self.last_interact = datetime.now()
        return
    

# Game Control Buttons
class ControlButtons(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(discord.ui.Button(label="Start"))
        self.add_item(discord.ui.Button(label="Quit"))

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green)
    async def hitBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Hit", ephemeral=True)
        return
    
    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red)
    async def standBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Stand", ephemeral=True)
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
        
        # check that game is still in play
        if reaction.message.id not in self.games.keys():
            return
        game = self.games[reaction.message.id]

        # print(game)

        if user.id != game.player_id:
            return
        
        game.last_interact = datetime.now()
        
        # check game state and process reaction
        if game.game_stage == 'init':
            # print(reaction.emoji)
            if reaction.emoji == '🖐️':
                # print('VALID REACTION')
                game.start_game()

                new_embed = self.game_embed(game)
                await reaction.message.edit(embed = new_embed, view=ControlButtons())

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
                await reaction.message.edit(embed = new_embed, view=ControlButtons())

            if reaction.emoji == '🛑':
                game.stand()
                # after stand, process dealer's turn
                game.play_dealer()
                game.evaluate_game()
                new_embed = self.evaluation_embed(game)
                await reaction.message.edit(embed = new_embed, view=ControlButtons())
            return
        
        if game.game_stage == 'evaluation':
            if reaction.emoji == '🖐️':
                # restart game
                game.reset()
                game.start_game()
                new_embed = self.game_embed(game)
                await reaction.message.edit(embed = new_embed, view=ControlButtons())
                
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
        message = await ctx.send(embed=embed, view=ControlButtons())

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
        embed.add_field(name='Dealer Hand', value=f'{self.getCardStr(game.dealer_hand.hand[0])} ??', inline=False)
        card_strings = [self.getCardStr(card) for card in game.player_hand.hand]
        embed.add_field(name='Player Hand', value=f'{" ".join(card_strings)}', inline=False)

        return embed
    
    def evaluation_embed(self, game:MessagableGameState):
        embed = discord.Embed(color=0x15800b)

        embed.set_author(name='Blackjack')
        embed.set_footer(text='🖐️ = play again, 🛑 = quit game')
        card_strings = [self.getCardStr(card) for card in game.dealer_hand.hand]
        embed.add_field(name='Dealer Hand', value=f'{" ".join(card_strings)}', inline=False)
        card_strings = [self.getCardStr(card) for card in game.player_hand.hand]
        embed.add_field(name='Player Hand', value=f'{" ".join(card_strings)}', inline=False)
        embed.add_field(name='Winner', value=f'{game.winner}', inline=False)

        return embed
    

    def getCardStr(self, card:StandardCard) -> str:
        rank = card.rank
        suite = card.suit
        if (suite == 'Hearts'):
            suite = '♥️'
        elif (suite == "Clubs"):
            suite = '♣️'
        elif (suite == "Diamonds"):
            suite = '♦️'
        elif (suite == "Spades"):
            suite = '♠️'
        
        return f'{rank}{suite}'

    
    @tasks.loop(minutes=5)
    async def age_check(self):
        print('Checking ages of embeds')
        to_remove = set()
        for message_id in self.games.keys():
            game = self.games[message_id]
            channel_id = game.channel_id
            last_interact = game.last_interact
            channel = self.bot.get_channel(channel_id)
            message = await channel.fetch_message(message_id)

            # get datetime info to determine age
            if datetime.now(tz=last_interact.tzinfo) - last_interact > timedelta(minutes=15):
                print(f'Removing message from consideration: {message_id}')
                to_remove.add(message_id)
                
        for message_id in to_remove:
            self.games.pop(message_id)
            print(f'{message_id} removed')