import visuals, menuing, roundHandler, cardHandler, network
from constants import START_CARDS_AMOUNT
from dependencies import pygame, graphy
from communicationHandler import getGameState
from playerHandler import getPlayers

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
