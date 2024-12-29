from scripts.utils.dependencies import graphy, pygame
from scripts.config.constants import ROOT, FONT, FONT2, IMAGE_SPRITES, CARD_WIDTH, CARD_HEIGHT, CARD_BACK_ASSET, CARD_BASE_WIDTH, HAND_BASE_HARD_WIDTH, HAND_BASE_SOFT_WIDTH, OWN_HAND_POSITION, OWN_HAND_SIZE, OWN_HAND_ANGLE, OWN_HAND_CARD_SPACING, OTHER_HANDS_POSITIONS, OTHER_HANDS_SIZES, OTHER_HANDS_ANGLES, OTHER_HANDS_CARD_SPACING, STACK_SIZES, STACK_ANGLES, STACK_POSITIONS, STACK_CARD_DISTANCES
from scripts.types.varTypes import Event, GameState
from scripts.types.card import Card
from scripts.types.player import Player
from scripts.handlers.playerHandler import getPlayers
import os, math
def initVisuals():
    global font
    graphy.init(file = __file__, fps = 60, fontPath = FONT2, fullscreen = False, singleSizeOn = True, windowName = "brUNO", spriteFolder = os.path.join(ROOT, IMAGE_SPRITES), windowIcon = "cardback")
    graphy.postDraw = drawFPS
    font = pygame.font.Font(FONT, 30)
    
def drawDrawPile(deck: list[Card]):
    drawCardStack(deck, False, 0)

def drawDiscardPile(stack: list[Card]):
    drawCardStack(stack, True, 1)

def drawCardStack(stack: list[Card], show: bool = False, stackNum: int = 0):
    # TODO: shadows (advanced, not necessary)
    position = STACK_POSITIONS[stackNum]
    angle = STACK_ANGLES[stackNum]
    size = STACK_SIZES[stackNum]
    distance = STACK_CARD_DISTANCES[stackNum]
    
    for i, card in enumerate(stack):
        card.renderObject.angle = angle
        card.renderObject.x = position[0] + i*distance[0]
        card.renderObject.y = position[1] + i*distance[1]
        card.renderObject.width = size * CARD_WIDTH
        card.renderObject.height = size * CARD_HEIGHT
        card.renderObject.enabled = True
        card.renderObject.priority = 2 + i / len(stack)
        
        if show:
            card.renderObject.image = card.createCardSurface()
        else:
            card.renderObject.image = graphy.sprites[CARD_BACK_ASSET][0]    
    
def drawOpen(cards, size = 1):
    i = 0
    for card in cards:
        columns = 15
        row = i // columns
        column = i - row*columns
        graphy.RenderImage(strName = f"deckCard{i}", imageName = card.renderObject, temporary = True, enabled = True, x = column*90*size, y = row*140*size, width = CARD_WIDTH*size, height = CARD_HEIGHT*size)
        i+=1

def drawHands(players: list[Player]):
    # TODO: add functionality (recommended to finish playerHandler and cardHandler first)
    for i, player in enumerate(players):
        drawHand(player.cards, False, OTHER_HANDS_POSITIONS[i][0], OTHER_HANDS_POSITIONS[i][1], OTHER_HANDS_SIZES[i], OTHER_HANDS_ANGLES[i], OTHER_HANDS_CARD_SPACING)

def drawOwnHand(cards: list[Card]):
    drawHand(cards, True, OWN_HAND_POSITION[0], OWN_HAND_POSITION[1], OWN_HAND_SIZE, OWN_HAND_ANGLE, OWN_HAND_CARD_SPACING)

def drawHand(cards, show, x, y, size=1, angle=0, spacing=1):
    angle_rad = math.radians(angle)
    
    width = CARD_BASE_WIDTH * size
    hardWidth = HAND_BASE_HARD_WIDTH
    softWidth = len(cards) * HAND_BASE_SOFT_WIDTH
    if softWidth > 1:
        softWidth = 1
    width = width * hardWidth + width * (1 - hardWidth) * softWidth

    # Apply spacing adjustment
    width *= spacing  # Increase or decrease distance between cards

    i = 1
    for card in cards:
        card_angle = 0.1 + ((i - 0.5) / len(cards) - 0.5) * 2 * 20
        base_x = x - width / 2 + (i - 0.5) / len(cards) * width
        base_y = y + (abs((i - 0.5) / len(cards) - 0.5) * 10) ** 2.25
        
        rotated_x = x + (base_x - x) * math.cos(angle_rad) - (base_y - y) * math.sin(angle_rad)
        rotated_y = y + (base_x - x) * math.sin(angle_rad) + (base_y - y) * math.cos(angle_rad)
        
        card.renderObject.angle = card_angle + angle
        card.renderObject.x = rotated_x
        card.renderObject.y = rotated_y
        card.renderObject.width = size * CARD_WIDTH  # Keep size constant
        card.renderObject.height = size * CARD_HEIGHT  # Keep size constant
        card.renderObject.enabled = True
        card.renderObject.priority = 3.9 - i / len(cards)
        
        if show:
            card.renderObject.image = card.createCardSurface()
        else:
            card.renderObject.image = graphy.sprites[CARD_BACK_ASSET][0]

        card.renderObject.update()
        
        i += 1

def drawFPS():
    fpsText = font.render(f"FPS: {graphy.clock.get_fps():.0f}", True, pygame.Color('black'))
    graphy.screen.blit(fpsText, (0, 0))
    
def endFrame():
    graphy.draw()

def displayEvent(event: Event):
    # TODO: display event animations
    pass

def drawFromPerspective(gameState: GameState, player: Player):
     # TODO: add full drawing of everything
    drawDrawPile(gameState.deck)
    drawDiscardPile(gameState.stack)
    drawOwnHand(player.cards)
    drawHands([playerX for playerX in getPlayers() if playerX != player])