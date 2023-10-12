from CardGame import Card, StandardCard, BlackJackHand, GameState, Deck
import random

if __name__ == '__main__':
    test_hand = BlackJackHand()
    print(test_hand)

    cards = []
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    for _ in range(3):
        rank = random.choice(ranks)
        suit = random.choice(suits)
        card = StandardCard(rank, suit)
        cards.append(card)

    for card in cards:
        test_hand.append_card(card)

    
    print(test_hand)
    test_hand.pop_card()
    print(test_hand)
    test_hand.pop_card()
    print(test_hand)
    test_hand.pop_card()
    print(test_hand)

    card = StandardCard('Ace', 'Spades')
    test_hand.append_card(card)
    card = StandardCard('10', 'Clubs')
    test_hand.append_card(card)
    card = StandardCard('2', 'Diamonds')
    test_hand.append_card(card)
    print(test_hand)

    print(test_hand.pop_card())
    print(test_hand)
    print(test_hand.pop_card('Ace'))
    print(test_hand)


    test_deck = Deck()
    print(test_deck)
    test_deck.shuffle()
    print(test_deck)
