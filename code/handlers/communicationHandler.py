from code.utils import network as network
from code.utils import visuals
from code.handlers.playerHandler import getPlayers, setPlayers
from code.dependencies.networking import Message
from code.types.varTypes import GameState, Request

gameState = None
requests = []
def getGameState():
    return gameState

# HOST Functions
def requestAction(sender: str, content: Request):
    global requests
    requests.append(content.addAuthor(sender))

# PLAYER Functions
def setGameState(sender: str, content: GameState):
    global gameState
    for event in content.events:
        visuals.displayEvent(event)
        content.resolveEvent(event)
    gameState = content.generateRenders(network.mainObject.name)
    setPlayers(gameState.players)
    if gameState.turn == network.mainObject.name: # check if it's this players turn locally
        pass # TODO: allow card play events now
    else:
        pass # TODO: disallow card play events now

def updatePlayerList(clients):
    network.mainObject.clients = clients

def rejectRequest(sender: str, reason: str):
    print(f"Request rejected: {reason}")


hostFunctions = {
    "requestAction": requestAction,
    "setGameState": setGameState,
}

playerFunctions = {
    "updatePlayerList": updatePlayerList,
    "setGameState": setGameState,
    "rejectRequest": rejectRequest,
}

def initCommunication(me: str):
    match me:
        case "host":
            network.mainObject.messageFunctions.update(hostFunctions)
        case "player":
            network.mainObject.messageFunctions.update(playerFunctions)

def broadcastGameState(gameState: GameState):
    network.mainObject.sendAll(Message(sender="host", type="setGameState", content=gameState.removeRenders()))
    
def sendRejection(playerId: str, reason: str):
    conn = network.getConnByPlayerId(playerId)
    network.mainObject.send(conn, Message(sender="host", type="rejectRequest", content=reason))