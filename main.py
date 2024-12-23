# Imports
from network import initNetwork
from visuals import initVisuals

# Game functions
import gameLogic as g

def main(): # main function
    initNetwork()
    initVisuals()
    g.initGameFunctions()
    g.startGameFunctions()

# Script
if __name__ == '__main__':
    main()