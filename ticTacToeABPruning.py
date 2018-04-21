import copy

X = 'X'
O = 'O'
CONTINUE = 'Continue'
TIE = 'Nobody'
LAST_TURN = 9
EMPTY = ' '
SIZE = 3
INFINITY = 100
INFINITE = 50

class GameBoard:
  def __init__(self):
    self.currentState = [
        [' ', ' ', ' '],
        [' ', ' ', ' '],
        [' ', ' ', ' ']]
    self.nextStates = []
    self.previousState = None
    self.heuristicValue = 0

def printBoard(gameBoard):
  for row in range(0, SIZE):
    for col in range(0, SIZE):
      print('[' + gameBoard.currentState[row][col] + ']', end = '')
    print()
  print()

def valueCounter(currentState, side):
  if(currentState == side):
    return 1
  return 0
  
def tabulateValues(xValue, oValue):
  value = 0
  if(xValue > 0):
    if(oValue < 0):
      return 0
    value += 1
    if(xValue > 1):
      value += 2
    if(xValue > 2):
      return 100
  if(oValue < 0):
    value -= 1
    if(oValue < -1):
      value -= 2
    if(oValue < -2):
      return -100
  return value
  
def calculateHorizontalValue(currentState):
  value = 0
  for row in range(0, SIZE):
    xValue = 0
    oValue = 0
    for col in range(0, SIZE):
      xValue += valueCounter(currentState[row][col], X)
      oValue -= valueCounter(currentState[row][col], O)
    value += tabulateValues(xValue, oValue)
  return value

def calculateVerticalValue(currentState):
  value = 0
  for col in range(0, SIZE):
    xValue = 0
    oValue = 0
    for row in range(0, SIZE):
      xValue += valueCounter(currentState[row][col], X)
      oValue -= valueCounter(currentState[row][col], O)
    value += tabulateValues(xValue, oValue)
  return value

def calculateDiagonalValue(currentState):
  value = 0
  xValue = 0
  oValue = 0
  for i in range(0, SIZE):
    xValue += valueCounter(currentState[i][i], X)
    oValue -= valueCounter(currentState[i][i], O)
  value += tabulateValues(xValue, oValue)
  xValue = 0
  oValue = 0
  for i in range(0, SIZE):
    xValue += valueCounter(currentState[i][SIZE - i - 1], X)
    oValue -= valueCounter(currentState[i][SIZE - i - 1], O)
  value += tabulateValues(xValue, oValue)
  return value
  
def getHeuristicValue(currentState):
  value = 0
  value += calculateHorizontalValue(currentState)
  value += calculateVerticalValue(currentState)
  value += calculateDiagonalValue(currentState)
  return value

def getNextState(gameBoard, side, row, col):
  tempBoard = copy.deepcopy(gameBoard)
  tempBoard.currentState[row][col] = side
  tempBoard.nextStates = []
  gameBoard.nextStates.append(tempBoard)
  gameBoard.nextStates[-1].previousState = gameBoard
  return gameBoard

def getNextStates(gameBoard, side):
  for row in range(0, SIZE):
    for col in range(0, SIZE):
      if(gameBoard.currentState[row][col] == EMPTY):
        gameBoard = getNextState(gameBoard, side, row, col)
  return gameBoard
  
def getLegalMoves(gameBoard, side):
  side1 = EMPTY
  if(side == X):
    side1 = O
  else:
    side1 = X
  gameBoard = getNextStates(gameBoard, side)
  for i in range(0, len(gameBoard.nextStates)):
    gameBoard.nextStates[i] = getNextStates(gameBoard.nextStates[i], side)
  return gameBoard
  
def getMinValue(gameBoard, alpha, beta):
  '''Returns a utility value.'''
  gameBoard.heuristicValue = getHeuristicValue(gameBoard.currentState)
  if(len(gameBoard.nextStates) == 0):
    return gameBoard
  gameBoard.heuristicValue = INFINITY
  for a in range(0, len(gameBoard.nextStates)):
    gameBoard.heuristicValue = min(gameBoard.heuristicValue, getMaxValue(gameBoard.nextStates[a], alpha, beta).heuristicValue)
    if(gameBoard.heuristicValue <= alpha):
      return gameBoard
    beta = min(beta, gameBoard.heuristicValue)
  return gameBoard
      
def getMaxValue(gameBoard, alpha, beta):
  '''Returns a utility value.'''
  gameBoard.heuristicValue = getHeuristicValue(gameBoard.currentState)
  if(len(gameBoard.nextStates) == 0):
    return gameBoard
  gameBoard.heuristicValue = -INFINITY
  for a in range(0, len(gameBoard.nextStates)):
    gameBoard.heuristicValue = max(gameBoard.heuristicValue, getMinValue(gameBoard.nextStates[a], alpha, beta).heuristicValue)
    if(gameBoard.heuristicValue >= beta):
      return gameBoard
    alpha = max(alpha, gameBoard.heuristicValue)
  return gameBoard

def executeAlphaBetaSearch(gameBoard, side):
  '''Returns a nextStates[i] with the value from maxValue(gameBoard, alpha, beta).'''
  if(side == X):
    gameBoard = getMaxValue(gameBoard, -INFINITY, INFINITY)
  else:
    gameBoard = getMinValue(gameBoard, -INFINITY, INFINITY)
  for i in range(0, len(gameBoard.nextStates)):
    if(gameBoard.nextStates[i].heuristicValue == gameBoard.heuristicValue):
      return gameBoard.nextStates[i]
  return gameBoard

def checkWin(gameBoard):
  if(calculateHorizontalValue(gameBoard.currentState) > INFINITE):
    return X
  if(calculateHorizontalValue(gameBoard.currentState) < -INFINITE):
    return O
  if(calculateVerticalValue(gameBoard.currentState) > INFINITE):
    return X
  if(calculateVerticalValue(gameBoard.currentState) < -INFINITE):
    return O
  if(calculateDiagonalValue(gameBoard.currentState) > INFINITE):
    return X
  if(calculateDiagonalValue(gameBoard.currentState) < -INFINITE):
    return O
  return CONTINUE

def checkEndGame(gameBoard, counter):
  side = checkWin(gameBoard)
  if(side != CONTINUE):
    return side
  if(counter == LAST_TURN):
    return TIE
  return CONTINUE
  
def runApplication(gameBoard, side, counter):
  winner = checkEndGame(gameBoard, counter)
  if(winner != CONTINUE):
    printBoard(gameBoard)
    print(winner + ' wins.')
    return gameBoard  
  printBoard(gameBoard)
  userInput = input('Enter to continue\n')
  if(userInput == ''):
    gameBoard = getLegalMoves(gameBoard, side)
    gameBoard = executeAlphaBetaSearch(gameBoard, side)
    counter += 1
    if(side == X):  
      runApplication(gameBoard, O, counter)
    else:
      runApplication(gameBoard, X, counter)
  else:
    print('You\'ve terminated the program.')

def main():
  gameBoard = GameBoard()
  gameBoard = getLegalMoves(gameBoard, X)
  runApplication(gameBoard, X, 0)
      
main()
