import os, discord
from discord.ext import commands
import random

class Card():
    def __init__(self):
        return
    

class StandardCard(Card):
    def __init__(self, rank, suit):
        super().__init__()
        self.rank = rank
        self.suit = suit
        return
    
    def __str__(self):
        return f'{self.rank} of {self.suit}'
    

class UnoCard(Card):
    def __init__(self):
        super().__init__()
        return
    


class BlackJackHand():
    def __init__(self):
        self.hand = []
        self.rank_values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Jack":10, "Queen":10, "King":10, "Ace":11}
    
    @property
    def size(self):
        return len(self.hand)
    
    @property
    def value(self):
        return self.calculate_value()

    def calculate_value(self):
        aces = 0
        value = 0
        for card in self.hand:
            rank = card.rank
            value += self.rank_values[rank]
            if rank == "Ace":
                aces += 1
        
        while aces > 0:
            if value <= 21:
                break
            value -= 10
            aces -= 1
        return value
    
    def append_card(self, card:StandardCard):
        self.hand.append(card)
        self.calculate_value()
        return
    
    def pop_card(self, rank = None)->StandardCard:
        # if rank specified, will not remove if not found
        card = None
        if rank in self.rank_values.keys():
            for c in reversed(self.hand):
                if c.rank == rank:
                    card = c
                    self.hand.remove(card)
                    break
        else:
            card = self.hand.pop()
        self.calculate_value()
        return card
    
    def clear(self):
        self.hand.clear()
        return
    

    def __str__(self):
        s = ''
        s += f'({len(self.hand)} cards, value = {self.value}): '
        for card in self.hand:
            s += f'({card}) '
        return s
    


class Deck():
    def __init__(self, decks:int = 1):
        self.deck = []
        self.ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        self.decks = decks

        for _ in range(decks):
            for rank in self.ranks:
                for suit in self.suits:
                    card = StandardCard(rank, suit)
                    self.deck.append(card)
    
    @property
    def size(self):
        return len(self.deck)
        

    def shuffle(self):
        random.shuffle(self.deck)
        return
    
    def draw(self)->StandardCard:
        card = self.deck.pop()
        return card
    
    def bury_card(self, card:StandardCard):
        self.deck.insert(0, card)
        return
    
    def return_card(self, card:StandardCard):
        self.deck.append(card)
        return
    
    def __str__(self):
        s = ''
        s += f'{self.size} cards: '
        for card in self.deck:
            s += f'({card}) '
        return s



    

# BlackJack
class GameState():
    def __init__(self):
        self.player_hand = BlackJackHand()
        self.dealer_hand = BlackJackHand()
        self.deck = Deck()

        # keep track of game stage
        # ['init', 'player_turn', 'dealer_turn', 'evaluation']
        self.game_stage = 'init'
        self.winner = None

        return



    def reset(self):
        # resets game to the 'init' state
        self.player_hand = BlackJackHand()
        self.dealer_hand = BlackJackHand()
        self.deck = Deck()

        self.game_stage = 'init'
        self.winner = None
        return
    
    def start_game(self):
        # starts game by dealing initial hands from shuffled deck
        # make sure player does not start with 21 bc that just wins the game and is not fun
        while True:
            self.reset()
            self.deck.shuffle()
            self.deal_initial_hands()

            if self.player_hand.value != 21:
                break

        self.game_stage = 'player_turn'
        return
    


    def deal_initial_hands(self):
        cards = []
        for _ in range(4):
            cards.append(self.deck.draw())
        
        for _ in range(2):
            self.player_hand.append_card(cards.pop())
            self.dealer_hand.append_card(cards.pop())

        return
    

    
    def hit(self):
        # player hits for a card
        if self.game_stage != 'player_turn':
            return
        
        card = self.deck.draw()
        self.player_hand.append_card(card)

        # check hand value
        if self.player_hand.value > 21:
            self.game_stage = 'evaluation'
            return

        return
    
    def stand(self):
        # player stands
        if self.game_stage != 'player_turn':
            return
        
        self.game_stage = 'dealer_turn'
        return

    def play_dealer(self):
        # play dealer until dealer hand >= 17
        if self.game_stage != 'dealer_turn':
            return
        
        while True:
            if self.dealer_hand.value >= 17:
                self.game_stage = 'evaluation'
                break

            card = self.deck.draw()
            self.dealer_hand.append_card(card)

        return
    
    def evaluate_game(self):
        # evaluate winner of game at end of round
        if self.game_stage != 'evaluation':
            return
        
        # win cases
        if self.player_hand.value > 21:
            # player bust
            self.winner = 'dealer'
        elif self.dealer_hand.value > 21:
            # dealer bust
            self.winner = 'player'
        elif self.player_hand.value > self.dealer_hand.value:
            # player win
            self.winner = 'player'
        elif self.player_hand.value == self.dealer_hand.value:
            # tie
            self.winner = None
        else:
            # dealer win
            self.winner = 'dealer'

        return

    def __str__(self):
        s = ''

        s += f'Player Hand: {self.player_hand}\n'
        s += f'Dealer Hand: {self.dealer_hand}\n'
        s += f'Deck: {self.deck}\n'

        s += f'Game Stage: {self.game_stage}\n'
        s += f'Winner: {self.winner}\n'
        return s
