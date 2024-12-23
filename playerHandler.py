""" TODO: playerHandler should be notified when:
        a) the game is started
        b) a player joins
        c) a player leaves
"""
import network
from player import Player

players = []

def initPlayerList():
    global players
    players.clear()
    
def addPlayer(ip):
    global players
    players.append(Player(ip, 0))

def playerLeft(ip):
    global players
    for player in players:
        if player.id == ip:
            players.remove(player)
            break