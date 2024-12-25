# Imports
from network import initNetwork
from visuals import initVisuals

# Game functions
import gameLogic as g

def init():
    initNetwork()
    initVisuals()
    g.initGameFunctions()

def start(): # main function
    g.startGameFunctions()

# Script
if __name__ == '__main__':
    init()
    start()