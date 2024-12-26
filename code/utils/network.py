from dependencies import networking
from ..handlers.communicationHandler import initCommunication
from ..handlers import playerHandler

def initNetwork():
    global me
    me = None # TODO: change from string to enum

def getConnByPlayerId(playerId: str):
    return next((client for client in mainObject.clients if client.name == playerId), None)

def addConnection(client):
    playerHandler.addPlayer(client.name)

def removeConnection(client):
    playerHandler.playerLeft(client.name)

def sendClientsUpdate():
    mainObject.sendAll(networking.Message(sender="host", type="updatePlayerList", content=mainObject.clients))

networking.onConnect = addConnection
networking.onDisconnect = removeConnection

def host(ip, port):
    global me, mainObject, menu, players
    me = "host"
    mainObject = networking.Server(host = ip, port = port, dataSize = 2048, encoding = "pickle", maxConnections = 4)

def join(ip, port):
    global me, mainObject, menu
    me = "player"
    mainObject = networking.Client(host = ip, port = port, dataSize = 2048, encoding = "pickle")

def leave():
    global menu
    menu = "main" # TODO: move 1 line to menu logic
    mainObject.close()
