## Imports
import os, sys, random, importlib.util, subprocess, time, socket, cProfile, pstats
from collections import deque
from functools import cache

root = os.path.dirname(os.path.abspath(__file__))
importType = "local"

#import custom modules
if importType == "global":
    path = os.path.join(os.path.dirname(root), "graphics\\graphy.py")
    spec = importlib.util.spec_from_file_location("graphy", path)
    graphy = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(graphy)
    path = os.path.join(os.path.dirname(root), "network\\networking.py")
    spec = importlib.util.spec_from_file_location("networking", path)
    networking = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(networking)
elif importType == "local":
    import graphy
    import networking
else:
    raise Exception("Invalid import type")


def install(package): #install libraries
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# load Pypi libraries
try:
    import pygame
    from pygame.locals import FULLSCREEN, DOUBLEBUF
except:
    install("pygame")
    import pygame
    from pygame.locals import FULLSCREEN, DOUBLEBUF


## Top Level Functions

def functions(): # creates all non top level functions
    global sendClientsUpdate, drawLobby, drawOpen, drawHand, host, join, leave, startGame, drawFPS, drawStack

    def sendClientsUpdate():
        mainObject.sendAll(networking.Message(sender="host", type="updatePlayerList", content=mainObject.clients))
    
    networking.onConnect = sendClientsUpdate
    networking.onDisconnect = sendClientsUpdate
    
    def host(ip, port):
        global me, mainObject, menu, players
        me = "host"
        mainObject = networking.Server(host = ip, port = port, dataSize = 2048, encoding = "pickle", maxConnections = 4)
        players = deque([])
        menu = "lobby"

    def join(ip, port):
        global me, mainObject, menu
        me = "player"
        mainObject = networking.Client(host = ip, port = port, dataSize = 2048, encoding = "pickle")
        mainObject.messageFunctions["updatePlayerList"] = updatePlayerList
        menu = "lobby"

    def leave():
        global menu
        menu = "main"
        mainObject.close()

    def updatePlayerList(clients):
        mainObject.clients = clients
    
    def startGame():
        global menu
        menu = "game"
        
    
    def drawLobby(me):
        global lobbybuttons
        lobbybuttons.append(myIP := graphy.RenderText(surface = graphy.screen, x = graphy.middle[0], y = 50, middle = True, text = f"IP: {socket.gethostbyname(socket.gethostname())} | Port: {mainObject.port}", size = 50))
        lobbybuttons.append(leaveButton := graphy.RenderTextButton(text = "Leave", clickAction = leave, color = (230, 20, 0), activeColor = (90, 10, 0),  x = graphy.middle[0]-225, y = graphy.middle[1]*1.75, height=80, width = 250, middle = True))
        
        if me == "host":
            lobbybuttons.append(startButton := graphy.RenderTextButton(text = "Start",clickAction = startGame, color = (0,230,20), activeColor = (0,90,10), x = graphy.middle[0]+225, y = graphy.middle[1]*1.75, height=80, width = 250, middle = True))
            
        elif me == "player":
            pass
        
            
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

    def drawHand(cards, show, x, y, size = 1):
        width = 300 * size
        hardWidth = 1/4
        softWidth = len(cards)/6
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
                card.renderObject.image = graphy.assets["cardback"]
                card.renderObject.update()
            i += 1
            
    def drawFPS():
        fpsText = font.render(f"FPS: {graphy.clock.get_fps():.0f}", True, pygame.Color('black'))
        graphy.screen.blit(fpsText, (0, 0))

def classes(): # creates all classes
    global Card, Player

    class Card():
        def __init__(self, color, value, priority = 3, hoverable = False, hoverOffset = (5, -25, 1.2, 1)):
            self.color = color
            self.value = value
            self.renderObject = graphy.RenderButton(surface = graphy.screen, strName = f"card|{color}|{value}", imageName = self.createCardSurface(), priority = priority)
            if hoverable:
                self.renderObject.hoverAction = self.renderObject.offset
                self.renderObject.hoverArguments = (hoverOffset[0], hoverOffset[1], hoverOffset[2], hoverOffset[3])
                self.renderObject.unHoverAction = self.renderObject.offset
                self.renderObject.unHoverArguments = (0, 0, 1, 0)
            
        def drawCorners(self, x, y, size, surface):
            border = 8 * size
            width, height = size * 82, size * 128
            symbolSize = 20*size
            graphy.drawNormal(surface, graphy.sprites[self.value][0], x+border, y+border, symbolSize, symbolSize)
            graphy.drawRotated(surface, graphy.sprites[self.value][0], x+width-symbolSize-border, y+height-symbolSize-border, 180, symbolSize, symbolSize, 1)
        
        def drawMiddle(self, x, y, size, surface):
            width, height = size * 82, size * 128
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
            w, h = size * 82, size * 128
            subSurface = pygame.Surface((w*graphy.rx, h*graphy.ry), pygame.SRCALPHA)
            graphy.drawNormal(surface = subSurface, img = graphy.sprites[self.color][0], x=x, y=y, width=w, height=h)
            graphy.drawNormal(surface = subSurface, img = graphy.sprites["card_extra"][0], x=x, y=y, width=w, height=h)
            self.drawCorners(x, y, size, subSurface)
            self.drawMiddle(x, y, size, subSurface)
            return subSurface

        def remove(self):
            self.renderObject.remove()
        
    class Player():
        def __init__(self, cards = deque([])):
            if isinstance(cards, list):
                self.cards = cards
            elif isinstance(cards, int):
                self.cards = deque([])
                self.drawCards(cards, deck)
        
        def drawCards(self, amount, stack): # actually draw cards to the players cards (not graphically)
            for i in range(amount):
                card = random.choice(stack)
                self.cards.append(card)
                stack.remove(card)

