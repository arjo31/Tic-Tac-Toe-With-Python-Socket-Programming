import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = '127.0.0.1'
port = 12345
client_socket.connect((hostname, port))

def displayBoard(matrix):
    for row in matrix:
        print(' '.join(row))

def winConditions(boards):
    win_combinations = [
        [(0, 0), (2, 0), (4, 0)],  
        [(0, 2), (2, 2), (4, 2)],
        [(0, 4), (2, 4), (4, 4)],
        [(0, 0), (0, 2), (0, 4)],
        [(2, 0), (2, 2), (2, 4)],
        [(4, 0), (4, 2), (4, 4)],
        [(0, 0), (2, 2), (4, 4)],
        [(0, 4), (2, 2), (4, 0)]
    ]

    for combination in win_combinations:
        symbols = [boards[row][col] for row, col in combination]
        if symbols == ['X', 'X', 'X'] or symbols == ['O', 'O', 'O']:
            return True
    return False

def boardFilled(boards):
    count = 0
    for i in range(5):
        for j in range(5):
            if (boards[i][j]==' '):
                count+=1
    if (count==0):
        return True
    return False

def checkFilled(boards, row, col):
    flag = True
    if (boards[row][col]!=' '):
        print("Invalid choice : Already filled. Fill choice again")
        flag = False
    return flag

def updateBoard(boards , player, symbol):
    while True:
        try:
            r,c = playerTurn(player)                
            while (not checkFilled(boards,r,c)):
                r,c = playerTurn(player)
            boards[r][c] = symbol
            if (player==1):
                player = 2
            elif (player==2):
                player = 1
            break
        except:
            print("Index Out of Bounds.... Please enter again")
            if (player==1):
                player = 1
            elif (player==2):
                player = 2
    return player

def playerTurn(player):
    print(f"Player {player}'s turn")
    r = int(input("Enter row number = "))
    r = 2 * r
    c = int(input("Enter column number = "))
    c = 2 * c
    return (r,c)

def playGame(boards, player):
    print("Let's Begin.......")
    win = False
    p1 = ""
    p2 = ""
    if (player==1):
        print("p1")
        p1 = input("Choose : X or O = ")
        if (p1=="O"):
            p2 = "X"
        else:
            p2 = "O"
    elif (player==2):
        print("p2")
        p2 = input("Choose : X or O = ")
        if (p2=="O"):
            p1 = "X"
        else:
            p1 = "O"
    while (not boardFilled(boards)):
        if (player==1):
            player = updateBoard(boards, player, p1)
        elif (player==2):
            player = updateBoard(boards, player, p2)

        displayBoard(boards)

        if (winConditions(boards)):
            if (player==1):
                print(f"Player 2 '('{p2}')' has won the game")
            elif (player==2):
                print(f"Player 1 '('{p1}')' has won the game")
            win = True
            break

    if (not win):
        print("Draw!!!!!. Nobody has won....")

playerNo = 0

def recieve_from_server():
    try:
        welcomeMsg = client_socket.recv(1024).decode()
        print(welcomeMsg)
        name = input("Enter your name = ")
        client_socket.send(name.encode())
        playerMsg = client_socket.recv(1024).decode()
        for c in playerMsg:
            if (c=='1'):
                playerNo = 1
            elif (c=='2'):
                playerNo = 2
        print("I am player no : ", playerNo)

        boardMessage = client_socket.recv(1024).decode()
        if (boardMessage=="BOARD"):
            board = client_socket.recv(2048).decode()
            board = eval(board)
            displayBoard(board)
        message()
    except:
        pass

def message():
    try:
        while True:
            msg = client_socket.recv(1024).decode()
            if (msg=="Player 1's turn"):
                row, col = playerTurn(1)
                client_socket.send(str(row).encode())
                client_socket.send(str(col).encode())
            elif (msg=="Player 2's turn"):
                row, col = playerTurn(2)
                client_socket.send(str(row).encode())
                client_socket.send(str(col).encode())
            elif(msg=="BOARD"):
                board = client_socket.recv(2048).decode()
                board = eval(board)
                displayBoard(board)
            elif(msg=="Index Out of Bounds.... Please enter again"):
                print(msg)
                continue
            elif (msg=="Invalid choice : Already filled. Fill choice again"):
                print(msg)
                continue
            else:
                print(msg)
                break
    except:
        pass

recieve_from_server()