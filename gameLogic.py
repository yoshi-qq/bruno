import visuals, menuing, roundHandler, cardHandler
from collections import deque
from card import Card
from constants import START_CARDS_AMOUNT
from dependencies import pygame, graphy

def initGameFunctions():
    me = None

def startGameFunctions():
        running = True
        inGame = False
        while running:
            outerLoop(inGame)
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
    cardHandler.createDeck()
    cardHandler.drawCardsToAllPlayers(START_CARDS_AMOUNT)
    inGame = True

def gameLoop():
    visuals.drawStack(deck)
    visuals.drawHands()
    roundHandler.startRound()

def outerLoop(inGame): # Runs every frame
    pygameEventHandler()
    menuing.displayMenu()
    
    if inGame:
        gameLoop()
    
    visuals.endFrame()