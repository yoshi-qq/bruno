import visuals, menuing, roundHandler, cardHandler, network, communicationHandler
from collections import deque
from card import Card
from player import Player
from constants import START_CARDS_AMOUNT, PENALTY_CARD_AMOUNT
from dependencies import pygame, graphy
from roundHandler import gameState
from playerHandler import players

running = False
inGame = False

def initGameFunctions():
    pass

def startGameFunctions():
    global inGame, running
    running = True
    inGame = False
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
    roundHandler.initGameState(players, cardHandler.deck)
    cardHandler.drawCardsToAllPlayers(players, START_CARDS_AMOUNT)
    inGame = True

def gameLoop():
    if network.me == "host":
        roundHandler.startTurn()
    else:
        visuals.drawFromPerspective(gameState, next((player for player in players if player.id == network.mainObject.name), None))

def outerLoop(): # Runs every frame
    global inGame
    pygameEventHandler()
    menuing.displayMenu()
    
    if inGame:
        gameLoop()
    elif gameState is not None:
        inGame = True
    
    
    visuals.endFrame()
