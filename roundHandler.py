from cardHandler import deck
from playerHandler import players
from constants import MAX_TURN_LENGTH
# TODO: add cardHandler and playerHandler first

def startRound():
    for player in players:
        pass # TODO: add turn functionality
        # 1. notify player client its their turn
        # 2. check if special cards a re active
        # 3. wait until player client responds or timeout
        # 4. check if the player has 1 card and not pressed the brUNO button
        # 5. check if game is over -> update game state
        # 6. update all player clients over the played card(s), their new cards and other events