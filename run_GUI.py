import pygame
import chess
#from multiprocessing import Process
import _thread
import sys


def render(screen):
    screen.fill(BLACK)
    renderBoard(screen)
    for piece in board.boardPieces:
        renderPiece(piece, screen)
    pygame.display.flip()

def renderBoard(screen):
    count = 1
    for i in range(1, numBlocksHorz - 1):
        for j in range(1, numBlocksVert - 1):
            if count % 2 == 0:
                pygame.draw.rect(screen, BLUE, pygame.Rect(i * blockSize[0], j * blockSize[1], blockSize[0], blockSize[1]))
            else:
                pygame.draw.rect(screen, WHITE, pygame.Rect(i * blockSize[0], j * blockSize[1], blockSize[0], blockSize[1]))
            count+=1
        count+=1

def renderPiece(piece, screen):
    if piece.getColorSymbol() == 'W':
        if piece.getSymbol() == 'P':
            image = wpawn
        if piece.getSymbol() == 'N':
            image = wknight
        if piece.getSymbol() == 'B':
            image = wbishop
        if piece.getSymbol() == 'R':
            image = wrook
        if piece.getSymbol() == 'Q':
            image = wqueen
        if piece.getSymbol() == 'K':
            image = wking
    else:
        if piece.getSymbol() == 'P':
            image = bpawn
        if piece.getSymbol() == 'N':
            image = bknight
        if piece.getSymbol() == 'B':
            image = bbishop
        if piece.getSymbol() == 'R':
            image = brook
        if piece.getSymbol() == 'Q':
            image = bqueen
        if piece.getSymbol() == 'K':
            image = bking
    image = pygame.transform.scale(image, (int(blockSize[0]), int(blockSize[1])))
    rowNum = numBlocksVert - piece.pos.row - 1
    colLet = piece.pos.col
    xPos = rowNum * blockSize[0]
    yPos = (board.getColNum(colLet) + 1) * blockSize[1]
    screen.blit(image, (yPos, xPos))

def checkInput():
    pos = pygame.mouse.get_pos()
    #rowNum = numBlocksVert - int(pos[1] / blockSize[0]) - 1
    if (numBlocksVert - int(pos[1] / blockSize[0]) - 1) in range(1, 9):
        rowNum = numBlocksVert - int(pos[1] / blockSize[0]) - 1
    else:
        rowNum = 'unknown'
    if int(pos[0] / blockSize[1]) in range(1, 9):
        colLet = board.boardCols[int(pos[0] / blockSize[1]) - 1]
    else:
        colLet = 'unknown'

    if(rowNum == 'unknown' or colLet == 'unknown'):
        pass
    else:
        pressed = pygame.mouse.get_pressed()
        if pressed[0]:
            startPos = chess.Position(colLet, rowNum)
            print(colLet)
            print(rowNum)

    #pressed =  pygame.mouse.get_pressed()
    #if pressed[0]:
    #    print('YEYEYE')



def simulate():
    board.printBoard()
    while(board.winner is None):
        print("WHITE'S TURN")
        whiteMove = board.playerWhite.getMove(board)
        while not board.validateMove(board.playerWhite, whiteMove):
            print("MOVE IS INVALID")
            print("WHITE'S TURN")
            whiteMove = board.playerWhite.getMove(board)
        board.movePiece(whiteMove)
        board.printBoard()

        print("BLACK'S TURN")
        blackMove = board.playerBlack.getMove(board)
        while not board.validateMove(board.playerBlack, blackMove):
            print("MOVE IS INVALID")
            print("BLACK'S TURN")
            blackMove = board.playerBlack.getMove(board)
        board.movePiece(blackMove)
        board.printBoard()

def loop():
    global blockSize
    #Main game loop
    stop = False
    while not stop:
        for event in pygame.event.get():
            #Close window when close button is clicked
            if event.type == pygame.QUIT:
                stop = True

            elif event.type == pygame.VIDEORESIZE:
                scrsize = event.size
                sW = event.w
                sH = event.h
                blockSize = (int(sW/numBlocksHorz), int(sH/numBlocksVert))
                #screen = pygame.display.set_mode(scrsize,RESIZABLE)
                #changed = True

        checkInput()
        render(screen)
        #Set fps
        clock.tick(10)

    pygame.quit()
    sys.exit(0)


#Get sprites
IMGDIR = 'assets'
wpawn = pygame.image.load(IMGDIR + '/wpawn.png')
wbishop = pygame.image.load(IMGDIR + '/wbishop.png')
wknight = pygame.image.load(IMGDIR + '/wknight.png')
wrook = pygame.image.load(IMGDIR + '/wrook.png')
wqueen = pygame.image.load(IMGDIR + '/wqueen.png')
wking = pygame.image.load(IMGDIR + '/wking.png')

bpawn = pygame.image.load(IMGDIR + '/bpawn.png')
bbishop = pygame.image.load(IMGDIR + '/bbishop.png')
bknight = pygame.image.load(IMGDIR + '/bknight.png')
brook = pygame.image.load(IMGDIR + '/brook.png')
bqueen = pygame.image.load(IMGDIR + '/bqueen.png')
bking = pygame.image.load(IMGDIR + '/bking.png')

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 140)


pygame.init()
pygame.font.init()

#Initialize global variables
sW = 500
sH = 500
numBlocksHorz = 10
numBlocksVert = 10
blockSize = (sW/numBlocksHorz, sH/numBlocksVert)
clock = pygame.time.Clock()

#Start window
screen = pygame.display.set_mode((sW, sH))
#screen = pygame.display.set_mode((sW, sH), pygame.RESIZABLE)
pygame.display.set_caption('Chess')
#pygame.display.set_icon(wpawn)

board = chess.Board(False, False)



_thread.start_new_thread(simulate,())
loop()
