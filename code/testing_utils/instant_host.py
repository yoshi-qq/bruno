import time
from ..main import init, start
from ..config.constants import DEFAULT_IP, DEFAULT_PORT
from ..utils.menuing import hostButton
from ..utils.gameLogic import startGame

def host():
    hostButton(DEFAULT_IP, DEFAULT_PORT)

def main():
    init()
    host()
    time.sleep(1)
    startGame()
    start()

if __name__ == '__main__':
    main()