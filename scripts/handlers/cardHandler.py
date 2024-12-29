from scripts.config.constants import COLORS, VALUES, SPECIAL_VALUES, SPECIAL_COLOR
from scripts.types.player import Player
from scripts.types.card import Card
deck = []

def initDeck():
    global deck
    deck.clear()
    for color in COLORS:
        for value in VALUES:
            if value in SPECIAL_VALUES:
                color = SPECIAL_COLOR
            deck.append(Card(color, value))
    return deck

def drawCardsToAllPlayers(players: list[Player], amount: int) -> None:
    for player in players:
        player.drawCards(amount, deck)