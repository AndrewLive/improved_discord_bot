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
    def __init__(self, games):
        super().__init__()
        self.games: dict[int, MessagableGameState] = games
        
        #find buttons and keep track of them to disable and enable them
        self.hitButton = None
        self.standButton = None
        self.startButton = None
        self.quitButton = None
        for child in self.children:
            if type(child) == discord.ui.Button:
                if child.label == 'Hit':
                    self.hitButton = child
                if child.label == 'Stand':
                    self.standButton = child
                if child.label == 'Start':
                    self.startButton = child
                if child.label == 'Quit':
                    self.quitButton = child
        

    @discord.ui.button(label="Hit", style=discord.ButtonStyle.green, custom_id="hitBtn", disabled=True)
    async def hitBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        # print('Hit Button pressed!')
        await self.processButton(interaction, button)
        await interaction.response.defer()
        return
    
    @discord.ui.button(label="Stand", style=discord.ButtonStyle.red, custom_id="standBtn", disabled=True)
    async def standBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        # print('Stand Button pressed!')
        await self.processButton(interaction, button)
        await interaction.response.defer()
        return
    
    @discord.ui.button(label="Start", style=discord.ButtonStyle.blurple, custom_id="startBtn", disabled=False)
    async def startBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        # print('Start Button pressed!')
        await self.processButton(interaction, button)
        await interaction.response.defer()
        return
    
    @discord.ui.button(label="Quit", style=discord.ButtonStyle.blurple, custom_id="quitBtn", disabled=False)
    async def quitBtn(self, interaction: discord.Interaction, button: discord.ui.Button):
        # print('Quit Button pressed!')
        await self.processButton(interaction, button)
        await interaction.response.defer()
        return
    
    # Process the reaction
    async def processButton(self, interaction, button):
        # print("Processing Reaction")
        if interaction.user.bot:
            return
        
        # check that game is still in play
        if interaction.message.id not in self.games.keys():
            return
        game = self.games[interaction.message.id]

        # print(game)

        if interaction.user.id != game.player_id:
            return
        
        game.last_interact = datetime.now()

        # print('evaluating game state')
        
        # check game state and process reaction
        if button.custom_id == 'quitBtn':
            # delete message and delete from dict
            self.games.pop(interaction.message.id)
            await interaction.message.delete()
            return
        
        if game.game_stage == 'init':
            # print(reaction.emoji)
            if (button.custom_id == 'startBtn') or (button.custom_id == 'hitBtn'):
                # print('VALID REACTION')
                game.start_game()

                new_embed = self.game_embed(game)
                self.hitButton.disabled = False
                self.standButton.disabled = False
                self.startButton.disabled = True

                self.games[interaction.message.id] = game
                await interaction.message.edit(embed = new_embed, view=self)

            return
        
        if game.game_stage == 'player_turn':
            if button.custom_id == 'hitBtn':
                game.hit()
                # after hit, can be either player_turn or evaluation
                if game.game_stage == 'player_turn':
                    new_embed = self.game_embed(game)
                elif game.game_stage == 'evaluation':
                    game.evaluate_game()
                    new_embed = self.evaluation_embed(game)
                    self.hitButton.disabled = True
                    self.standButton.disabled = True
                    self.startButton.disabled = False

                self.games[interaction.message.id] = game
                await interaction.message.edit(embed = new_embed, view=self)

            if button.custom_id == 'standBtn':
                game.stand()
                # after stand, process dealer's turn
                game.play_dealer()
                game.evaluate_game()
                new_embed = self.evaluation_embed(game)
                self.hitButton.disabled = True
                self.standButton.disabled = True
                self.startButton.disabled = False

                self.games[interaction.message.id] = game
                await interaction.message.edit(embed = new_embed, view=self)
            return
        
        if game.game_stage == 'evaluation':
            if (button.custom_id == 'startBtn') or (button.custom_id == 'hitBtn'):
                # restart game
                game.reset()
                game.start_game()
                new_embed = self.game_embed(game)
                self.hitButton.disabled = False
                self.standButton.disabled = False
                self.startButton.disabled = True

                self.games[interaction.message.id] = game
                await interaction.message.edit(embed = new_embed, view=self)
                
            if button.custom_id == 'quitBtn':
                # delete message and delete from dict
                self.games.pop(interaction.message.id)
                await interaction.message.delete()

            return

        
        return
    

    # Need these here bc interactivity moved to this class
    def init_embed(self, username) -> discord.Embed:
        embed = discord.Embed(color=0x15800b)

        embed.set_author(name='Blackjack')
        # embed.set_footer(text='🖐️ to start the game')
        embed.add_field(name='Game', value=f'Welcome {username}')

        return embed
    
    def game_embed(self, game:MessagableGameState):
        embed = discord.Embed(color=0x15800b)

        embed.set_author(name='Blackjack')
        # embed.set_footer(text='🖐️ = hit, 🛑 = stand')
        embed.add_field(name='Dealer Hand', value=f'{self.getCardStr(game.dealer_hand.hand[0])} ??', inline=False)
        card_strings = [self.getCardStr(card) for card in game.player_hand.hand]
        embed.add_field(name='Player Hand', value=f'{" ".join(card_strings)}', inline=False)

        return embed
    
    def evaluation_embed(self, game:MessagableGameState):
        embed = discord.Embed(color=0x15800b)

        embed.set_author(name='Blackjack')
        # embed.set_footer(text='🖐️ = play again, 🛑 = quit game')
        card_strings = [self.getCardStr(card) for card in game.dealer_hand.hand]
        embed.add_field(name='Dealer Hand', value=f'{" ".join(card_strings)}', inline=False)
        card_strings = [self.getCardStr(card) for card in game.player_hand.hand]
        embed.add_field(name='Player Hand', value=f'{" ".join(card_strings)}', inline=False)
        embed.add_field(name='Winner', value=f'{game.winner}', inline=False)

        return embed
    

    def getCardStr(self, card:StandardCard) -> str:
        rank = card.rank
        if (rank == 'Jack'):
            rank = 'J'
        elif (rank == 'Queen'):
            rank = 'Q'
        elif (rank == 'King'):
            rank = 'K'
        elif (rank == 'Ace'):
            rank = 'A'
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
    
    



class Blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.games: dict[int, MessagableGameState] = {}

        self.buttons = ControlButtons(self.games)
        self.age_check.start()
        return
    
    def cog_unload(self):
        self.age_check.cancel()
        return

    @commands.command(aliases=['bj'])
    async def blackjack(self, ctx):
        """
        Initiates a game of Blackjack
        """
        # print(f'Blackjack game initialized by {ctx.author.id}')
        player_id = ctx.author.id
        channel_id = ctx.channel.id
        new_game = MessagableGameState(player_id, channel_id)

        # send start game embed
        # print(f'Sending game embed...')
        embed = self.init_embed(ctx.author.name)
        # init a new Buttons obj to try to fix non-responsiveness after long time issue
        buttons = ControlButtons(self.games)
        message = await ctx.send(embed=embed, view=buttons)
        # print(f'Game embed sent!')

        # store game state in dict for later retrieval
        self.games[message.id] = new_game

        # # send reaction controls
        # await message.add_reaction('🖐️')
        # await message.add_reaction('🛑')
        
        return
    

    # @commands.Cog.listener()
    # async def on_reaction_add(self, reaction, user):
    #     await self.processReaction(reaction, user)
    #     return
    
    # @commands.Cog.listener()
    # async def on_reaction_remove(self, reaction, user):
    #     await self.processReaction(reaction, user)
    #     return


    # async def processReaction(self, reaction, user):
    #     # print("Processing Reaction")
    #     if user.bot:
    #         return
        
    #     # check that game is still in play
    #     if reaction.message.id not in self.games.keys():
    #         return
    #     game = self.games[reaction.message.id]

    #     # print(game)

    #     if user.id != game.player_id:
    #         return
        
    #     game.last_interact = datetime.now()
        
    #     # check game state and process reaction
    #     if game.game_stage == 'init':
    #         # print(reaction.emoji)
    #         if reaction.emoji == '🖐️':
    #             # print('VALID REACTION')
    #             game.start_game()

    #             new_embed = self.game_embed(game)
    #             await reaction.message.edit(embed = new_embed, view=self.buttons)

    #         return
        
    #     if game.game_stage == 'player_turn':
    #         if reaction.emoji == '🖐️':
    #             game.hit()
    #             # after hit, can be either player_turn or evaluation
    #             if game.game_stage == 'player_turn':
    #                 new_embed = self.game_embed(game)
    #             elif game.game_stage == 'evaluation':
    #                 game.evaluate_game()
    #                 new_embed = self.evaluation_embed(game)
    #             await reaction.message.edit(embed = new_embed, view=self.buttons)

    #         if reaction.emoji == '🛑':
    #             game.stand()
    #             # after stand, process dealer's turn
    #             game.play_dealer()
    #             game.evaluate_game()
    #             new_embed = self.evaluation_embed(game)
    #             await reaction.message.edit(embed = new_embed, view=self.buttons)
    #         return
        
    #     if game.game_stage == 'evaluation':
    #         if reaction.emoji == '🖐️':
    #             # restart game
    #             game.reset()
    #             game.start_game()
    #             new_embed = self.game_embed(game)
    #             await reaction.message.edit(embed = new_embed, view=self.buttons)
                
    #         if reaction.emoji == '🛑':
    #             # delete message and delete from dict
    #             self.games.pop(reaction.message.id)
    #             await reaction.message.delete()

    #         return

        
    #     return
    


    
    # @commands.Cog.listener()
    # async def on_raw_button_click(self, interaction, button):
    #     print("Button Clicked!")
    #     await self.processButton(interaction)
    #     return

    
    # async def processButton(self, interaction):
    #     print("Processing Reaction")
    #     if interaction.user.bot:
    #         return
        
    #     # check that game is still in play
    #     if interaction.message.id not in self.games.keys():
    #         return
    #     game = self.games[interaction.message.id]

    #     # print(game)

    #     if interaction.user.id != game.player_id:
    #         return
        
    #     game.last_interact = datetime.now()
        
    #     # check game state and process reaction
    #     if game.game_stage == 'init':
    #         # print(reaction.emoji)
    #         if interaction.custom_id == 'startBtn':
    #             # print('VALID REACTION')
    #             game.start_game()

    #             new_embed = self.game_embed(game)
    #             await interaction.message.edit(embed = new_embed, view=self.buttons)

    #         return
        
    #     if game.game_stage == 'player_turn':
    #         if interaction.custom_id == 'hitBtn':
    #             game.hit()
    #             # after hit, can be either player_turn or evaluation
    #             if game.game_stage == 'player_turn':
    #                 new_embed = self.game_embed(game)
    #             elif game.game_stage == 'evaluation':
    #                 game.evaluate_game()
    #                 new_embed = self.evaluation_embed(game)
    #             await interaction.message.edit(embed = new_embed, view=self.buttons)

    #         if interaction.custom_id == 'standBtn':
    #             game.stand()
    #             # after stand, process dealer's turn
    #             game.play_dealer()
    #             game.evaluate_game()
    #             new_embed = self.evaluation_embed(game)
    #             await interaction.message.edit(embed = new_embed, view=self.buttons)
    #         return
        
    #     if game.game_stage == 'evaluation':
    #         if interaction.custom_id == 'startBtn':
    #             # restart game
    #             game.reset()
    #             game.start_game()
    #             new_embed = self.game_embed(game)
    #             await interaction.message.edit(embed = new_embed, view=self.buttons)
                
    #         if interaction.custom_id == 'quitBtn':
    #             # delete message and delete from dict
    #             self.games.pop(interaction.message.id)
    #             await interaction.message.delete()

    #         return

        
    #     return
    

    def init_embed(self, username) -> discord.Embed:
        embed = discord.Embed(color=0x15800b)

        embed.set_author(name='Blackjack')
        # embed.set_footer(text='🖐️ to start the game')
        embed.add_field(name='Game', value=f'Welcome {username}')

        return embed
    
    def game_embed(self, game:MessagableGameState):
        embed = discord.Embed(color=0x15800b)

        embed.set_author(name='Blackjack')
        # embed.set_footer(text='🖐️ = hit, 🛑 = stand')
        embed.add_field(name='Dealer Hand', value=f'{self.getCardStr(game.dealer_hand.hand[0])} ??', inline=False)
        card_strings = [self.getCardStr(card) for card in game.player_hand.hand]
        embed.add_field(name='Player Hand', value=f'{" ".join(card_strings)}', inline=False)

        return embed
    
    def evaluation_embed(self, game:MessagableGameState):
        embed = discord.Embed(color=0x15800b)

        embed.set_author(name='Blackjack')
        # embed.set_footer(text='🖐️ = play again, 🛑 = quit game')
        card_strings = [self.getCardStr(card) for card in game.dealer_hand.hand]
        embed.add_field(name='Dealer Hand', value=f'{" ".join(card_strings)}', inline=False)
        card_strings = [self.getCardStr(card) for card in game.player_hand.hand]
        embed.add_field(name='Player Hand', value=f'{" ".join(card_strings)}', inline=False)
        embed.add_field(name='Winner', value=f'{game.winner}', inline=False)

        return embed
    

    def getCardStr(self, card:StandardCard) -> str:
        rank = card.rank
        if (rank == 'Jack'):
            rank = 'J'
        elif (rank == 'Queen'):
            rank = 'Q'
        elif (rank == 'King'):
            rank = 'K'
        elif (rank == 'Ace'):
            rank = 'A'
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
            await message.delete()