def preload(): # loads variables before starting the script
    global rgbColors, colors, values, deck
    rgbColors = [(237, 28, 36), (80, 170, 68), (0, 114, 188), (255, 222, 22)]
    colors = ["red", "green", "blue", "yellow"]
    values = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "switch", "skip", "plus2", "colors", "plus4"]
    specialValues = ["colors", "plus4"]
    deck = deque([])
    for color in colors:
        for value in values:
            if value in specialValues:
                color = "black"
            deck.append(Card(color, value)) 

def profile(function):
    profiler = cProfile.Profile()
    profiler.enable()

    function()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats()

def main(): # main function
    graphy.init(file = __file__, fps = 60, fontPath = os.path.join(root, "font\\unifont.otf"),fullscreen = True, singleSizeOn = True, windowName = "brUNO", spriteFolder = "assets", windowIcon = "cardback")
    classes()
    functions()
    preload()
    
    global me, menu, font, lobbybuttons, deck
    me = None
    game = True
    lastMenu = "none"
    menu = "main"
    font = pygame.font.Font(root + "/font/fixed_sys.ttf", 30)
    graphy.postDraw = drawFPS
    while game:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # ALT+F4/X-Button handling
                game = False
            elif event.type == pygame.KEYDOWN: # Keyboard handling
                print(f"Key {event.key} pressed")
            elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse handling
                graphy.click()
            
        if menu == "main":
            if lastMenu != menu:
                if lastMenu == "lobby":
                    for lobbybutton in lobbybuttons:
                        lobbybutton.remove()
                    buttons = deque([])
                lastMenu = menu
                buttons = [
                    # Card("blue", "settings", hoverable = True),
                    Card("red", "host", hoverable = True),
                    Card("green", "join", hoverable = True),
                    Card("blue", "settings", hoverable = True),
                    Card("black", "exit", hoverable = True),
                ] 
                buttons[0].renderObject.clickAction = host
                buttons[0].renderObject.arguments = ('localhost', 54322)
                buttons[1].renderObject.clickAction = join
                buttons[1].renderObject.arguments = ('localhost', 54322)
                buttons[3].renderObject.clickAction = sys.exit
                drawHand(buttons, True, 960-150, 600, 3)

        elif menu == "lobby":
            if lastMenu != menu:
                if lastMenu == "main":
                    for button in buttons:
                        button.remove()
                    buttons = deque([])
                    lobbybuttons = deque([])
                    drawLobby(me)
            lastMenu = menu
            if me == "host":
                # TODO: send message to all clients if client list changes
                # TODO: make clients display client list too
                for i, client in enumerate(mainObject.clients):
                    ip, port = client.conn.getpeername()
                    
                    lobbybuttons.append(banner := graphy.RenderTextButton(x = graphy.middle[0], color = rgbColors[i], borderColor = (0, 0, 0), textColor = (0, 0, 0), y = 200 + i * 150, width = 800, height = 80, middle = True, text = f"{ip}:{port}", temporary = True))
                    lobbybuttons.append(playerNumbers := graphy.RenderTextButton(drawType = "circ", x = banner.x - banner.width//(3/2) - 100, y = banner.y, text = str(i+1), color = rgbColors[i], borderColor = (0, 0, 0), textColor = (0, 0, 0), width = banner.height*1.2, height = banner.height*1.2, middle = True, temporary = True))
        
            else:
                if hasattr(mainObject, 'clients'):
                    for i, client in enumerate(mainObject.clients):
                        ip, port = client.conn.getpeername()

                        lobbybuttons.append(banner := graphy.RenderTextButton(x = graphy.middle[0], color = rgbColors[i], borderColor = (0, 0, 0), textColor = (0, 0, 0), y = 200 + i * 150, width = 800, height = 80, middle = True, text = f"{ip}:{port}", temporary = True))
                        lobbybuttons.append(playerNumbers := graphy.RenderTextButton(drawType = "circ", x = banner.x - banner.width//(3/2) - 100, y = banner.y, text = str(i+1), color = rgbColors[i], borderColor = (0, 0, 0), textColor = (0, 0, 0), width = banner.height*1.2, height = banner.height*1.2, middle = True, temporary = True))
            
        elif menu == "game":
            if lastMenu != menu:
                if lastMenu == "lobby":
                    for lobbybutton in lobbybuttons:
                        lobbybutton.remove()
                    buttons = deque([])
                
                background = graphy.RenderImage(imageName = "background", width=graphy.nativeResolution[0], height=graphy.nativeResolution[1])
                
            lastMenu = menu
            drawStack(deck)
            
        graphy.draw()
    pygame.quit()


## Script
if __name__ == '__main__':
    main()
