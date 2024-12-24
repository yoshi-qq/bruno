import random
from collections import deque
from card import Card
class Player:
    def __init__(self, id: str, cards: deque[Card] | int = deque([]), deckToDrawFrom: deque[Card] = None):
        self.id = id
        if isinstance(cards, int):
            self.cards = deque([])
            self.drawCards(cards, deckToDrawFrom)
        else:
            self.cards = cards
    
    def drawCards(self, amount: int, stack: deque[Card]): # actually draw cards to the players cards (not graphically)
        for i in range(amount):
            card = random.choice(stack)
            self.cards.append(card)
            stack.remove(card)