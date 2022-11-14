import pygame as p
from ChessEngine import GameState
import ChessEngine
import random
#Dimensions
WIDTH = HEIGHT = 512
DIMENSION = 8 #8x8 chess board
SQ_SIZE = HEIGHT // DIMENSION #Square size is equal to the height divided by dimension
MAX_FPS = 15 #For animations
IMAGES = {}
 
'''Loading images initialize a global dictionary of images. 
This will be called once to save time'''

def loadImages():
    pieces = ["wp", "wR", "wB", "wN", "wQ", "wK", "bp", "bR", "bN", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE)) #Finds the images

'''
Handle user input and update graphics
'''

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    loadImages() #Only load the images once!
    running = True
    sqselected = () #No square is selected initially
    playerclicks = [] #keeps track of the clicks
    validMoves = gs.getValidMoves()
    moveMade = False

    while running:
        
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                
                location = p.mouse.get_pos() #Gets the (x,y) position of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqselected == (row, col):
                    enginemove = random.choice(gs.getValidMoves())
                    print("Engine best move!:" + str(enginemove.moveID)) #If the user clicked on the square twice (Usually means deselect)
                    sqselected = () #Deselect the piece
                    playerclicks = []
                else:
                    sqselected = (row, col)
                    playerclicks.append(sqselected)
                if len(playerclicks) == 2:
                    move = ChessEngine.Move(playerclicks[0], playerclicks[1], gs.board)
                    print(move.getChessNotation())
                    
                    for moves in validMoves:
                        if move.moveID == moves.moveID:
                            gs.makeMove(move)
                            moveMade = True
                    else:
                        pass
                    
                    sqselected = () #Reset user clicks
                    playerclicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            

        drawGameState(screen,gs)
        clock.tick(MAX_FPS)
        p.display.flip()
        
'''
Remember to draw pieces after drawing the board
'''
def drawGameState(screen, gs):
    drawBoard(screen) #This function draws the squares on the board
    #Remember to add in move suggestions
    drawPieces(screen, gs.board) #draws pieces on the top of the squares

def drawBoard(screen): #Draws squares on the board
    colors = [p.Color("white"), p.Color("dark green")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j) % 2)]
            p.draw.rect(screen, color, p.Rect(j*SQ_SIZE, i*SQ_SIZE, SQ_SIZE, SQ_SIZE))
            

def drawPieces(screen, board): #Draws the pieces on the baord using the current GameState
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

if __name__ == "__main__":
    main()
