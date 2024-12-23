from collections import deque
from constants import COLORS, VALUES, SPECIAL_VALUES, SPECIAL_COLOR
from card import Card
# from playerHandler import players
# TODO: add playerHandler first
deck = deque([])

def initDeck():
    global deck
    deck.clear()
    for color in COLORS:
        for value in VALUES:
            if value in SPECIAL_VALUES:
                color = SPECIAL_COLOR
            deck.append(Card(color, value)) 

def drawCardsToAllPlayers(amount: int) -> None:
    pass # TODO: uncomment when playerHandler is implemented
    # for player in players:
    #     player.drawCards(amount, deck)