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


def bid(card):
    deck = Cards.cards
    data = training.data
    df = pd.DataFrame(data)
    x = df[[
        '1H', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH',
        '1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS',
        '1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC',
        '1D', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 's_len', 'h_len', 'd_len',
        'c_len', 's_val'
    ]]
    y = df[['bid']]
    model = LinearRegression()
    model.fit(x, y)
    suites = cards_assigner(card)
    data2 = dictionary = {
        '1H': [], '2H': [], '3H': [], '4H': [], '5H': [], '6H': [], '7H': [], '8H': [], '9H': [], 'TH': [], 'JH': [],
        'QH': [], 'KH': [],
        '1S': [], '2S': [], '3S': [], '4S': [], '5S': [], '6S': [], '7S': [], '8S': [], '9S': [], 'TS': [], 'JS': [],
        'QS': [], 'KS': [],
        '1D': [], '2D': [], '3D': [], '4D': [], '5D': [], '6D': [], '7D': [], '8D': [], '9D': [], 'TD': [], 'JD': [],
        'QD': [], 'KD': [],
        '1C': [], '2C': [], '3C': [], '4C': [], '5C': [], '6C': [], '7C': [], '8C': [], '9C': [], 'TC': [], 'JC': [],
        'QC': [], 'KC': [], 's_len': [], 'h_len': [], 'd_len': [], 'c_len': [], 's_val': []

    }
    for xard in Cards.cards:
        dictionary[xard].append(1 if xard in card else 0)
    data2['s_len'].append(len(suites['S']))
    data2['h_len'].append(len(suites['H']))
    data2['d_len'].append(len(suites['D']))
    data2['c_len'].append(len(suites['C']))
    data2['s_val'].append(sum(map(valueFetch, suites['S'])))
    df2 = pd.DataFrame(data2)
    x2 = df2[[
        '1H', '2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH',
        '1S', '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS',
        '1C', '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC',
        '1D', '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 's_len', 'h_len', 'd_len',
        'c_len', 's_val'
    ]]
    predicted_bid = model.predict(x2.take([0]))
    bid_final = round(predicted_bid[0][0])
    return bid_final
