import visuals, menuing
from collections import deque
from card import Card
from constants import COLORS, VALUES, SPECIAL_VALUES, SPECIAL_COLOR
from dependencies import pygame, graphy

def initGameFunctions():
    global deck
    deck = createDeck()
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
    pass # TODO: make game playable

def gameLoop():
    visuals.drawStack(deck)

def outerLoop(inGame): # Runs every frame
    pygameEventHandler()
    menuing.displayMenu()
    
    if inGame:
        gameLoop()
    
    visuals.endFrame()


def createDeck():
    newDeck = deque([])
    for color in COLORS:
        for value in VALUES:
            if value in SPECIAL_VALUES:
                color = SPECIAL_COLOR
            newDeck.append(Card(color, value)) 
    return newDeck