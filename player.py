import random
from collections import deque
from gameLogic import deck
class Player:
        def __init__(self, cards = deque([])):
            if isinstance(cards, list):
                self.cards = cards
            elif isinstance(cards, int):
                self.cards = deque([])
                self.drawCards(cards, deck)
        
        def drawCards(self, amount, stack): # actually draw cards to the players cards (not graphically)
            for i in range(amount):
                card = random.choice(stack)
                self.cards.append(card)
                stack.remove(card)