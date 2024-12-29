import random
from enum import Enum
from scripts.types.player import Player
from scripts.types.card import Card

class menuOperation(Enum):
    OPEN = 1
    DRAW = 0
    CLOSE = -1

# REQUEST TYPES (to transmit from player to host)
class Request:
    def __init__(self):
        self.author = None
    def addAuthor(self, author):
        self.author = author
        return self

class playCardRequest(Request):
    def __init__(self, playedCard: Card) -> None:
        super().__init__()
        self.playedCard = playedCard

class drawCardRequest(Request):
    def __init__(self) -> None:
        super().__init__()

class shoutBrunoRequest(Request):
    def __init__(self) -> None:
        super().__init__()

class colorChangeRequest(Request):
    def __init__(self, newColor: str) -> None:
        super().__init__()
        self.newColor = newColor

# Response (to transmit from host to player)

# EVENT TYPES
class Event:
    def __init__(self, target: str) -> None:
        self.target = target

class playCardEvent(Event):
    def __init__(self, playerId: str, playedCard: Card) -> None:
        super().__init__(playerId)
        self.playedCard = playedCard

class drawCardsEvent(Event):
    def __init__(self, playerId: str, cardAmount: int) -> None:
        super().__init__(playerId)
        self.cardAmount = cardAmount

class shoutBrunoEvent(Event):
    def __init__(self, playerId: str) -> None:
        super().__init__(playerId)

class colorChangeEvent(Event):
    def __init__(self, playerId: str, newColor: str) -> None:
        super().__init__(playerId)
        self.newColor = newColor

class skipPlayerEvent(Event):
    def __init__(self, playerId: str) -> None:
        super().__init__(playerId)

# Game State (to transmit from host to players)
class GameState:
    def __init__(self, players: list[Player], deck: list[Card], stack: list[Card]):
        self.deck = deck
        self.stack = stack
        self.players: list[Player] = players
        self.turnOrder: list[str] = [player.id for player in self.players ]
        self.turn: str = self.turnOrder[0]
        self.events: list[Event] = []
        self.direction = 1
    
    # RENDERS
    def generateRenders(self, perspectivePlayerName: str | None = None):
        for card in self.deck:
            card.generateRenderObject()
        for card in self.stack:
            card.generateRenderObject()
        for player in self.players:
            for card in player.cards:
                card.generateRenderObject(hoverable = (perspectivePlayerName == player.id or perspectivePlayerName == None))
        return self
    
    def removeRenders(self):
        for card in self.deck:
            card.removeRenderObject()
        for card in self.stack:
            card.removeRenderObject()
        for player in self.players:
            for card in player.cards:
                card.removeRenderObject()
        return self
    
    # TURN
    def setTurn(self, id: str):
        self.turn = id
    
    def getTurn(self) -> str:
        return self.turn
    
    def randomizeTurnOrder(self):
        self.turnOrder = [player.id for player in self.players]
        random.shuffle(self.turnOrder)
        self.turn = self.turnOrder[0]
    
    # DECK
    def setDeck(self, newDeck: list[Card]):
        self.deck = newDeck
    
    def getDeck(self) -> list[Card]:
        return self.deck
    
    def addCardToDeck(self, card: Card):
        self.deck.append(card)
    
    def removeCardFromDeck(self, card: Card):
        self.deck.remove(card)
    
    def drawFromStackToDeck(self, amount: int = 1):
        for i in range(amount):
            self.stack.append(self.deck[0])
            self.deck.pop(0)
    
    # STACK
    def setStack(self, newStack: list[Card]):
        self.stack = newStack
    
    def getStack(self) -> list[Card]:
        return self.stack
    
    def addCardToStack(self, card: Card):
        self.stack.append(card)
    
    def removeCardFromStack(self, card: Card):
        self.stack.remove(card)

    
    # def updatePlayerStatuses(self, players: list[Player]):
    #     for localPlayer in self.players:
    #         for networkPlayer in players:
    #             if localPlayer.id == networkPlayer.id:
    #                 localPlayer.present = True
    #                 localPlayer.cardAmount = len(networkPlayer.cards)
    #                 break
    #         localPlayer.present = False # OLD TODO: add handling for player rejoining

    def changeDirection(self):
        self.direction *= -1
    
    def addEvent(self, event: Event):
        self.events.append(event)
    
    def resolveEvent(self, event: Event):
        self.events.remove(event)
    