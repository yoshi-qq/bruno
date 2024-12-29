from scripts.utils import visuals as visuals
from scripts.utils import menuing
from scripts.handlers import roundHandler 
from scripts.handlers import cardHandler
from scripts.utils import network
from scripts.config.constants import START_CARDS_AMOUNT
from scripts.utils.dependencies import pygame, graphy
from scripts.handlers.communicationHandler import getGameState
from scripts.handlers.playerHandler import getPlayers

running = False
inGame = False

def initGameFunctions():
    pass

def startGameFunctions():
    global inGame, running
    running = True
    while outerLoop():
        pass
    pygame.quit()

def pygameEventHandler():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # ALT+F4/X-Button handling
            game = False
        elif event.type == pygame.KEYDOWN: # Keyboard handling
            print(f"Key {event.key} pressed")
        elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse handling
            graphy.click()


def startGame(): # Starts a game with 2 to 4 players from the hosts machine
    global deck, inGame
    cardHandler.initDeck()
    cardHandler.drawCardsToAllPlayers(getPlayers(), START_CARDS_AMOUNT)
    roundHandler.initGameState(getPlayers(), cardHandler.deck)    
    menuing.setMenu("game")
    inGame = True

def gameLoop():
    if network.me == "host":
        roundHandler.startTurn()
    else:
        visuals.drawFromPerspective(getGameState(), next((player for player in getPlayers() if player.id == network.mainObject.name)))

def outerLoop(): # Runs every frame, returns False on Quit
    global inGame, currentMenu
    pygameEventHandler()
    status = menuing.displayMenu()
    
    if inGame:
        gameLoop()
    elif getGameState() is not None:
        menuing.setMenu("game")
        inGame = True
    
    
    visuals.endFrame()
    return status
