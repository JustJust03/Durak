from random import shuffle

suits = {1: "Clubs", 2: "Diamonds", 3: "Hearts", 4: "Spades"}
ranks = {6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "Jack", 12: "Queen", 13: "King", 14: "Ace"}


def get_rank(card):
    return card.rank


def get_suit(card):
    return card.suit


def get_value(cards: list):
    return sum(card.value for card in cards)


class Card:
    """The card object, they should all have a unique suit and rank combination."""

    def __init__(self, suit, rank):
        self.suit = suit  #1-clubs, 2-diamonds, 3-hearts, 4-spades
        self.rank = rank  #2 - 10, 11-jack, 12-queen, 13-king, 14-ace
        self.value = None #Card value is given by the Deck, after the trumpcard was chosen

    def __repr__(self):
        return f"{ranks[self.rank]} of {suits[self.suit]}"


class Deck:
    """Handles everything to do with the deck.

    Holds the stockpile, where the cards are grabbed from.
    the lowest card in the stockpile becomes the trumpcard.
    Assigns values to the cards."""
    stockpile = []
    trumpcard = None

    def __init__(self):
        """Initializes the cards - Get the trumpcard - Assign the value to the cards"""
        for suit in suits.keys():
            for rank in ranks.keys():
                card = Card(suit, rank)
                self.stockpile.append(card)
        shuffle(self.stockpile)
        self.trumpcard = self.stockpile[0]
        self.assign_card_values()

    def __repr__(self):
        represent = ""
        for card in list(reversed(self.stockpile)):
            represent += f"{card}\n"
        return represent

    def grab_cards(self, Nofcards):
        """Returns the top cards from the stockpile give by Nofcards"""
        if len(self.stockpile) == 0:
            return []
        if Nofcards > len(self.stockpile):
            Nofcards = len(self.stockpile)

        return_cards = []
        for card in range(Nofcards):
            return_cards.append(self.stockpile.pop())
        return return_cards

    def assign_card_values(self):
        """card value is the rank of the card, except for the trump cards, they are rank + 20"""
        for card in self.stockpile:
            if card.suit == self.trumpcard.suit:
                card.value = card.rank + 20
            else:
                card.value = card.rank

