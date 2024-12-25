import os
ROOT = os.path.dirname(os.path.abspath(__file__))

# NETWORK
DEFAULT_IP = 'localhost'
DEFAULT_PORT = 54322

# DESIGN
RGB_COLORS = [(237, 28, 36), (80, 170, 68), (0, 114, 188), (255, 222, 22)]
COLORS = ["red", "green", "blue", "yellow"]
SPECIAL_COLOR = "black"

# CARDS
VALUES = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "switch", "skip", "plus2", "colors", "plus4"]
SPECIAL_VALUES = ["colors", "plus4"]

# RULES
START_CARDS_AMOUNT = 7
MAX_TURN_LENGTH = 30 # in seconds
PENALTY_CARD_AMOUNT = 2

# HANDS VISUALS
CARD_BACK_ASSET = "cardback"
CARD_BASE_WIDTH = 300
HAND_BASE_HARD_WIDTH = 1/4
HAND_BASE_SOFT_WIDTH = 1/6
    # Own Hand
OWN_HAND_POSITION = (960-CARD_BASE_WIDTH/2, 750)
OWN_HAND_SIZE = 3
OWN_HAND_ANGLE = 0 # DEG
    # Other Players
OTHER_HANDS_POSITIONS = [(320-CARD_BASE_WIDTH/2, 250), (960-CARD_BASE_WIDTH/2, 0), (1600-CARD_BASE_WIDTH/2, 250)]
OTHER_HANDS_SIZES = (1.5, 2, 1.5)
OTHER_HANDS_ANGLES = (-45, 0, 45) # DEG
