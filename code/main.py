""" TODO: 
    1. refactor folder structure for better overview
    2. look for the other Fixmes & Todos in different files
    3. add rest of communication as shown in communication.drawio.png
    4. plan next features needed to continue
"""
# Imports
from code.utils.network import initNetwork
from code.utils.visuals import initVisuals

# Game functions
import code.utils.gameLogic as g

def init():
    initNetwork()
    initVisuals()
    g.initGameFunctions()

def start(): # main function
    g.startGameFunctions()

def main():
    init()
    start()