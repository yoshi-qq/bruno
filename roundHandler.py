from collections import deque
from card import Card
from time import time as now, sleep
from player import Player
from playerHandler import getPlayers
from varTypes import GameState
from communicationHandler import broadcastGameState, gameState
import communicationHandler
from constants import MAX_TURN_LENGTH, PENALTY_CARD_AMOUNT
# TODO: add cardHandler and playerHandler first

def initGameState(players: list[Player], deck: deque[Card]):
    global gameState
    gameState = GameState(players, deck)

def startTurn():
    # TODO: add full turn functionality
    currentIndex = gameState.turnOrder.index(gameState.turn)
    newIndex = (currentIndex + gameState.direction) % len(gameState.turnOrder)
    gameState.setTurn(gameState.turnOrder[newIndex])
    broadcastGameState(gameState)
    # (2. check if special cards are active)
    turnStartTime = now()
    communicationHandler.response = None
    turn_done = False
    while now() <= turnStartTime + MAX_TURN_LENGTH and turn_done == False:
        sleep(0.1)
        if communicationHandler.response is not None:
            playerPlaysCard(gameState.turn, communicationHandler.response)
            turn_done = True
    if turn_done == False:
        timeOutPenalty(next((player for player in getPlayers() if player.id == gameState.turn), None))
    
    # 4. check if the player has 1 card and not pressed the brUNO button
    # 5. check if game is over -> update game state
    # 6. update all player clients over the played card(s), their new cards and other events


def playerPlaysCard(player: Player, card: Card):
    if card in player.cards:
        player.cards.remove(card)
        # TODO: check if card is valid
        # TODO: activate card effects
        # TODO: send card play event to other players

def drawCardsForPlayer(player: Player, amount: int):
    player.drawCards(amount)
    # TODO: add event for card drawing

def timeOutPenalty(player: Player):
    drawCardsForPlayer(player, PENALTY_CARD_AMOUNT)