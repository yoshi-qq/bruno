from dependencies import networking
from collections import deque

def initNetwork():
    global me
    me = None

def sendClientsUpdate():
    mainObject.sendAll(networking.Message(sender="host", type="updatePlayerList", content=mainObject.clients))

networking.onConnect = sendClientsUpdate
networking.onDisconnect = sendClientsUpdate

def host(ip, port):
    global me, mainObject, menu, players
    me = "host"
    mainObject = networking.Server(host = ip, port = port, dataSize = 2048, encoding = "pickle", maxConnections = 4)

def join(ip, port):
    global me, mainObject, menu
    me = "player"
    mainObject = networking.Client(host = ip, port = port, dataSize = 2048, encoding = "pickle")
    mainObject.messageFunctions["updatePlayerList"] = updatePlayerList

def leave():
    global menu
    menu = "main" # TODO: move 1 line to menu logic
    mainObject.close()

def updatePlayerList(clients):
    mainObject.clients = clients