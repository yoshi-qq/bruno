import random
from enum import Enum
from collections import deque
from player import Player
from card import Card

class menuOperation(Enum):
    OPEN = 1
    DRAW = 0
    CLOSE = -1

class event:
    pass

class GameState:
    def __init__(self, players: list[Player], deck: deque[Card]):
        self.deck = deck
        self.players: list[Player] = players
        self.turnOrder: list[str] = [player.id for player in self.players ]
        self.turn: str = self.turnOrder[0]
        self.events: list[event] = []
        self.direction = 1
    
    def setTurn(self, id: str):
        self.turn = id
    
    def setDeck(self, deck: deque[Card]):
        self.deck = deck
    
    def randomizeTurnOrder(self):
        self.turnOrder = [player.id for player in self.players]
        random.shuffle(self.turnOrder)
        self.turn = self.turnOrder[0]
    
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
    
    def addEvent(self, event: event):
        self.events.append(event)
    
    def resolveEvent(self, event: event):
        self.events.remove(event)
    