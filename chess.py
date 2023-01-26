import sys

class Position:
    def __init__(self, columnLetter, rowNumber):
        self.col = columnLetter
        self.row = rowNumber

    def relativePos(self, board, numRight, numUp):
        colNum = board.getColNum(self.col)
        newColNum = colNum + numRight  #index of offset
        newRowNum = self.row - 1 + numUp   #index of offset
        if newColNum > len(board.boardCols) - 1 or newColNum < 0:
            return None
        if newRowNum > len(board.boardRows) - 1 or newRowNum < 0:
            return None
        return Position(board.boardCols[newColNum], board.boardRows[newRowNum])

    def __str__(self):
        return  str(self.col) + str(self.row)


    def __eq__(self, other):
        if not isinstance(other, Position):
            return False
        return self.col == other.col and self.row == other.row

class Move:
    def __init__(self, startPos, endPos):
        self.startPos = startPos
        self.endPos = endPos

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.startPos == other.startPos and self.endPos == other.endPos

    def __str__(self):
     return str(self.startPos) + ' ' + str(self.endPos)



class Piece:
    def __init__(self, isWhite, pos):
        self.isWhite = isWhite
        self.pos = pos

    def getColorSymbol(self):
        if self.isWhite:
            return 'W'
        return 'B'


class Pawn(Piece):
    atStart = True
    def __init__(self, isWhite, pos):
        self.isWhite = isWhite
        self.pos = pos

    def getPossMoves(self, board):
        possMoves = []
        #1 if moving up, -1 if moving down
        direction = -1
        if self.isWhite:
            direction = 1

        oneUp = self.pos.relativePos(board, 0, direction)

        if (oneUp is not None) and (board.pieceAt(oneUp) is None):
            possMoves.append(Move(self.pos, oneUp))

        if self.atStart:
            twoUp = self.pos.relativePos(board, 0, 2 * direction)
            if (twoUp is not None) and (board.pieceAt(twoUp) is None):
                possMoves.append(Move(self.pos, twoUp))

        diagLeft = self.pos.relativePos(board, -1, direction)
        diagRight = self.pos.relativePos(board, 1, direction)

        if diagLeft is not None:
            pieceToTake = board.pieceAt(diagLeft)
            if pieceToTake is not None:
                if pieceToTake.isWhite != self.isWhite:
                    possMoves.append(Move(self.pos, diagLeft))

        if diagRight is not None:
            pieceToTake = board.pieceAt(diagRight)
            if pieceToTake is not None:
                if pieceToTake.isWhite != self.isWhite:
                    possMoves.append(Move(self.pos, diagRight))

        return possMoves

    def getSymbol(self):
        return 'P'

class Bishop(Piece):
    def __init__(self, isWhite, pos):
        self.isWhite = isWhite
        self.pos = pos

    def getPossMoves(self, board):
        possMoves = []

        colIdx = board.getColNum(self.pos.col)
        rowIdx = self.pos.row - 1

        for i in range(colIdx + 1, len(board.boardCols)):
            pos = self.pos.relativePos(board, i - colIdx, i - colIdx)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(colIdx - 1, -1, -1):
            pos = self.pos.relativePos(board, i - colIdx, i - colIdx)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(colIdx + 1, len(board.boardCols)):
            pos = self.pos.relativePos(board, i - colIdx, -(i - colIdx))
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(colIdx - 1, -1, -1):
            pos = self.pos.relativePos(board, i - colIdx, -(i - colIdx))
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break

        return possMoves


    def getSymbol(self):
        return 'B'

class Knight(Piece):
    def __init__(self, isWhite, pos):
        self.isWhite = isWhite
        self.pos = pos

    def getPossMoves(self, board):
        possMoves = []
        positions = []

        positions.append(self.pos.relativePos(board, 1, 2))
        positions.append(self.pos.relativePos(board, -1, 2))
        positions.append(self.pos.relativePos(board, 1, -2))
        positions.append(self.pos.relativePos(board, -1, -2))
        positions.append(self.pos.relativePos(board, 2, 1))
        positions.append(self.pos.relativePos(board, 2, -1))
        positions.append(self.pos.relativePos(board, -2, 1))
        positions.append(self.pos.relativePos(board, -2, -1))

        for pos in positions:
            if pos is not None:
                piece = board.pieceAt(pos)
                if piece is None:
                    possMoves.append(Move(self.pos, pos))
                else:
                    if piece.isWhite != self.isWhite:
                        possMoves.append(Move(self.pos, pos))

        return possMoves


    def getSymbol(self):
        return 'N'

