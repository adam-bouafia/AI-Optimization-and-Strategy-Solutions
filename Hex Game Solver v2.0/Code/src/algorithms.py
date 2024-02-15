# Importing necessary modules and classes
from Game import Game
from State import State
from random import randint
import copy

noOfNodes = 0

def heuristic(state, l):
    H0 = sum(1 for row in state.board.matrix for tile in row if tile == '.')
    HL = l * H0 + (1 - l) * sum(1 for row in state.board.matrix for tile in row if tile.lower() == state.currentPlayer[0])
    return H0, HL



# Function to update the extreme tiles based on the state of the game
def updateExtremeTiles(state: State) -> None:
    """Updates the extreme tiles of the game.

    Args:
        state (State): The current state of the game.
    """

    i = 0
    j = 0
    ok = False
    # we are looking for the first position in which the computer moved
    # to update the extreme track
    for i in range(state.chosenState.board.NUM_ROWS):
        for j in range(state.chosenState.board.NUM_COLS):
            if state.chosenState.board.matrix[i][j] == state.board.JMAX[0].upper():
                ok = True
                break
        if ok:
            break

    # newPos = (x-coordinate, y-coordinate) = (column, line)
    newPos = (j, i)
    # if JMAX plays with red, then we update either the top piece or the bottom one
    if state.board.JMAX == 'red':
        # we check the existence of the uppermost red piece
        if Game.topTile is None:
            Game.topTile = newPos
        else:
            # we update it if it has moved above it
            if i < Game.topTile[1]:
                Game.topTile = newPos

        # we check the existence of the lowest red piece
        if Game.bottomTile is None:
            Game.bottomTile = newPos
        else:
            # we update it if it has moved below it
            if i > Game.bottomTile[1]:
                Game.bottomTile = newPos

    # otherwise, if JMAX plays with blue, we update the leftmost / rightmost track
    elif state.board.JMAX == 'blue':
        # we check the existence of the leftmost blue piece
        if Game.leftTile is None:
            Game.leftTile = newPos
        else:
            # we update it if it has moved to the left of it
            if j < Game.leftTile[0]:
                Game.leftTile = newPos

        # we update it if it has moved to the left of it
        if Game.rightTile is None:
            Game.rightTile = newPos
        else:
            # we update it if it has moved to the right of it
            if j > Game.rightTile[0]:
                Game.rightTile = newPos

# Function to create possible moves for the game
def createPossibleMove(state: State) -> None:
    """Creates a possible move for the game.

    Args:
        state (State): The current state of the game.
    """

    if not state.possibleMoves:
        i = randint(0, state.board.NUM_ROWS - 1)
        j = randint(0, state.board.NUM_COLS - 1)

        newMatrix = copy.deepcopy(state.board.matrix)
        newMatrix[i][j] = state.board.JMAX[0].upper()
        newGame = Game(newMatrix)
        newGame.currentPlayer = state.board.otherPlayer(state.currentPlayer)
        newGame.text = newGame.currentPlayer.capitalize() + '\'s turn'
        move = newGame

        state.possibleMoves.append(
            State(move, newGame.currentPlayer, state.depth - 1, parent=state))

# Function to apply the Minimax algorithm to the game
# Function to apply the Minimax algorithm to the game
def minimax(state, l):
   global noOfNodes
   if state.depth == 0 or state.board.gameOver():
       _, state.score = heuristic(state, l) # Use HL value from heuristic
       return state

   # we generate the children of the current node (the following possible moves)
   state.possibleMoves = state.nextMoves()

   # if it is the first move, then the computer moves randomly
   createPossibleMove(state)

   # we go recursively in the children of the current state
   statesWithScores = [minimax(move, l) for move in state.possibleMoves] # Pass l here
   noOfNodes += len(statesWithScores)

   # if we are in the tree on a MAX level (it's the computer's turn)
   if state.currentPlayer == Game.JMAX:
      # then we choose the maximum of the fii moves (relative to f)
       state.chosenState = max(statesWithScores, key=lambda x: x.score)
   else:
       # otherwise, we are on the player's move, so we choose the minimum of sons (relative to f)
       state.chosenState = min(statesWithScores, key=lambda x: x.score)

   # we update the parts from extreme positions
   updateExtremeTiles(state)

    # after choosing the next best move for the computer,
    # we update the score of the current state
    # => bottom-up update of the tree
   state.score = state.chosenState.score
   return state


def alpha_beta(alpha, beta, state, l):
    global noOfNodes
    if state.depth == 0 or state.board.gameOver():
        state.score, _ = heuristic(state, l)  # Use H0 value from heuristic
        return state

    # invalid range, stop the search
    if alpha > beta:
        return state

    # we generate the following possible moves
    state.possibleMoves = state.nextMoves()

    # if it is the first move, the computer randomly places a piece on the board
    createPossibleMove(state)

    # if the current player is MAX (the computer)
    if state.currentPlayer == Game.JMAX:

        # the maximum initial score is -infinite
        currentScore = float('-inf')

       # we go recursively in the following possible states
        for move in state.possibleMoves:
            newState = alpha_beta(alpha, beta, move, l)
            noOfNodes += 1

            # we calculate the maximum value among the children of the current node
            # and update the chosen state
            if currentScore < newState.score:
                state.chosenState = newState
                currentScore = newState.score

            # we check if the value of the son can maximize the alpha for the father
            if alpha < newState.score:
                alpha = newState.score
                # if we updated alpha and reached an invalid range, we stop
                if alpha >= beta:
                    break

# if current player is MIN (player)
    elif state.currentPlayer == Game.JMIN:

         # the minimum initial score is infinite
         currentScore = float('inf')

         # we go recursively in the following possible states
         for move in state.possibleMoves:
             newState = alpha_beta(alpha, beta, move, l)
             noOfNodes += 1

             # we calculate the minimum value among the children of the current node
             # and update the chosen state
             if currentScore > newState.score:
                 state.chosenState = newState
                 currentScore = newState.score

             # we check if the value of the son can minimize the beta for the father
             if beta > newState.score:
                 beta = newState.score
                 # if we updated the beta and reached an invalid interval, we stop
                 if alpha >= beta:
                     break

     # we update the parts from extreme positions
    updateExtremeTiles(state)

     # after choosing the next move of the player that will be the most advantageous for the computer,
     # we update the score of the current state
     # => bottom-up update of the tree
    state.score = state.chosenState.score
    return state
