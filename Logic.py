import Cards
from dataset1 import bid
import time

start = time.time()


def spades_checker(cards):
    for a in cards:
        if a[-1] == 'S':
            return False
    return True


def get_plays(sign, played):
    a = []
    for i in played:
        if i[-1] == sign:
            a.append(i)
    return a


neg_factor = 1


def bid_calculator(cards):
    bid_final = int(bid(cards))
    if bid_final < 1:
        bid_final = 1
    if bid_final > 8:
        bid_final = 8
    return bid_final


def cards_assigner(cards):
    """
    This function assigns cards of different suits to different lists and adds them to a dictionary.
    """

    # Sort the cards in ascending order
    # and return the sorted list
    dictionary = {'C': [],
                  'D': [],
                  'H': [],
                  'S': []}
    for card in cards:
        dictionary[card[-1]].append(card)
    for suit in dictionary:
        dictionary[suit].sort(key=lambda x: Cards.value[x], reverse=True)
    return dictionary


def card_sort(cards):
    """
    This function sorts the cards in descending order.
    """
    ret = cards_assigner(cards)
    clubs = ret['C']
    spades = ret['S']
    diamonds = ret['D']
    hearts = ret['H']
    list2 = []

    c = str(len(clubs)) + 'C'
    h = str(len(hearts)) + 'H'
    d = str(len(diamonds)) + 'D'
    dictionary = {
        c: clubs,
        h: hearts,
        d: diamonds,
    }
    list1 = [c, h, d]
    list1.sort(reverse=True)
    for i in list1:
        list2 = list2 + dictionary[i]
    return spades + list2


def get_cards(card_name):
    """
    This function returns suitable name of player's cards. Like, it takes '1S/0' and returns '1S'.
    """
    return card_name[0:2]


