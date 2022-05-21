import pandas as pd
from sklearn.linear_model import LinearRegression
import Cards
import training


def valueFetch(card):
    return Cards.value[card]


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


def spade_ace(cards):
    if '1S' in cards:
        return 1
    else:
        return 0


def heart_ace(cards):
    if '1H' in cards:
        return 1
    else:
        return 0


def diamond_ace(cards):
    if '1D' in cards:
        return 1
    else:
        return 0


def club_ace(cards):
    if '1C' in cards:
        return 1
    else:
        return 0


def spade_king(cards):
    if 'KS' in cards:
        return 1
    else:
        return 0


def heart_king(cards):
    if 'KH' in cards:
        return 1
    else:
        return 0


def diamond_king(cards):
    if 'KD' in cards:
        return 1
    else:
        return 0


def club_king(cards):
    if 'KC' in cards:
        return 1
    else:
        return 0


def bid(card):
    print(card)
    data = training.data
    df = pd.DataFrame(data)
    x = df[['1S', '1H', '1D', '1C', 'KS', 'KH', 'KD', 'KC', 's_len', 'h_len', 'd_len', 'c_len', 's_val']]
    y = df[['bid']]
    model = LinearRegression()
    model.fit(x, y)

    suites = cards_assigner(card)
    data2 = {
        '1S': [spade_ace(card)],
        '1H': [heart_ace(card)],
        '1D': [diamond_ace(card)],
        '1C': [club_ace(card)],
        'KS': [spade_king(card)],
        'KH': [heart_king(card)],
        'KD': [diamond_king(card)],
        'KC': [club_king(card)],
        's_len': [len(suites['S'])],
        'h_len': [len(suites['H'])],
        'd_len': [len(suites['D'])],
        'c_len': [len(suites['C'])],
        's_val': [sum(map(valueFetch, suites['S']))]
    }
    df2 = pd.DataFrame(data2)
    x2 = df2[['1S', '1H', '1D', '1C', 'KS', 'KH', 'KD', 'KC', 's_len', 'h_len', 'd_len', 'c_len', 's_val']]
    predicted_bid = model.predict(x2.take([0]))
    bid_final = round(predicted_bid[0][0])
    return bid_final