class Rook(Piece):
    def __init__(self, isWhite, pos):
        self.isWhite = isWhite
        self.pos = pos

    def getPossMoves(self, board):
        possMoves = []

        colIdx = board.getColNum(self.pos.col)
        rowIdx = self.pos.row - 1

        for i in range(colIdx + 1, len(board.boardCols)):
            pos = self.pos.relativePos(board, i - colIdx, 0)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(colIdx - 1, -1, -1):
            pos = self.pos.relativePos(board, i - colIdx, 0)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(rowIdx + 1, len(board.boardRows)):
            pos = self.pos.relativePos(board, 0, i - rowIdx)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(rowIdx - 1, -1, -1):
            pos = self.pos.relativePos(board, 0, i - rowIdx)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break

        return possMoves

    def getSymbol(self):
        return 'R'

class Queen(Piece):
    def __init__(self, isWhite, pos):
        self.isWhite = isWhite
        self.pos = pos

    def getPossMoves(self, board):
        possMoves = []

        colIdx = board.getColNum(self.pos.col)
        rowIdx = self.pos.row - 1

        for i in range(colIdx + 1, len(board.boardCols)):
            pos = self.pos.relativePos(board, i - colIdx, i - colIdx)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(colIdx - 1, -1, -1):
            pos = self.pos.relativePos(board, i - colIdx, i - colIdx)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(colIdx + 1, len(board.boardCols)):
            pos = self.pos.relativePos(board, i - colIdx, -(i - colIdx))
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(colIdx - 1, -1, -1):
            pos = self.pos.relativePos(board, i - colIdx, -(i - colIdx))
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break

        for i in range(colIdx + 1, len(board.boardCols)):
            pos = self.pos.relativePos(board, i - colIdx, 0)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(colIdx - 1, -1, -1):
            pos = self.pos.relativePos(board, i - colIdx, 0)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(rowIdx + 1, len(board.boardRows)):
            pos = self.pos.relativePos(board, 0, i - rowIdx)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break
        for i in range(rowIdx - 1, -1, -1):
            pos = self.pos.relativePos(board, 0, i - rowIdx)
            piece = board.pieceAt(pos)
            if piece is None:
                possMoves.append(Move(self.pos, pos))
            elif piece.isWhite != self.isWhite:
                possMoves.append(Move(self.pos, pos))
            else:
                break

        return possMoves


    def getSymbol(self):
        return 'Q'

class King(Piece):
    inCheck = False
    def __init__(self, isWhite, pos):
        self.isWhite = isWhite
        self.pos = pos

    def getPossMoves(self, board):
        possMoves = []
        positions = []

        positions.append(self.pos.relativePos(board, 0, 1))
        positions.append(self.pos.relativePos(board, 1, 1))
        positions.append(self.pos.relativePos(board, 1, 0))
        positions.append(self.pos.relativePos(board, 1, -1))
        positions.append(self.pos.relativePos(board, 0, -1))
        positions.append(self.pos.relativePos(board, -1, -1))
        positions.append(self.pos.relativePos(board, -1, 0))
        positions.append(self.pos.relativePos(board, -1, 1))


        for pos in positions:
            if pos is not None:
                piece = board.pieceAt(pos)
                if piece is None:
                    possMoves.append(Move(self.pos, pos))
                else:
                    if piece.isWhite != self.isWhite:
                        possMoves.append(Move(self.pos, pos))
        return possMoves

    def getSymbol(self):
        return 'K'

class Player:
    def __init__(self, isWhite, isBot):
        self.isBot = isBot
        self.isWhite = isWhite

    def getAutoMove(self, board):
        pass

    def getUserMove(self, board):
        moveString = input("Enter two board space seperated by a space: ")
        if moveString == 'resign' or moveString == 'Resign' or moveString == 'forfeit' or moveString == 'Forfeit':
            if self.isWhite:
                board.winner = 'Black'
            else:
                board.winner = 'White'
            board.endGame()
        posStrings = moveString.split(' ')
        if len(posStrings) != 2:
            return None
        if len(posStrings[0]) != 2 or len(posStrings[1]) != 2:
            return None
        startLet = posStrings[0][0]
        endLet = posStrings[1][0]
        startNum = int(posStrings[0][1])
        endNum = int(posStrings[1][1])
        startLetFound = False
        endLetFound = False
        for letter in board.boardCols:
            if startLet == letter:
                startLetFound = True
            if endLet == letter:
                endLetFound = True
        if not (startLetFound and endLetFound):
            return None
        if(startNum < 1 or startNum > 8 or endNum < 1 or endNum > 8):
            return None
        startPos = Position(startLet, startNum)
        endPos = Position(endLet, endNum)
        move = Move(startPos, endPos)
        return move


    def getMove(self, board):
        if self.isBot:
            return self.getAutoMove(board)
        else:
            return self.getUserMove(board)

