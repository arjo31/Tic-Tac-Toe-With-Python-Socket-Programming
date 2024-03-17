import socket
import time
from game import TicTacToe

game = TicTacToe()
gameBoard = game.boards

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = '127.0.0.1'
port = 12345

server_socket.bind((hostname,port))

server_socket.listen()

print("Game server connected to network..... Ready to play")

players = []
playerName = []

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

def checkFilled(boards, row, col,client):
    flag = True
    if (boards[row][col]!=' '):
        print("Invalid choice : Already filled. Fill choice again")
        client.send("Invalid choice : Already filled. Fill choice again".encode())
        flag = False
    return flag

def updateBoard(boards, player, symbol, r, c, client):
    while True:
        try:               
            while (not checkFilled(boards,r,c,client)):
                playerTurn(player)
                r = int(client.recv(1024).decode())
                c = int(client.recv(1024).decode())
            boards[r][c] = symbol
            break
        except:
            print("Index Out of Bounds.... Please enter again")
            if (client==player[0]):
                player1()
            else:
                player2()
   
def playerTurn(player):
    players[player-1].send(f"Player {player}'s turn".encode())

def recieve_players():
    try:
        welcomeMsg = "Welcome to the TicTacToe Game Server......"
        for i in range(2):
            client, address = server_socket.accept()
            client.send(welcomeMsg.encode())
            client_name = client.recv(1024).decode()

            players.append(client)
            playerName.append(client_name)
            print(f"{client_name} has joined the server...")
            client.send(f"{str(i+1)}".encode())    
        sendBoard()
        server_socket.close()
            
    except socket.error as e:
        print("Server Connection error : ", e)
    except:
        print("Error occured")

def sendBoard():
    try:
        for player in players:
            player.send("BOARD".encode())
            time.sleep(0.05)
            player.send(str(gameBoard).encode())   
        startGame()
    except:
        pass

def player1():
    while True:
        print("Player 1's turn")
        players[0].send("Player 1's turn".encode())
        row = int(players[0].recv(1024).decode())
        col = int(players[0].recv(1024).decode())
        if (row > 4 or col > 4 or row < 0 or col < 0):
            players[0].send("Index Out of Bounds.... Please enter again".encode())
            time.sleep(0.05)
            continue
        updateBoard(gameBoard, 1, 'X', row, col, players[0])
        players[0].send("BOARD".encode())
        time.sleep(0.05)
        players[0].send(str(gameBoard).encode()) 
        players[1].send("BOARD".encode())
        time.sleep(0.05)
        players[1].send(str(gameBoard).encode()) 
        break

def player2():
    while True:
        print("Player 2's turn")
        players[1].send("Player 2's turn".encode())
        row = int(players[1].recv(1024).decode())
        col = int(players[1].recv(1024).decode())
        if (row > 4 or col > 4 or row < 0 or col < 0):
            players[1].send("Index Out of Bounds.... Please enter again".encode())
            time.sleep(0.05)
            continue
        updateBoard(gameBoard, 2, 'O', row, col, players[1])
        players[0].send("BOARD".encode())
        time.sleep(0.05)
        players[0].send(str(gameBoard).encode()) 
        players[1].send("BOARD".encode())
        time.sleep(0.05)
        players[1].send(str(gameBoard).encode()) 
        break

def startGame():
    try:
        win = False
        while(not boardFilled(gameBoard)):
            
            if (not boardFilled(gameBoard)):
                player1()
            
            if winConditions(gameBoard):
                msg = "Player 1 wins"
                print(msg)
                players[0].send(msg.encode())
                players[1].send(msg.encode())
                win = True
                break

            if (not boardFilled(gameBoard)):
                player2()
            
            if (winConditions(gameBoard)):
                win = True
                msg = "Player 2 wins"
                print(msg)
                players[0].send(msg.encode())
                players[1].send(msg.encode())
                break

        if (not win):
            print("Draw...Nobody has won!!!")
            players[0].send("Draw...Nobody has won!!!".encode())
            players[1].send("Draw...Nobody has won!!!".encode())
        pass
    except:
        pass

recieve_players()