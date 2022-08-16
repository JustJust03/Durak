from Cards import Deck
from Player import Player
from DurakGameRules import check_player_count


class DurakGame:
    """Class to handle all the rounds in the card game."""
    deck: Deck = None
    players: list = []                  # A list of players
    defender: Player = None             # The defending player
    attackers: list = None              # The attacking players, a list of players
    table: list = []                    # A list of lists representing the cards on table: [attack_card, defend_card]
    players_to_grab_cards: list = []    # Keeps track of the players that have to grab a card
    playing: bool = True                # Turns false whenever there is only 1 player left with cards
    rounds: int = 0                     # Keeps track of how many rounds have been played
    not_cpu_player: Player = None       # If there is a human player, save him in here

    def __init__(self, player_count: int):
        self.player_count = player_count
        check_player_count(self.player_count)

        self.deck = Deck()
        self.init_players(6)

        self.handle_rounds()

    def handle_rounds(self):
        """The main loop to run the program.

        Only ends when playing turns false."""
        while self.playing:
            print("\nStart new round?")
            input("> ")
            self.rounds += 1
            self.flip_next_defender(grab_cards=True)
            print(f"Round {self.rounds},    Cards left: {len(self.deck.stockpile)}")
            self.table = []

            self.handle_round()

    def handle_round(self):
        """Handles one single round, including attacking, defending, diverting.

        Ends when there is a Durak (loser),
        or no new cards are played,
        or the maximum number of attacks are played (6).

        1. The first attacker plays his attack.
        2. The defender can choose to defend, divert the attack, or take the cards.
        3. If not diverted, see if attackers can attack again.

        4. The defender can choose to defend, or take the cards.
        5. See if attackers can attack again. if so, return to 4
        """
        self.update_player_info()

        # The first attacker puts the first cards on the table
        first_attacker = self.first_attacker_of_the_round()
        for attack in first_attacker.attack(self.defender, self.table):
            self.players_to_grab_cards.append(first_attacker)
            self.table.append([attack, None])
            self.check_winner()

        attacking = True
        while attacking and self.playing:
            print(f"Players {[player.player_id for player in self.attackers]}")
            print(f"Table: {self.table}\n")

            self.update_player_info()

            defence = self.defender.defend(self.next_defender(), self.table)
            if not defence:
                self.fail_defence()
                attacking = False
            else:
                old_len = len(self.table)
                self.table = defence
                if len(self.table) > old_len:
                    # Attack got diverted to the next defender
                    self.players_to_grab_cards.append(self.defender)
                    self.flip_next_defender(grab_cards=False)
                else:
                    self.update_player_info()
                    print(f"Player {self.defender.player_id}")
                    print(f"Table: {self.table}\n")
                    attacking = False
                    for attacker in self.attackers:
                        attacks = attacker.attack(self.defender, self.table)
                        if attacks:
                            attacking = True
                            for attack in attacks:
                                self.players_to_grab_cards.append(attacker)
                                self.table.append([attack, None])
                                self.check_winner()
        if self.playing:
            self.check_winner()
            """
            print(f"Defender {self.defender}")
            for a in self.attackers:
                print(a)
            """

    def fail_defence(self):
        """The defender get's flipped twice now.

        This is because the defender that failed doesn't get to attack someone first."""
        print("DEFENCE FAILED!")
        self.flip_next_defender(grab_cards=True)

    def init_players(self, cards_in_starting_hand):
        """Creates the amount of players given by player_count and gives them 6 cards.

        Should only be run if the deck is initialized."""
        for id in range(self.player_count):
            starting_hand = self.deck.grab_cards(cards_in_starting_hand)
            if id == 0:
                player = Player(starting_hand, self.deck.trumpcard.suit, id, cpu=False)
                self.not_cpu_player = player
            else:
                player = Player(starting_hand, self.deck.trumpcard.suit, id)
            self.players.append(player)

    def grab_cards(self):
        """Uses players_to_grab_cards to determine who needs to grab cards"""
        if len(self.deck.stockpile) > 0:
            for player in self.players_to_grab_cards:
                player.hand.extend(self.deck.grab_cards(6 - len(player.hand)))
            self.players_to_grab_cards = []

    def first_attacker_of_the_round(self):
        """Determines the first attacker, the player before the defender."""
        for player_number, player in enumerate(self.players):
            if player == self.defender and player_number != 0:
                return self.players[player_number - 1]

        # Only triggers when the first attacker should be the the last player in players
        return self.players[-1]

    def flip_next_defender(self, grab_cards=True):
        """Flips the defender to the next player.

        grab_cards is true when the round was ended,
                      false when the attack was passed on."""
        self.defender = self.next_defender()
        self.attackers = [player for player in self.players if player != self.defender]

        if grab_cards:
            self.grab_cards()
        # If the attacks are looped around to the original attacker, make sure he doesn't have to grab cards
        elif not grab_cards:
            if self.defender in self.players_to_grab_cards:
                self.players_to_grab_cards.remove(self.defender)

    def next_defender(self):
        """Finds the next defender and returns him."""
        for player_number, player in enumerate(self.players):
            if player == self.defender and player_number != len(self.players) - 1:
                return self.players[player_number + 1]
        # Only triggers if the last player in players is the current defender or it's the first round
        return self.players[0]

    def check_winner(self):
        """Checks if a player has 0 card, thus won and is out of the game.

        Print something cool if the player was a human."""
        for player in self.players:
            if len(player.hand) == 0:
                if not player.cpu:
                    print("\t\tGOOD JOB!\n\t\tYou are not the Durak")
                self.players.remove(player)
        self.check_loser()

    def check_loser(self):
        """Checks if only 1 player is left with cards, thus lost the game.

        Print something humiliating if the player was a human."""
        if len(self.players) < 2:
            self.playing = False
            if not self.players[0].cpu:
                print("You suck and are the Durak!")
            else:
                print(f"Player {self.players[0].player_id} lost the game!")

    def update_player_info(self):
        # TODO: update only when the player could need it.
        """Updates the info of the human player if there is one.

        Always upates before the human player can do an action."""
        if self.not_cpu_player:
            self.not_cpu_player.update_pgi(self.deck, self.defender, self.attackers, self.table)







