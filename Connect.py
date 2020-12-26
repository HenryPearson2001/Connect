# game of connect 4 with intelligent computer
from random import shuffle

def createBoard(rows,columns):
    board = []
    for i in range(0,rows):
        row = []
        for j in range(0,columns):
            row.append(" ")
        board.append(row)
    return board

def printBoard(board):
    for i in range(0,len(board)):
        print(board[i])
    rowNumbers = ""
    for i in range(1,len(board) + 2):
        rowNumbers += " [" + str(i) + "] "
    print(rowNumbers)

def getMoves(board):
    moves = []
    for i in range(0,len(board[0])):
        if findTopCounter(i,board) != -1:
            moves.append(i)
    return moves

# row inputs start at 0
def moveMade(board,column,symbol):
    height = 0
    height = findTopCounter(column,board)
    if height != -1:
        board[height][column] = symbol
        return [board,True]
    else:
        return [board,False]

# very inefficient
# checks if there are any horizontal connects - returns true if found one
def anaylseHorizontal(board,symbol):
    count = 1
    for j in range(0,len(board)):
        for i in range(0,len(board[j]) - 1):
            if board[j][i] == board[j][i + 1] and board[j][i] == symbol:
                count += 1
            else:
                count = 1
            if count == 4:
                return True
    return False

# checks if there are any vertical connects - returns true if found one
def analyseVertical(board,symbol):
    count = 1
    # iterates through the columns
    for j in range(0,len(board[0])):
        previousElement = ""
        # iterates through the rows of each column
        for i in range(0,len(board)):
            if board[i][j] == previousElement and board[i][j] == symbol:
                count += 1
            else:
                count = 1
            if count == 4:
                return True
            previousElement = board[i][j]
    return False

# iterates through all possible wins created by that move
def checkWinMove(board,symbol,move):
    # created the boundaries for the move (incase near edges)
    if move[1] < 3:
        horizontalLowerBound = 0
    else:
        horizontalLowerBound = move[1] - 3
    if move[1] > len(board[0]) - 3:
        horizontalUpperBound = len(board[0])
    else:
        horizontalUpperBound = move[1] + 3
    if move[0] < 3:
        verticalLowerBound = 0
    else:
        verticalLowerBound = move[0]
    if move[0] > len(board) - 3:
        verticalUpperBound = len(board)
    else:
        verticalUpperBound = move[0]
    # count to keep track of how many in a row there have been
    count = 0
    # check for horizontal possibilites
    for i in range(horizontalLowerBound,horizontalUpperBound):
        # checking the horizontal possibilities
        if board[5 - move[0]][i] == symbol:
            count += 1
            if count == 4:
                return True
    # check if there is a horizontal connect
    if move[0] >= 3:
        if board[verticalLowerBound][move[1]] == symbol and board[verticalLowerBound + 1][move[1]] == symbol and board[verticalLowerBound + 2][move[1]] == symbol:
            return True
    return False

def checkWin(board,symbol,move):
    if getMoves(board) == []:
        return 0
    elif checkWinMove(board,symbol,move):
        return 1
    return 2

# input row starts at 1
def getPlayerMove(numberOfRows):
    validInput = False
    while not validInput:
        try:
            playerMove = int(input("Please enter the number of the row you will go next:\n"))
            if playerMove >= 1 and playerMove <= numberOfRows:
                validInput = True
        except ValueError:
            validInput = False
    return playerMove

# calculates the best possible move for symbol
def getMax(board,symbol,depth):
    if depth < 5:
        bestScore = -2
        # work out the available moves
        moves = getMoves(board)
        count = 0
        # keep searching until found a move guaranteed to win or all moves explored
        while bestScore < 1 and count < len(moves):
            # work out the current game state
            newBoard = board
            newBoard = moveMade(newBoard,moves[count],symbol)[0]
            # calculate the score for the current game state
            result = checkWin(board,symbol,[findTopCounter(moves[count],board),moves[count]])
            # if the game is not ended by that move (does not result in a win, draw or a loss), work out the best move
            if result == 2:
                # swap the symbols
                if symbol == "X":
                    newSymbol = "O"
                else:
                    newSymbol = "X"
                # takes the best move the opponent from this position and uses that score to rank their move
                minimum = getMin(newBoard,newSymbol, depth + 1)
                if minimum[1] > bestScore:
                    bestMove = moves[count]
                    bestScore = minimum[1]
            # if move does decide the game, check if that is better than the current best possible move
            else:
                if result > bestScore:
                    bestMove = moves[count]
                    bestScore = result
            # reset the baord
            newBoard[findTopCounter(moves[count],newBoard) + 1][moves[count]] = " "
            count += 1
        return [bestMove,bestScore]
    else:
        return [0,0]

# calculates the worst possible for the ai originally calling this function
def getMin(board,symbol,depth):
    if depth < 5:
        worstScore = 2
        # work out the available moves
        moves = getMoves(board)
        count = 0
        # keep searching until found a move guaranteed to lose or all moves explored
        while worstScore > -1 and count < len(moves):
            # work out the current game state
            newBoard = board
            newBoard = moveMade(newBoard,moves[count],symbol)[0]
            # calculate the score for the current game state
            result = checkWin(board,symbol,[findTopCounter(moves[count],board),moves[count]])
            # if the game is not ended by that move (does not result in a win, draw or a loss), work out the best move
            if result == 2:
                # swap the symbols
                if symbol == "X":
                    newSymbol = "O"
                else:
                    newSymbol = "X"
                # takes the best move the opponent from this position and uses that score to rank their move
                maximum = getMax(newBoard,newSymbol,depth + 1)
                if maximum[1] < worstScore:
                    worstMove = moves[count]
                    worstScore = maximum[1]
             # if move does decide the game, check if that is better than the current worst possible move
            else:
                if -result < worstScore:
                    worstMove = moves[count]
                    worstScore = -result
            # reset the board
            newBoard[findTopCounter(moves[count],newBoard) + 1][moves[count]] = " "
            count += 1
        return [worstMove,worstScore]
    else:
        return [0,0]
    
def getNextMove(playerSymbol,depth,board):
    bestMove = getMax(board,playerSymbol,0)[0]
    return bestMove

def findTopCounter(column,board):
    count = len(board) - 1
    while True:
        try:
            if board[count][column] == " ":
                return count
            count -= 1
        except IndexError:
            return -1
        
# first player to go has an "X", second has an "O"
def main():
    mainBoard = createBoard(6,7)
    printBoard(mainBoard)
    inGame = True
    currentPlayerSymbol = "X"
    turns = 0
    while inGame:
        move = getNextMove(currentPlayerSymbol,0,mainBoard.copy())
        moveResult = moveMade(mainBoard,move,currentPlayerSymbol)
        #while not moveResult[1]:
        #   moveResult = moveMade(mainBoard,getPlayerMove(7) - 1,currentPlayerSymbol)
        boardCopy = mainBoard
        mainBoard = moveResult[0]
        result = [checkWin(mainBoard,currentPlayerSymbol,[findTopCounter(move,boardCopy),move])]
        print(result)
        if result[0] != 2:
            inGame = False
        printBoard(mainBoard)
        if currentPlayerSymbol == "X":
            currentPlayerSymbol = "O"
        else:
            currentPlayerSymbol = "X"
        turns += 1
    if result[0] == 1:
        print("The winner is " + result[0] + "!!!!!")
    else:
        print("The match was a draw")

    
    

    


main()












