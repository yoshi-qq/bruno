from code.utils import visuals as visuals
from code.utils import menuing
from code.handlers import roundHandler 
from code.handlers import cardHandler
from code.utils import network
from code.config.constants import START_CARDS_AMOUNT
from code.utils.dependencies import pygame, graphy
from code.handlers.communicationHandler import getGameState
from code.handlers.playerHandler import getPlayers

running = False
inGame = False

def initGameFunctions():
    pass

def startGameFunctions():
    global inGame, running
    running = True
    while running:
        outerLoop()
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
    inGame = True

def gameLoop():
    if network.me == "host":
        roundHandler.startTurn()
    else:
        visuals.drawFromPerspective(getGameState(), next((player for player in getPlayers() if player.id == network.mainObject.name)))

def outerLoop(): # Runs every frame
    global inGame, currentMenu
    pygameEventHandler()
    menuing.displayMenu()
    
    if inGame:
        gameLoop()
    elif getGameState() is not None:
        currentMenu = "game"
        inGame = True
    
    
    visuals.endFrame()
