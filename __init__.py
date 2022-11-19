from pieces import *

from player import *

class BlokusGame():
    FOUR_EDGES = [[-1, 0], [1, 0], [0, 1], [0, -1]] 
    FOUR_CORNERS = [[-1, -1], [-1, 1], [1, 1], [1, -1]]

    def __init__(self):
        self.boardSize = 14
        self.p1 = Player('□')
        self.p2 = Player('■')
        self.board = [['o' for _ in range(14)] for _ in range(14)]
        self.turn = 1
        self.currentPlayer = None
        self.playGame()

    def displayBoard(self):
        print('    a b c d e f g h i j k l m n') 
        print('    ___________________________')
        rows = iter([' 1', ' 2', ' 3', ' 4', ' 5', ' 6', ' 7', ' 8', ' 9', '10', '11', '12', '13', '14'])
        for row in self.board:
            print('{} |'.format(next(rows)), end='')
            for i in range(self.boardSize - 1):
                print('{} '.format(row[i]), end='')
            print('{}|'.format(row[-1]))    
        print('    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾')

    def placePiece(self, move, piece):
        row = int(move[1:]) - 1
        col = ord(move[0].lower()) - 97
        for drow, dcol in piece.dirs:
            self.board[row+drow][col+dcol] = self.currentPlayer.square

    def validateSelection(self, selectedPiece): 
        return self.currentPlayer.checkExists(selectedPiece.upper())

    def isReorient(self, move):
        return move in ['cw', '180', 'ccw', 'v', 'h']

    def isValidMove(self, move, piece):
        if len(move) not in [2, 3]:
            return False
        elif move[0] not in 'abcdefghijklmn':
            return False
        elif move[1:] not in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14']:
            return False
        elif self.currentPlayer.onFirst:
            row = int(move[1:]) - 1
            col = ord(move[0].lower()) - 97
            for drow, dcol in piece.dirs: # each part of the piece
                if sorted([row+drow, col+dcol]) == [4, 9]:
                    if self.board[row+drow][col+dcol] == 'o':
                        self.currentPlayer.onFirst = False
                        return True
            return False            
        else:
            row = int(move[1:]) - 1
            col = ord(move[0].lower()) - 97
            satisfyCorner = False
            for drow, dcol in piece.dirs: # each part of the piece
                startRow, startCol = row + drow, col + dcol # square where it'll be placed
                if not (0 <= startRow < self.boardSize) and (0 <= startCol < self.boardSize):
                    return False # piece is off the grid
                if self.board[startRow][startCol] != 'o':
                    return False # piece overlaps
                for dr, dc in BlokusGame.FOUR_EDGES: # check for edge
                    edgeR, edgeC = startRow + dr, startCol + dc
                    if (0 <= edgeR < self.boardSize) and (0 <= edgeC < self.boardSize): # need to check this edge
                        if self.board[edgeR][edgeC] == self.currentPlayer.square:
                            return False
                for dr, dc in BlokusGame.FOUR_CORNERS: # check for corner
                    cornerR, cornerC = startRow + dr, startCol + dc
                    if (0 <= cornerR < self.boardSize) and (0 <= cornerC < self.boardSize): # need to check this corner
                        if self.board[cornerR][cornerC] == self.currentPlayer.square:
                            satisfyCorner = True
            return satisfyCorner
                            
    def takeTurn(self): 
        pieceIsSelected = False
        self.currentPlayer = eval('self.p{}'.format(self.turn))
        while True:            
            self.displayBoard() # display board for each turn                        
            if not pieceIsSelected:
                self.currentPlayer.displayRemaining() # display remaining pieces to choose from
                selectedPiece = input("Player {}, select a piece to play or type 'pass' to pass: ".format(self.turn))
                if selectedPiece.lower() == 'pass': # end turn
                    self.turn = 3 - self.turn
                    return False
                elif self.validateSelection(selectedPiece): # picked a valid piece
                    pieceIsSelected = True
                    piece = self.currentPlayer.getPiece(selectedPiece)
                else:   # what do to if the selection is not valid
                    print('Invalid Piece!')
            else: # piece is already selected
                piece.display()
                move = input("Player {}, play, re-orient, re-select the piece with 'exit', or type 'pass' to pass: ".format(self.turn))
                if move.lower() == 'pass': # end turn
                    self.turn = 3 - self.turn
                    return False
                elif move.lower() == 'exit': # picking a new piece
                    pieceIsSelected = False
                elif self.isReorient(move): # rotating piece
                    if move in ['h', 'v']:
                        piece.reflect(move)
                    else:
                        piece.rotate(move)
                elif self.isValidMove(move, piece):
                    self.placePiece(move, piece)
                    self.currentPlayer.removePiece(piece.symbol)
                    self.turn = 3-self.turn
                    return True
                else:
                    print('Invalid move!')                

    def playGame(self):
        passes = 0 # end game if 2 passes in a row
        while passes != 2:
            if not self.takeTurn():
                passes += 1
            else:
                passes = 0
        p1Score, p2Score = 89, 89
        for piece in self.p1.pieces:
            p1Score -= len(piece.dirs)
        for piece in self.p2.pieces:
            p2Score -= len(piece.dirs)
        if p1Score > p2Score:
            print('Player 1 Wins with □! Score: {} - {}'.format(p1Score, p2Score))
        elif p1Score == p2Score:
            print("It's a tie! Score: {} - {}".format(p1Score, p2Score))
        else:
            print('Player 2 Wins with ■! Score: {} - {}'.format(p1Score, p2Score))

def main():
    game = BlokusGame()
    game.displayBoard()

if __name__ == '__main__':
    main()
