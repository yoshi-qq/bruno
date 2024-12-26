from time import time as now, sleep
from code.types.card import Card
from code.types.player import Player
from code.handlers.playerHandler import getPlayers
from code.types.varTypes import GameState, Request
from code.types import varTypes as v
from code.handlers.communicationHandler import broadcastGameState, gameState, sendRejection
from code.handlers import communicationHandler
from code.config.constants import ACTIONS_PER_TURN, MAX_TURN_LENGTH, PENALTY_CARD_AMOUNT

def initGameState(players: list[Player], deck: list[Card]):
    global gameState
    gameState = GameState(players, deck, [])
    gameState.drawFromStackToDeck()

def startTurn():
    # TODO: add full turn functionality
    currentIndex = gameState.turnOrder.index(gameState.turn)
    newIndex = (currentIndex + gameState.direction) % len(gameState.turnOrder)
    gameState.setTurn(gameState.turnOrder[newIndex])
    communicationHandler.requests = []
    broadcastGameState(gameState)
    # (2. check if special cards are active)
    turnStartTime = now()
    actionsLeft = ACTIONS_PER_TURN
    while now() <= turnStartTime + MAX_TURN_LENGTH and actionsLeft > 0:
        sleep(0.1)
        if communicationHandler.requests != []:
            handleRequests(communicationHandler.requests, gameState.getTurn(), actionsLeft)
    if actionsLeft <= 0:
        timeOutPenalty(next((player for player in getPlayers() if player.id == gameState.turn), None))
    
    # 4. check if the player has 1 card and not pressed the brUNO button
    # 5. check if game is over -> update game state
    # 6. update all player clients over the played card(s), their new cards and other events


def handleRequests(requests: list[Request], currentTurn: str, actionsLeft: int):
    for request in requests:
        handleRequest(request, currentTurn, actionsLeft)

def handleRequest(request: Request, currentTurn: str, actionsLeft: int):
    approved = False
    reason = "No Request"
    match type(request):
        case v.playCardRequest:
            pass
        case v.drawCardRequest:
            pass
        case v.shoutBrunoRequest:
            pass
        case v.colorChangeRequest:
            pass
        case _:
            reason = "Request unknown"
    
    if approved:
        actionsLeft -= 1
    else:
        sendRejection(request.author, reason)

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