class Board:
    winner = None
    boardCols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    boardRows = [1, 2, 3, 4, 5, 6, 7, 8]
    whitePieces = [Pawn(True, Position('a', 2)), Pawn(True, Position('b', 2)), Pawn(True, Position('c', 2)), Pawn(True, Position('d', 2)),
                   Pawn(True, Position('e', 2)), Pawn(True, Position('f', 2)), Pawn(True, Position('g', 2)), Pawn(True, Position('h', 2)),
                   Rook(True, Position('a', 1)), Rook(True, Position('h', 1)), Knight(True, Position('b', 1)), Knight(True, Position('g', 1)),
                   Bishop(True, Position('c', 1)), Bishop(True, Position('f', 1)), Queen(True, Position('d', 1)), King(True, Position('e', 1))]

    blackPieces = [Pawn(False, Position('a', 7)), Pawn(False, Position('b', 7)), Pawn(False, Position('c', 7)), Pawn(False, Position('d', 7)),
                   Pawn(False, Position('e', 7)), Pawn(False, Position('f', 7)), Pawn(False, Position('g', 7)), Pawn(False, Position('h', 7)),
                   Rook(False, Position('a', 8)), Rook(False, Position('h', 8)), Knight(False, Position('b', 8)), Knight(False, Position('g', 8)),
                   Bishop(False, Position('c', 8)), Bishop(False, Position('f', 8)), Queen(False, Position('d', 8)), King(False, Position('e', 8))]

    boardPieces = whitePieces
    boardPieces.extend(blackPieces)


    def __init__(self, whiteIsBot, blackIsBot):
        self.playerWhite = Player(True, whiteIsBot)
        self.playerBlack = Player(False, blackIsBot)

    def getColNum(self, letter):
        for i in range(len(self.boardCols)):
            if self.boardCols[i] == letter:
                return i

    def pieceAt(self, position):
        for piece in self.boardPieces:
            if piece.pos == position:
                return piece
        return None

    def printBoard(self):
        for rowNum in reversed(self.boardRows):
            line = str(rowNum) + '|  '
            for colLet in self.boardCols:
                piece = self.pieceAt(Position(colLet, rowNum))
                if piece is not None:
                    line = line + piece.getSymbol() + piece.getColorSymbol() + ' '
                else:
                    line = line + '[] '
            print(line)
        print('    ______________________')
        print('    a  b  c  d  e  f  g  h')

    def validateMove(self, player, move):
        if move is None:
            return False
        piece = self.pieceAt(move.startPos)
        if piece is None:
            return False
        if (player.isWhite and not piece.isWhite) or (not player.isWhite and piece.isWhite):
            return False
        possMoves = piece.getPossMoves(self)
        if len(possMoves) == 0:
            return False
        for possMove in possMoves:
            if possMove == move:
                return True
        return False

    def movePiece(self, move):
        endPiece = self.pieceAt(move.endPos)
        if endPiece is not None:
            endPiece.pos = None
        self.pieceAt(move.startPos).pos = move.endPos


    def simulate(self):
        self.printBoard()
        while(self.winner is None):
            print("WHITE'S TURN")
            whiteMove = self.playerWhite.getMove(self)
            while not self.validateMove(self.playerWhite, whiteMove):
                print("MOVE IS INVALID")
                print("WHITE'S TURN")
                whiteMove = self.playerWhite.getMove(self)
            self.movePiece(whiteMove)
            self.printBoard()

            print("BLACK'S TURN")
            blackMove = self.playerBlack.getMove(self)
            while not self.validateMove(self.playerBlack, blackMove):
                print("MOVE IS INVALID")
                print("BLACK'S TURN")
                blackMove = self.playerBlack.getMove(self)
            self.movePiece(blackMove)
            self.printBoard()

    def endGame(self):
        print('Winner is ' + self.winner)
        sys.exit()



#board = Board(False, False)
#game.printBoard()
#board.simulate()
