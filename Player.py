from Cards import get_rank, get_value
from DurakGameRules import possible_attacks, possible_defends
from Human_inputs import human_input, PlayerGameInfo


class Player:
    hand = []
    pgi: PlayerGameInfo = None

    def __init__(self, starting_hand, trump_suit, player_id, cpu: bool = True):
        self.hand = starting_hand
        self.trump = trump_suit
        self.player_id = player_id
        self.cpu: bool = cpu

        if self.cpu:
            self.attack = self.cpu_lowest_value_attack
            self.defend = self.cpu_lowest_value_defend
        else:
            #PGI will be updated in the handle round loop of durakgame.
            self.pgi = PlayerGameInfo(None, None, None, None, None)
            self.attack = self.human_attack
            self.defend = self.human_defend

    def __repr__(self):
        self.sort_cards()
        if len(self.hand) == 0:
            return "Empty Hand"

        string_hand = f"Player {self.player_id}:\n\n"
        for card in self.hand:
            string_hand += f"\t{card}\n"
        return string_hand

    def sort_cards(self):
        trump_suits = [card for card in self.hand if card.suit == self.trump]
        non_trump_suits = [card for card in self.hand if card.suit != self.trump]
        if len(non_trump_suits) > 0:
            non_trump_suits.sort(key=get_rank)
        if len(trump_suits) > 0:
            trump_suits.sort(key=get_rank)

        self.hand = non_trump_suits
        self.hand.extend(trump_suits)

    def update_pgi(self, deck, defender, attackers, table):
        self.pgi.player = self
        self.pgi.deck = deck
        self.pgi.defender = defender
        self.pgi.attackers = attackers
        self.pgi.table = table

    def attack(self):
        pass

    def defend(self):
        pass

    def human_attack(self, defender, table):
        """Gives a prompt to the human, so he can choose to attack.

        Uses PlayerGameInfo (pgi) to tell the player about the state of the game (in standard_actions)."""
        print(self)
        print(f"You are attacking player {defender.player_id}")
        attacks = possible_attacks(self.hand, defender, table)
        if not attacks:
            print("\t\tNo possible attacks")
            print("Type '0' to proceed")
            human_input(0, self.pgi)
            return None

        attack_number = 0
        for attack in attacks:
            print(f"\t\t{attack_number}\t", attack)
            attack_number += 1
        if not table:
            #Don't give the option to hold on to cards if you are the first attacker.
            chosen_attack_number = human_input(len(attacks) - 1, self.pgi)
        else:
            print(f"\t\t{attack_number}\t Hold on to cards")
            chosen_attack_number = human_input(len(attacks), self.pgi)
            if chosen_attack_number == attack_number:
                return None

        self.hand = [card for card in self.hand if card not in attacks[chosen_attack_number]]
        return attacks[chosen_attack_number]

    def human_defend(self, next_defender, table):
        """Gives a prompt to the human, so he can choose how and if he defends.

        Uses PlayerGameInfo (pgi) to tell the player about the state of the game (in standard_actions)."""
        print(self)
        print(f"You are defending: {table}")
        # first_attack is a bool, true if you're defending the first card, false if the attacks are extra cards
        first_attack = all([attacks[1] is None for attacks in table])
        defends = possible_defends(self.hand, table, first_attack, next_defender)
        if not defends:
            print("\t\tNo possible defends")
            print("Type '0' to proceed")
            human_input(0, self.pgi)
            self.hand.extend([attack[0] for attack in table if attack[0]])
            self.hand.extend([attack[1] for attack in table if attack[1]])
            return None

        defend_number = 0
        for defend in defends:
            print(f"\t\t{defend_number}\t", defend)
            defend_number += 1
        print(f"\t\t{defend_number}\t Fail defence and take the cards")
        chosen_defend_number = human_input(len(defends), self.pgi)
        if chosen_defend_number == len(defends):
            self.hand.extend([attack[0] for attack in table if attack[0]])
            self.hand.extend([attack[1] for attack in table if attack[1]])
            return None

        self.hand = [card for card in self.hand if (card not in [defence[1] for defence in defends[chosen_defend_number]]) and
                                                   (card not in [defence[0] for defence in defends[chosen_defend_number]])]
        return defends[chosen_defend_number]

    def cpu_lowest_value_attack(self, defender, table):
        """returns the best attack, based on the lowest value"""
        attacks = possible_attacks(self.hand, defender, table)
        if not attacks:
            return None
        attacks.sort(key=get_value)
        self.hand = [card for card in self.hand if card not in attacks[0]]

        return attacks[0]

    def cpu_lowest_value_defend(self, next_defender, table):
        """returns the best defence, based on the lowest value"""
        # first_attack is a bool, true if you're defending the first card, false if the attacks are extra cards
        first_attack = all([attacks[1] is None for attacks in table])
        defends = possible_defends(self.hand, table, first_attack, next_defender)
        if not defends:
            self.hand.extend([attack[0] for attack in table if attack[0]])
            self.hand.extend([attack[1] for attack in table if attack[1]])
            return None

        self.hand = [card for card in self.hand if (card not in [defence[1] for defence in defends[0]]) and
                                                   (card not in [defence[0] for defence in defends[0]])]
        return defends[0]



