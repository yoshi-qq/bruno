import random
from card import Card
class Player:
    def __init__(self, id: str, cards: list[Card] | int = [], deckToDrawFrom: list[Card] = None):
        self.id = id
        if isinstance(cards, int):
            self.cards = []
            self.drawCards(cards, deckToDrawFrom)
        else:
            self.cards = cards
    
    def drawCards(self, amount: int, stack: list[Card]): # actually draw cards to the players cards (not graphically)
        for i in range(amount):
            card = random.choice(stack)
            self.cards.append(card)
            stack.remove(card)