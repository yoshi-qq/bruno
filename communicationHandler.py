import network, visuals
from playerHandler import getPlayers, setPlayers
from networking import Message
from varTypes import GameState
from card import Card

gameState = None
response = None

def getGameState():
    return gameState

# HOST Functions
def playCard(sender: str, content: Card):
    global response
    if ((senderPlayer := next((player for player in getPlayers() if player.id == sender), None)) is not None) and senderPlayer.id == gameState.turn:
        if isinstance(content, Card):
            response = Card
        

# PLAYER Functions
def setGameState(sender: str, content: GameState):
    global gameState
    for event in content.events:
        visuals.displayEvent(event)
        content.resolveEvent(event)
    gameState = content.generateRenders()
    setPlayers(gameState.players)
    if gameState.turn == network.mainObject.name: # check if it's this players turn locally
        pass # TODO: allow card play events now
    else:
        pass # TODO: disallow card play events now

def updatePlayerList(clients):
    network.mainObject.clients = clients


hostFunctions = {
    "playCard": playCard,
    "setGameState": setGameState,
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
    network.mainObject.sendAll(Message(sender="host", type="setGameState", content=gameState.removeRenders()))