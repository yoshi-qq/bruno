from dependencies import graphy, pygame
from constants import CARD_WIDTH, CARD_HEIGHT, CARD_HOVER_OFFSET
from functools import cache

class Card:
        def __init__(self, color, value, priority = 3, hoverable = False, hoverOffset = CARD_HOVER_OFFSET):
            self.color = color
            self.value = value
            self.renderObject = graphy.RenderButton(surface = graphy.screen, strName = f"card|{color}|{value}", imageName = self.createCardSurface(), priority = priority)
            if hoverable:
                self.renderObject.hoverAction = self.renderObject.offset
                self.renderObject.hoverArguments = (hoverOffset[0], hoverOffset[1], hoverOffset[2], hoverOffset[3])
                self.renderObject.unHoverAction = self.renderObject.offset
                self.renderObject.unHoverArguments = (0, 0, 1, 0)
        
        def generateRenderObject(self, hoverable = False, hoverOffset = CARD_HOVER_OFFSET):
            self.renderObject = graphy.RenderButton(surface = graphy.screen, strName = f"card|{self.color}|{self.value}", imageName = self.createCardSurface(), priority = 3)
            if hoverable:
                self.renderObject.hoverAction = self.renderObject.offset
                self.renderObject.hoverArguments = (hoverOffset[0], hoverOffset[1], hoverOffset[2], hoverOffset[3])
                self.renderObject.unHoverAction = self.renderObject.offset
                self.renderObject.unHoverArguments = (0, 0, 1, 0)

        def removeRenderObject(self):
            del self.renderObject
        
        def drawCorners(self, x, y, size, surface):
            border = 8 * size
            width, height = size * CARD_WIDTH, size * CARD_HEIGHT
            symbolSize = 20*size
            graphy.drawNormal(surface, graphy.sprites[self.value][0], x+border, y+border, symbolSize, symbolSize)
            graphy.drawRotated(surface, graphy.sprites[self.value][0], x+width-symbolSize-border, y+height-symbolSize-border, 180, symbolSize, symbolSize, 1)
        
        def drawMiddle(self, x, y, size, surface):
            width, height = size * CARD_WIDTH, size * CARD_HEIGHT
            symbolSize = 45*size
            if self.value == "plus4":
                graphy.drawNormal(surface, graphy.sprites[self.value + "_big"][0], x+width/2-symbolSize/2, y+height/2-symbolSize/2, symbolSize, symbolSize)
            elif self.value in ("colors", "start", "join", "host", "exit"):
                symbolHeight, symbolWidth = 104*size, 72*size
                graphy.drawNormal(surface, graphy.sprites[self.value + "_big"][0], x+width/2-symbolWidth/2, y+height/2-symbolHeight/2, symbolWidth, symbolHeight)
            else:
                graphy.drawNormal(surface, graphy.sprites[self.value][0], x+width/2-symbolSize/2, y+height/2-symbolSize/2, symbolSize, symbolSize)

        @cache
        def createCardSurface(self, x = 0, y = 0, size = 1):
            w, h = size * CARD_WIDTH, size * CARD_HEIGHT
            subSurface = pygame.Surface((w*graphy.rx, h*graphy.ry), pygame.SRCALPHA)
            graphy.drawNormal(surface = subSurface, img = graphy.sprites[self.color][0], x=x, y=y, width=w, height=h)
            graphy.drawNormal(surface = subSurface, img = graphy.sprites["card_extra"][0], x=x, y=y, width=w, height=h)
            self.drawCorners(x, y, size, subSurface)
            self.drawMiddle(x, y, size, subSurface)
            return subSurface

        def remove(self):
            self.renderObject.remove()
