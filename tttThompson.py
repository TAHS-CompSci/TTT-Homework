import random

xScore = 0
oScore = 0
ai = input('Would you like to play against an Ai: ')
y_list = ['yes','y','ye']

def printBoard(board):
    print(board['top-L'] + '|' + board['top-M'] + '|' + board['top-R'])
    print('-----')
    print(board['mid-L'] + '|' + board['mid-M'] + '|' + board['mid-R'])
    print('-----')
    print(board['low-L'] + '|' + board['low-M'] + '|' + board['low-R'])

def score(xScore, oScore):
    if xScore >= oScore:
        highScore = xScore
    else:
        highScore = oScore
    try:
        with open('highScoreTicTac.txt','r') as file:
            for x in file.read():
                if int(x) > highScore:
                    highScore = x
            else:
                with open('highScoreTicTac.txt','w') as file:
                    file.write(str(highScore))
    except FileNotFoundError:
        with open('highScoreTicTac.txt','w') as file:
            file.write(str(highScore))
    return highScore  

def checkWin(moveList,turn,theBoard):
    checkRowUp = []
    checkRowAcross = []
    diagCount = 0
    for move in moveList[turn]:
        checkRowUp.append(move[0])
        checkRowAcross.append(move[-1])
    for x in set(checkRowUp):
        if checkRowUp.count(x) >= 3:
            return True
    for x in set(checkRowAcross):
        if checkRowAcross.count(x) >= 3:
            return True
    for x in ['top-L','mid-M','low-R']:
        if x in moveList[turn]:
            diagCount += 1
        if diagCount == 3:
            return True
    diagCount = 0
    for x in ['top-R','mid-M','low-L']:
        if x in moveList[turn]:
            diagCount += 1
        if diagCount == 3:
            return True
    return False

def catTest(board,moveList,turn):
    testList = []
    newList = moveList
    for x in board.keys():
        if x not in moveList['moves']:
            newList[turn].append(x)
            test = checkWin(newList,turn,board)
            testList.append(test)
            newList[turn].pop()
    if True in testList:
        return False
    else:
        return True          
    
def aipic(turn,moveList,theBoard):
    pmoves = []
    newList = moveList
    newBoard = theBoard
    m = ' '
    for x in theBoard.keys():
        if theBoard[x] == ' ':
            pmoves.append(x)
    for x in pmoves:
        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'
        newList[turn].append(x)
        newBoard[x] = turn
        if checkWin(newList,turn,newBoard):
            m =  x
        newList[turn].pop()
        newBoard[x] = ' '
        if turn == 'X':
            turn = 'O'
        else:
            turn = 'X'
        newList[turn].append(x)
        newBoard[x] = turn
        if checkWin(newList,turn,newBoard):
            return x
        newList[turn].pop()
        newBoard[x] = ' '
    if m != ' ':
        return m
    else:
        return random.choice(pmoves)

def movecheck(turn,theBoard,moveList):
    global y_list
    global ai
    move = ' '
    while move not in theBoard.keys():
        if ai in y_list:
            if turn == 'O':
                move = aipic(turn,moveList,theBoard)
                print('Your move O\n- ' + move)
            else:
                move = input('Your move ' + turn + '. Which space? (type ''help'' for more info)\n- ')
        if ai not in y_list:
            move = input('Your move ' + turn + '. Which space? (type ''help'' for more info)\n- ')
        while move not in theBoard.keys() or move in moveList['moves']:
            if move == 'help':
                possibleMoves = ''
                for x in theBoard.keys():
                    if theBoard[x] == ' ':
                        possibleMoves += x + ' '
                print('\nPossible Moves\n' + possibleMoves)
                move = input('\n- ')
            else:
                print('That is not a viable move: (Type "help" for more info)')
                move = input('\n- ')
        return move

def ttt():
    moveList = {'X':[], 'O':[],'moves': []}
    theBoard = {'top-L': ' ', 'top-M': ' ', 'top-R': ' ', 'mid-L': ' ', 'mid-M': ' ', 'mid-R': ' ', 'low-L': ' ', 'low-M': ' ', 'low-R': ' '}
    global xScore
    global oScore  
    global y_list
    turn = 'X'
    while True:
        for i in range(9):
            if i == 7:
               cat = catTest(theBoard,moveList,'X')
               cat2 = catTest(theBoard,moveList,'O')
            if i == 8:
               cat = catTest(theBoard,moveList,'X')
               cat2 = True
            if i >= 7:
                if cat == True and cat2 == True:
                   printBoard(theBoard)
                   print('\nCat\n')
                   break
            printBoard(theBoard)
            move = movecheck(turn,theBoard,moveList)
            moveList[turn].append(move)
            moveList['moves'].append(move)
            theBoard[move] = turn
            if checkWin(moveList,turn,theBoard):
                printBoard(theBoard)
                print('\nYou Win ' + turn + '\n')
                if turn == 'X':
                    xScore += 1
                else:
                    oScore += 1
                break
            if turn == 'X':
                turn = 'O'
            else:
                turn = 'X'
        print("X's Score is " + str(xScore) +"\nO's Score is " + str(oScore) + '\n')
        highScore = score(xScore,oScore)
        print(str(highScore) + ' is the High Score\n')
        break
    replay = input('\nDo you want to play again: ')
    if replay.lower() in y_list:
        ttt()

ttt()
