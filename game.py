class TicTacToe():
    def __init__(self):
        self.boards = [
            [' ','|',' ','|',' '],
            ['—','|','—','|','—'],
            [' ','|',' ','|',' '],
            ['—','|','—','|','—'],
            [' ','|',' ','|',' ']
        ]

    def displayBoard(self):
        for row in self.boards:
            print(' '.join(row))

    def updateBoard(self, player, symbol):
        while True:
            try:
                r,c = self.playerTurn(player)                
                while (not self.checkFilled(r,c)):
                    r,c = self.playerTurn(player)
                self.boards[r][c] = symbol
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
    
    def winConditions(self):
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
            symbols = [self.boards[row][col] for row, col in combination]
            if symbols == ['X', 'X', 'X'] or symbols == ['O', 'O', 'O']:
                return True
        return False
    
    def playerTurn(self, player):
        print(f"Player {player}'s turn")
        r = int(input("Enter row number = "))
        r = 2 * r
        c = int(input("Enter column number = "))
        c = 2 * c
        return (r,c)

    def boardFilled(self):
        count = 0
        for i in range(5):
            for j in range(5):
                if (self.boards[i][j]==' '):
                    count+=1
        if (count==0):
            return True
        return False

    def checkFilled(self, row, col):
        flag = True
        if (self.boards[row][col]!=' '):
            print("Invalid choice : Already filled. Fill choice again")
            flag = False
        return flag
    
    def playGame(self):
        print("Let's Begin.......")

        self.displayBoard()

        win = False
        turn = 1
        p1 = ""
        p2 = ""
        if (turn==1):
            p1 = input("Choose : X or O = ")
            if (p1=="O"):
                p2 = "X"
            else:
                p2 = "O"
        elif (turn==2):
            p2 = input("Choose : X or O = ")
            if (p2=="O"):
                p1 = "X"
            else:
                p1 = "O"
        while (not self.boardFilled()):
            if (turn==1):
                turn = self.updateBoard(turn, p1)
            elif (turn==2):
                turn = self.updateBoard(turn, p2)

            self.displayBoard()

            if (self.winConditions()):
                if (turn==1):
                    print(f"Player 2 '('{p2}')' has won the game")
                elif (turn==2):
                    print(f"Player 1 '('{p1}')' has won the game")
                win = True
                break

        if (not win):
            print("Draw!!!!!. Nobody has won....")
        