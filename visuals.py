from dependencies import graphy, pygame
from constants import ROOT, CARD_BACK_ASSET, CARD_BASE_WIDTH, HAND_BASE_HARD_WIDTH, HAND_BASE_SOFT_WIDTH, OWN_HAND_POSITION, OWN_HAND_SIZE, OTHER_HANDS_POSITIONS, OTHER_HANDS_SIZES
from varTypes import event, GameState
from card import Card
from player import Player
from playerHandler import getPlayers
import os
def initVisuals():
    global font
    graphy.init(file = __file__, fps = 60, fontPath = os.path.join(ROOT, "font\\unifont.otf"),fullscreen = False, singleSizeOn = True, windowName = "brUNO", spriteFolder = "assets", windowIcon = "cardback")
    graphy.postDraw = drawFPS
    font = pygame.font.Font(ROOT + "/font/fixed_sys.ttf", 30)
    
def drawStack(deck):
    for i in range(len(deck)):
        graphy.RenderImage(priority = 2.5, strName = f"deckCard{i}", imageName = "cardback", x = graphy.middle[0] - 50, y = graphy.middle[1]- i/1.2, width = 82*1.5, height = 128*1.5, middle = True, temporary = True)

def drawOpen(cards, size = 1):
    i = 0
    for card in cards:
        columns = 15
        row = i // columns
        column = i - row*columns
        graphy.RenderImage(strName = f"deckCard{i}", imageName = card.renderObject, temporary = True, enabled = True, x = column*90*size, y = row*140*size, width = 82*size, height = 128*size)
        i+=1

def drawHands(players: list[Player]):
    # TODO: add functionality (recommended to finish playerHandler and cardHandler first)
    for i, player in enumerate(players):
        drawHand(player.cards, False, OTHER_HANDS_POSITIONS[i][0], OTHER_HANDS_POSITIONS[i][1], OTHER_HANDS_SIZES[i])

def drawOwnHand(cards: list[Card]):
    drawHand(cards, True, OWN_HAND_POSITION[0], OWN_HAND_POSITION[1], OWN_HAND_SIZE)

def drawHand(cards: list[Card], show, x, y, size = 1):
    width = CARD_BASE_WIDTH * size
    hardWidth = HAND_BASE_HARD_WIDTH
    softWidth = len(cards) * HAND_BASE_SOFT_WIDTH
    if softWidth > 1:
        softWidth = 1
    width = width*hardWidth + width*(1-hardWidth)*softWidth
    i = 1
    for card in cards:
        card.renderObject.angle = 0.1+((i-0.5)/len(cards)-0.5) * 2 * 20
        card.renderObject.x = x - width/2 + (i-0.5)/len(cards) * width
        card.renderObject.y = y + (abs((i-0.5)/len(cards)-0.5)*10)**2.25
        subSize = size
        card.renderObject.width = subSize*82
        card.renderObject.height = subSize*128
        card.renderObject.enabled = True
        card.renderObject.priority = 3.9 - i/(len(cards))
        if show:
            card.renderObject.image = card.createCardSurface()
            card.renderObject.update()
        else:
            card.renderObject.image = graphy.sprites[CARD_BACK_ASSET][0]
            card.renderObject.update()
        i += 1
        
def drawFPS():
    fpsText = font.render(f"FPS: {graphy.clock.get_fps():.0f}", True, pygame.Color('black'))
    graphy.screen.blit(fpsText, (0, 0))
    
def endFrame():
    graphy.draw()

def displayEvent(event: event):
    # TODO: display event animations
    pass

def drawFromPerspective(gameState: GameState, player: Player):
     # TODO: add full drawing of everything
    drawStack(gameState.deck)
    drawOwnHand(player.cards)
    drawHands([playerX for playerX in getPlayers() if playerX != player])