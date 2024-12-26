from ..main import init, start
from ..config.constants import DEFAULT_IP, DEFAULT_PORT
from ..utils.menuing import joinButton

def intercept():
    joinButton(DEFAULT_IP, DEFAULT_PORT)

def main():
    init()
    intercept()
    start()
    
if __name__ == '__main__':
    main()