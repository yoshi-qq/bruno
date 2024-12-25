from varTypes import menuOperation
from communicationHandler import initCommunication, gameState
from dependencies import graphy
from card import Card
from constants import RGB_COLORS, OWN_HAND_POSITION, OWN_HAND_SIZE, DEFAULT_IP, DEFAULT_PORT
import sys, socket
import visuals, network, gameLogic

lastMenu: str = None
currentMenu: str = "main" # TODO: make menu an enum
buttons: list = []

def hostButton(ip, port):
    global currentMenu
    network.host(ip, port)
    currentMenu = "lobby"
    initCommunication("host")

def joinButton(ip, port):
    global currentMenu
    network.join(ip, port)
    currentMenu = "lobby"
    initCommunication("player")

def settingsButton():
    global currentMenu
    currentMenu = "settings"

def exitButton():
    global currentMenu
    currentMenu = "exit"

def leaveGameButton():
    global currentMenu
    network.leave()
    currentMenu = "main"

def drawMainMenu(operation: menuOperation):
    global buttons
    match operation:
        case menuOperation.OPEN:
            buttons = buttons + [
                # Card("blue", "settings", hoverable = True),
                Card("red", "host", hoverable = True),
                Card("green", "join", hoverable = True),
                Card("blue", "settings", hoverable = True),
                Card("black", "exit", hoverable = True),
            ] 
            buttons[0].renderObject.clickAction = hostButton
            buttons[0].renderObject.arguments = (DEFAULT_IP, DEFAULT_PORT)
            buttons[1].renderObject.clickAction = joinButton
            buttons[1].renderObject.arguments = (DEFAULT_IP, DEFAULT_PORT)
            buttons[2].renderObject.clickAction = settingsButton
            buttons[3].renderObject.clickAction = exitButton
            visuals.drawHand(buttons, True, OWN_HAND_POSITION[0], OWN_HAND_POSITION[1], OWN_HAND_SIZE)
        case menuOperation.CLOSE:
            for button in buttons:
                button.remove()
            buttons = []
        case menuOperation.DRAW:
            pass

def drawLobbyMenu(operation: menuOperation):
    global buttons, currentMenu
    match operation:
        case menuOperation.OPEN:
            buttons = []
            buttons.append(myIP := graphy.RenderText(surface = graphy.screen, x = graphy.middle[0], y = 50, middle = True, text = f"IP: {socket.gethostbyname(socket.gethostname())} | Port: {network.mainObject.port}", size = 50))
            buttons.append(leaveButton := graphy.RenderTextButton(text = "Leave", clickAction = leaveGameButton, color = (230, 20, 0), activeColor = (90, 10, 0),  x = graphy.middle[0]-225, y = graphy.middle[1]*1.75, height=80, width = 250, middle = True))
            match network.me:
                case "host":
                    buttons.append(startButton := graphy.RenderTextButton(text = "Start", clickAction = gameLogic.startGame, color = (0,230,20), activeColor = (0,90,10), x = graphy.middle[0]+225, y = graphy.middle[1]*1.75, height=80, width = 250, middle = True))
                    
                case "player":
                    pass
        case menuOperation.CLOSE:
            for button in buttons:
                button.remove()
            buttons = []
        case menuOperation.DRAW:
            if network.me == "host":
                # TODO: send message to all clients if client list changes
                # TODO: make clients display client list too
                for i, client in enumerate(network.mainObject.clients): # TODO: move logic to network & add getPlayers function to be used here instead
                    ip, port = client.conn.getpeername()
                    
                    buttons.append(banner := graphy.RenderTextButton(x = graphy.middle[0], color = RGB_COLORS[i], borderColor = (0, 0, 0), textColor = (0, 0, 0), y = 200 + i * 150, width = 800, height = 80, middle = True, text = f"{ip}:{port}", temporary = True))
                    buttons.append(playerNumbers := graphy.RenderTextButton(drawType = "circ", x = banner.x - banner.width//(3/2) - 100, y = banner.y, text = str(i+1), color = RGB_COLORS[i], borderColor = (0, 0, 0), textColor = (0, 0, 0), width = banner.height*1.2, height = banner.height*1.2, middle = True, temporary = True))
            else:
                pass
                # if hasattr(network.mainObject, 'clients'): # TODO: 1. find out what this does 2. move it to network and replace this with an adequately named function
                #     for i, client in enumerate(network.mainObject.clients):
                #         ip, port = client.conn.getpeername()

                #         buttons.append(banner := graphy.RenderTextButton(x = graphy.middle[0], color = RGB_COLORS[i], borderColor = (0, 0, 0), textColor = (0, 0, 0), y = 200 + i * 150, width = 800, height = 80, middle = True, text = f"{ip}:{port}", temporary = True))
                #         buttons.append(playerNumbers := graphy.RenderTextButton(drawType = "circ", x = banner.x - banner.width//(3/2) - 100, y = banner.y, text = str(i+1), color = RGB_COLORS[i], borderColor = (0, 0, 0), textColor = (0, 0, 0), width = banner.height*1.2, height = banner.height*1.2, middle = True, temporary = True))
                    
def drawGameMenu(operation: menuOperation):
    global buttons, background
    match operation:
        case menuOperation.OPEN:
            buttons = []
            background = graphy.RenderImage(imageName = "background", width=graphy.nativeResolution[0], height=graphy.nativeResolution[1])
        case menuOperation.CLOSE:
            pass
        case menuOperation.DRAW:
            pass
        
def drawSettingsMenu(operation: menuOperation):
    match operation:
        case menuOperation.OPEN:
            pass
        case menuOperation.CLOSE:
            pass
        case menuOperation.DRAW:
            pass

# (Name: str -> Function: function) matching for menu drawing functions
menuFunctions = {
    None: lambda action: None,
    "main": drawMainMenu,
    "lobby": drawLobbyMenu,
    "game": drawGameMenu,
    "settings": drawSettingsMenu, # TODO: add settings menu
    "exit": sys.exit,  # TODO: replace with proper exit function
}

def displayMenu():
    global lastMenu, currentMenu
    if lastMenu != currentMenu:
        menuFunctions[lastMenu](menuOperation.CLOSE)
        menuFunctions[currentMenu](menuOperation.OPEN)
        print(f"Switched from {lastMenu} to {currentMenu}")
        lastMenu = currentMenu
    menuFunctions[currentMenu](menuOperation.DRAW)