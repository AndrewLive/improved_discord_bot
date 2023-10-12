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
        self.value = 0
        self.rank_values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Jack":10, "Queen":10, "King":10, "Ace":11}
    
    @property
    def size(self):
        return len(self.hand)

    def calculate_value(self):
        aces = 0
        self.value = 0
        for card in self.hand:
            rank = card.rank
            self.value += self.rank_values[rank]
            if rank == "Ace":
                aces += 1
        
        while aces > 0:
            if self.value <= 21:
                break
            self.value -= 10
            aces -= 1
        return
    
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
    

    def __str__(self):
        s = ''
        s += f'({len(self.hand)} cards, value = {self.value}): '
        for card in self.hand:
            s += f'({card}) '
        return s
    


class Deck():
    def __init__(self, decks:int):
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
    def __init__(self, player):
        self.player = player

        self.player_hand = []
        self.player_hand_value = 0
        self.dealer_hand = []
        self.dealer_hand_value = 0
        self.deck = []
        self.reset()

        self.stand = False

        return



    def reset_deck(self):
        self.deck.clear()
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        for rank in ranks:
            for suit in suits:
                card = StandardCard(rank, suit)
                self.deck.append(card)

        return
    
    def shuffle_deck(self):
        random.shuffle(self.deck)
    
    def reset(self):
        self.player_hand.clear()
        self.dealer_hand.clear()
        self.player_hand_value = 0
        self.dealer_hand_value = 0
        self.reset_deck()
        self.shuffle_deck()



    def calculate_value(self, hand:[StandardCard]):
        aces = 0
        values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Jack":10, "Queen":10, "King":10, "Ace":11}
        value = 0

        for card in hand:
            rank = card.rank
            value += values[rank]
        
        while aces > 0:
            if value > 21:
                value -= 10
                aces -= 1
        
        return value
    

    def deal_initial_hands(self):
        for _ in range(2):
            card = self.deck.pop()
            self.player_hand.append(card)
            card = self.deck.pop()
            self.dealer_hand.append(card)





    def __str__(self):
        s = ''
        s += f'Player: {self.player}\n'

        s += f'Player Hand ({len(self.player_hand)} cards, value = {self.player_hand_value}): '
        for card in self.player_hand:
            s += f'({card}) '
        s += '\n'


        s += f'Dealer Hand ({len(self.dealer_hand)} cards, value = {self.dealer_hand_value}): '
        for card in self.dealer_hand:
            s += f'({card}) '
        s += '\n'

        s += f'Deck ({len(self.deck)}): '
        for card in self.deck:
            s += f'({card}) '
        s += '\n'
        return s
