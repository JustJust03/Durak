from sys import exit
from Cards import Deck


class PlayerGameInfo:
    player = None
    deck: Deck = None
    defender = None
    attackers = None
    table = None

    def __init__(self, player, deck, defender, attackers, table):
        self.player = player
        self.deck = deck
        self.defender = defender
        self.attackers = attackers
        self.table = table


def human_input(maxlen, pgi: PlayerGameInfo):
    chosen_attack_number = input("> ")
    try:
        chosen_attack_number = int(chosen_attack_number)
    except ValueError:
        # Input wasn't an integer
        standard_actions(chosen_attack_number, pgi)
        return human_input(maxlen, pgi)
    if chosen_attack_number < 0:
        print("The given number wasn't higher than 0.")
        print(f"Try inputting a number between 0 and {maxlen}")
        return human_input(maxlen, pgi)
    elif chosen_attack_number > maxlen:
        print(f"The given number wasn't lower than {maxlen + 1}.")
        print(f"Try inputting a number between 0 and {maxlen}")
        return human_input(maxlen, pgi)

    return chosen_attack_number


def standard_actions(inp, pgi: PlayerGameInfo):
    inp = inp.lower()
    if inp in ["exit", "quit", "q"]:
        exit("Exitted out of the game")
    elif inp in ["hand", "h"]:
        print(pgi.player)
    elif inp in ["stockpile", "stock", "s"]:
        print(f"Stockpile length: {len(pgi.deck.stockpile)}")
    elif inp in ["opponents", "o", "p"]:
        print(f"Defender:   Player {pgi.defender.player_id}, with {len(pgi.defender.hand)} cards")
        for attacker in pgi.attackers:
            print(f"attacker:   Player {attacker.player_id}, with {len(attacker.hand)} cards")
    elif inp in ["table", "t"]:
        print("Table: ", pgi.table)
    elif inp in ["trump", "trump card", "trumpcard", "tc"]:
        print("Trump card: ", pgi.deck.trumpcard)

    elif inp == "help":
        print("""
            exit (q):       exit's out of the program.
            hand (h):       Shows your hand.
            stockpile (s):  info about the stockpile.
            opponents (o):  info about your opponents.
            table (t):      The table right now.
            trumpcard (tc): the trump card.
        """)
    else:
        print("Try inputting a number, or type 'help' to show commands.")