def logic(played, cards, history):
    # This is the main logic of the game.
    play = ''  # This is the variable for final card that we're returning
    same = 0  # Just to track sth
    if len(played) > 0:
        sign_of_the_card = played[0][1]
    else:
        sign_of_the_card = ''
    total_cards = cards_assigner(cards)
    spades = total_cards['S']
    clubs = total_cards['C']
    diamonds = total_cards['D']
    hearts = total_cards['H']
    playable = []
    overall_history = []
    cards_arranged = card_sort(cards)
    for dash in history:
        overall_history += dash[1]
    overall_history = list(map(get_cards, overall_history))
    # When no players have played before you, i.e. your turn is in the first throw of any round.
    played_cards = list(map(get_cards, played))  # Gets proper list of played card
    play_sorted = card_sort(played_cards)  # Sorts played cards
    total_played = card_sort(
        list(map(get_cards,
                 overall_history)) + played_cards)  # Gets overall history of cards that have been played
    sign_match = get_plays(sign_of_the_card,
                           play_sorted)  # Gets the list of played cards that have the same sign as the played card
    sign_match = card_sort(sign_match)  # Sorts the sign_match list
    remains = card_sort([z for z in Cards.cards if
                         z not in total_played])  # Gets the list of cards that have not been played yet
    able = remains + play_sorted
    sign_remains = cards_assigner(
        remains)  # Gets a dictionary of the cards that have not been played yet with their respective signs
    sign_history = cards_assigner(total_played)
    sign_playable = cards_assigner(able)
    if played == []:
        # When it's the first round
        if history == []:
            playable = [card for card in cards_arranged if '1' in card]
            if playable:
                play = playable[-1]
            else:
                if '1S' in cards and 'KS' in cards and 'QS' in cards:  # If we have 'KS', 'QS' and '1S', it plays '1S' at the very beginning of the game so that we can make other player throw their spades
                    play = '1S'
                elif '1C' in cards or '1D' in cards or '1H' in cards:
                    play = [x for x in cards if '1' in x][
                        0]  # If we have '1C', '1D' or '1H', it plays '1C' or '1D' or '1H' at the very beginning of the game.
                else:
                    play = card_sort(cards)[-1]  # Otherwise, it plays the lowest possible card
        # When it's not the first round
        elif history != []:
            applicable = [b for b in card_sort(cards) if b in clubs or b in diamonds or b in hearts]
            playable = [z for z in cards_arranged if Cards.value[z] >= Cards.value[sign_remains[z[-1]][0]]]
            if len(playable) > 0:
                play = playable[-1]
            else:
                try:
                    playable = [applicable[0], applicable[-1]]
                except:
                    playable = spades
                if Cards.value[playable[0]] > Cards.value[sign_remains[playable[0][-1]][0]] and len(
                        sign_remains[playable[0][-1]]) > 6:
                    play = playable[0]
                else:
                    play = playable[-1]

    # When other players have played before you
    elif played != []:
        sign_of_the_card = played_cards[0][1]  # Gets the sign of the card that has been played
        # Gets the list of remaining cards that have the same sign as the played card
        # When it's the first round
        for c in cards:
            if c[1] == sign_of_the_card:
                playable.append(c)  # Gets the list of cards that we have that have the same sign as the played card
        if history == []:
            if len(playable) < 1:  # If we no longer have cards with same sign,
                if spades != []:  # And if we have spades,
                    if len(cards_assigner(play_sorted)['S']) < 1:
                        playable = [spades[-1]]  # Spade of the lowest value is played
                    else:
                        for i in spades:
                            if Cards.value[i] > Cards.value[play_sorted[0]]:
                                playable = [i]
                else:
                    playable = list(i for i in cards if
                                    Cards.value[i] <= 5)  # If we don't have spades, we play cards of value 5 or less
                    if playable == []:
                        playable = [cards_arranged[
                                        -1]]  # If we don't have cards of value 5 or less, we play the lowest card that we have
                same = 1
            if same != 1:
                playable = card_sort(playable)  # If we have cards with same sign, we sort them
                if Cards.value[playable[0]] >= Cards.value[sign_playable[sign_of_the_card][0]] and len(
                        sign_remains[sign_of_the_card]) > 6 and sign_of_the_card != 'S':
                    play = playable[0]
                else:
                    for i in playable:
                        if Cards.value[i] > Cards.value[sign_match[0]]:
                            # And play the card with exactly higher value than already played card with the highest value
                            play = i
                    if play == '':
                        play = playable[-1]
            else:
                play = playable[
                    -1]  # If we do not have cards with same sign, we play the lowest spade card or lowest other card
            if play == '':
                # If we don't have higher cards with same sign, we play the last card of the list, i.e. the lowest value card of same sign
                play = cards_arranged[-1]

        elif history != []:
            if len(playable) < 1:  # If we no longer have cards with same sign,
                if spades != []:  # And if we have spades,
                    if len(cards_assigner(play_sorted)['S']) < 1:
                        playable = [spades[-1]]  # Spade of the lowest value is played
                    else:
                        for i in spades:
                            if Cards.value[i] > Cards.value[play_sorted[0]]:
                                playable = [i]
                            if playable == []:
                                playable = spades  # If we don't have spades, we play cards of value 5 or less
                else:
                    playable = list(i for i in cards if
                                    Cards.value[i] <= 5)  # If we don't have spades, we play cards of value 5 or less
                    if playable == []:
                        playable = [cards_arranged[
                                        -1]]  # If we don't have cards of value 5 or less, we play the lowest card that we have
                same = 1
            if same != 1:
                playable = card_sort(playable)  # If we have cards with same sign, we sort them
                if Cards.value[playable[0]] > Cards.value[sign_playable[sign_of_the_card][0]] and spades_checker(
                        played) or Cards.value[
                    playable[0]] >= Cards.value[sign_playable[sign_of_the_card][0]] and spades_checker(played):
                    play = playable[0]
                else:

                    for i in playable:
                        if Cards.value[i] > Cards.value[sign_match[0]]:
                            # And play the card with exactly higher value than already played card with the highest value
                            play = i
                    if play == '':
                        play = playable[-1]
            else:
                play = playable[
                    -1]  # If we do not have cards with same sign, we play the lowest spade card or lowest other card
            if play == '':
                # If we don't have higher cards with same sign, we play the last card of the list, i.e. the lowest value card of same sign
                play = cards_arranged[-1]

    ######################################################################################
    return int(cards.index(play))
