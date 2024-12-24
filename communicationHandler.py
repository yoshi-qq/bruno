import network, visuals, roundHandler
from playerHandler import players
from networking import Message
from varTypes import GameState
from card import Card

gameState = False

# HOST Functions
def playCard(sender: str, content: Card):
    if ((senderPlayer := next((player for player in players if player.id == sender), None)) is not None) and senderPlayer.id == gameState.turn:
        if isinstance(content, Card):
            roundHandler.response = Card
        

# PLAYER Functions
def setGameState(sender: str, content: GameState):
    global gameState
    for event in content.events:
        visuals.displayEvent(event)
        content.resolveEvent(event)
    gameState = content
    if gameState.turn == network.mainObject.name: # check if it's this players turn locally
        pass # TODO: allow card play events now
    else:
        pass # TODO: disallow card play events now

def updatePlayerList(clients):
    network.mainObject.clients = clients


hostFunctions = {
    "playCard": playCard
}

playerFunctions = {
    "updatePlayerList": updatePlayerList,
    "setGameState": setGameState,
}

def initCommunication(me: str):
    match me:
        case "host":
            network.mainObject.messageFunctions.update(hostFunctions)
        case "player":
            network.mainObject.messageFunctions.update(playerFunctions)

def broadcastGameState(gameState: GameState):
    network.mainObject.sendAll(Message(sender="host", type="setGameState", content=gameState))


