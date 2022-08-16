from itertools import combinations


def check_player_count(player_count):
    """Raises an error if there are more than 5 or less than 2 players.

    Is only run in the initialization of Durak."""
    if player_count > 5:
        raise ValueError("Can't play Durak with more than 5 players.")
    if player_count < 2:
        raise ValueError("Can't play Durak with less than 2 players.")


def strip_list(l:list):
    """returns the combinations of the cards in the given list

    for example:
        input = [King of Clubs, King of Hearts]
        output = [[King of Clubs], [King of Hearts], [King of Clubs, King of Hearts]]"""
    combis = []
    for i in range(1, len(l)):
        combis.extend(list(combinations(l, i)))
    combis = [list(e) for e in combis]
    combis.append(l)
    return combis


# TODO: Make this uniform, so either possible_attacks returns the whole table,
#                          or possible_defends only returns the now defended cards.
# I think the first one makes more sense
def possible_attacks(hand, defender, table):
    """Returns all possible attacks for this player.

    Returns a list of attacks.
    It doesn't return the whole table like in defends!"""
    # First attack
    if all([attacks[1] is None for attacks in table]):
        attacks = []
        processed_cards = []
        for card in hand:
            if card not in processed_cards:
                card_combination = [c for c in hand if c.rank == card.rank]
                processed_cards.extend(card_combination)
                attacks.extend(strip_list(card_combination))
        attacks = [a for a in attacks if len(a) <= len(defender.hand)]
        return attacks
    # Extra attacks
    else:
        undefended_attacks_on_table = [attack for attack in table if not attack[1]]
        ranks_on_table = [card[1].rank for card in table if card[1]]
        ranks_on_table.extend([card[0].rank for card in table if card[0]])

        attacks = []
        processed_cards = []
        for card in hand:
            if card not in processed_cards and card.rank in ranks_on_table:
                card_combination = [c for c in hand if c.rank == card.rank]
                processed_cards.extend(card_combination)
                attacks.extend(strip_list(card_combination))
        # Only allow the attack, if there aren't more undefended attacks than the amount of cards of the defender
        attacks = [a for a in attacks if len(a) + len(undefended_attacks_on_table) <= len(defender.hand) and
                                         len(a) + len(undefended_attacks_on_table) <= 6]
        return attacks


def cartesian_product2(defences: list):
    return [[x, y] for x in defences[0] for y in defences[1] if x != y]


def cartesian_product3(defences: list):
    return [[x, y, z] for x in defences[0] for y in defences[1] for z in defences[2]
            if (x != y) and (x != z) and (y != z)]


def cartesian_product4(defences: list):
    return [[a, b, c, d] for a in defences[0] for b in defences[1] for c in defences[2] for d in defences[3]
            if (a != b) and (a != c) and (a != d) and (b != c) and (b != d) and (c != d)]


def cartesian_product5(defences: list):
    return [[a, b, c, d, e] for a in defences[0] for b in defences[1] for c in defences[2] for d in defences[3] for e in
            defences[4]
            if (a != b) and (a != c) and (a != d) and (a != e) and (b != c) and (b != d) and (b != e) and (c != d) and (
                        c != e) and (d != e)]


def remove_duplicates(defences: list):
    """Removes duplicate cards from the defences list."""
    for defence in defences:
        for other_defence in [d for d in defences if d != defence]:
            if all(item in other_defence for item in defence):
                defences.remove(other_defence)
    return defences


def possible_defends_per_card(hand, attack):
    """returns a list of cards from the hand that the attack could be defended with."""
    defends = []
    for card in hand:
        if card.suit == attack.suit and card.rank > attack.rank:  # Same suit, higher rank
            defends.append(card)
        elif card.value > 14 and attack.value < 15:  # Trump card to non trump suit
            defends.append(card)
    return defends


def possible_defends(hand, table, first_attack, next_defender):
    """Finds all the possibilities to defend the current table.

    returns a list of the tables with possible defences.
    returns None if the attack could not be defended."""
    undefended_attacks = [attack for attack in table if not attack[1]]
    defended_attacks = [attack for attack in table if attack[1]]
    # Check if the attack can be diverted
    possible_attacks_and_defences = []
    if first_attack:
        pass_on_cards = [card for card in hand if card.rank == undefended_attacks[0][0].rank]
        if pass_on_cards:
            stripped_pass_on = strip_list(pass_on_cards)
            for divert_cards in stripped_pass_on:
                possible_attack = undefended_attacks.copy()
                for divert_card in divert_cards:
                    possible_attack.append([divert_card, None])
                if len(possible_attack) < len(next_defender.hand):
                    possible_attacks_and_defences.append(possible_attack)

    # Per card see with which cards it can be defended
    defence_cards = []
    for attack in undefended_attacks:
        defence = possible_defends_per_card(hand, attack[0])
        defence_cards.append(defence)

    Nattacks = len(undefended_attacks)
    defences = []

    # Return a list with the combinations of cards to defend with, without duplicates
    if Nattacks == 1:
        defences.extend([[d] for d in defence_cards[0]])
    elif Nattacks == 2:
        defences.extend(cartesian_product2(defence_cards))
    elif Nattacks == 3:
        defences.extend(cartesian_product3(defence_cards))
    elif Nattacks == 4:
        defences.extend(cartesian_product4(defence_cards))
    elif Nattacks == 5:
        defences.extend(cartesian_product5(defence_cards))

    if not any(defences) and not possible_attacks_and_defences:
        return None
    defe = remove_duplicates(defences)

    # Creates the full table again, including the already defended attacks
    for possible_defence in defe:
        possible_attack_and_defence = defended_attacks.copy()
        for i, attack in enumerate(undefended_attacks):
            possible_attack_and_defence.append([attack[0], possible_defence[i]])
        possible_attacks_and_defences.append(possible_attack_and_defence)

    return possible_attacks_and_defences
