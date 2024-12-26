from ..types.player import Player

players: list[Player] = []

def getPlayers() -> list[Player]:
    return players

def setPlayers(newPlayers: list[Player]) -> None:
    global players
    players = newPlayers

def initPlayerList():
    global players
    players.clear()
    
def addPlayer(name):
    global players
    players.append(Player(name, 0))

def playerLeft(name):
    global players
    for player in players:
        if player.id == name:
            players.remove(player)
            break
    