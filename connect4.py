import pygame,sys,math
import numpy as np

ROW_COUNT=6
COLUMN_COUNT=7

COLOR_BLUE=(0,0,255)
COLOR_RED=(255,0,0)
COLOR_GREEN=(0,255,0)
COLOR_BLACK=(0,0,0)

"""game functions"""
def create_board():
    board=np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def is_valid_position(board,col):
    #minusing 1 because list starts from 0
    return board[ROW_COUNT-1][col]==0

def drop_piece(board,row,col,piece):
    board[row][col]=piece

def get_next_row(board,col):
    for r in range(ROW_COUNT):
        if board[r][col]==0:
            return r
    
def print_board():
    print(np.flip(board,0))
    
def winning_move(board,piece):
    """checking horizontal locations"""
    #minusing 3 because if we match 4 color then 3 remained unmathced
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True

    """checking vertical location"""
    for c in range(COLUMN_COUNT):
    #minusing 3 because if we match 4 color then 3 remained unmathced
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True
    
    """checking postively sloped diaganols"""
    #minusing 3 because if we match 4 color then 3 remained unmathced
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True
    
    """checking negatively sloped diaganols"""
    #minusing 3 because if we match 4 color then 3 remained unmathced
    for c in range(COLUMN_COUNT-3):
        for r in range(3,ROW_COUNT):#because it started from 3th row and cell index is decreasing
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:#minus because of bcackward index down
                return True
    
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            #pygame.draw.rect(screen,color,(x,y,width,height))
            pygame.draw.rect(screen,COLOR_BLUE,(c*SQUARE_SIZE,r*SQUARE_SIZE+SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
            pygame.draw.circle(screen,COLOR_BLACK,(int(c*SQUARE_SIZE+SQUARE_SIZE/2),int(r*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)),RADIOUS)#+SQUARESIZE/2 is to keep some space with round from screen

    
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c]==1:
                #pygame.draw.circle(screen,color,position,radious)
                pygame.draw.circle(screen,COLOR_RED,(int(c*SQUARE_SIZE+SQUARE_SIZE/2),height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)),RADIOUS)
            #minusing from height because of the filling of last row
            elif board[r][c]==2:
                pygame.draw.circle(screen,COLOR_GREEN,(int(c*SQUARE_SIZE+SQUARE_SIZE/2),height-int(r*SQUARE_SIZE+SQUARE_SIZE/2)),RADIOUS)
                
                
    # pygame.display.update()
                
    
"""pygame setting up"""
pygame.init()

"""game objectt"""
SQUARE_SIZE=85
RADIOUS=int(SQUARE_SIZE/2-5)

width=COLUMN_COUNT*SQUARE_SIZE
height=(ROW_COUNT+1)*SQUARE_SIZE# +1 for the extra space
size=(width,height)

screen=pygame.display.set_mode(size)
    
"""it is for showing board to begin"""
board=create_board()
draw_board(board)
# pygame.display.update()

myfont=pygame.font.SysFont('monospace',60)

game_over=False
turn=0

while not game_over:
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()
            
        if event.type==pygame.MOUSEMOTION:
            pygame.draw.rect(screen,COLOR_BLACK,(0,0,width,SQUARE_SIZE))#this is for filling space with black to prevent being all red
            posx=event.pos[0]
            """adding ball in space"""
            if turn==0:
                pygame.draw.circle(screen,COLOR_RED,(posx,int(SQUARE_SIZE/2)),RADIOUS)
            else:
                pygame.draw.circle(screen,COLOR_GREEN,(posx,int(SQUARE_SIZE/2)),RADIOUS)
        
            
        if event.type==pygame.MOUSEBUTTONDOWN:
            # print(event.pos)
            pygame.draw.rect(screen,COLOR_BLACK,(0,0,width,SQUARE_SIZE))
            if turn==0:
                posx=event.pos[0]
                col=int(math.floor(posx/SQUARE_SIZE))
                # col=int(input('Player 1 (0-6):'))-1
                if is_valid_position(board,col):
                    row=get_next_row(board,col)
                    drop_piece(board,row,col,1)
                    
                    if winning_move(board,1):
                        
                        label=myfont.render('Player 1 wins!!!',1,COLOR_RED)
                        screen.blit(label,(40,10))
                        
                        
                        game_over=True
                
            else:
                posx=event.pos[0]                
                col=int(math.floor(posx/SQUARE_SIZE))

                # col=int(input('Player 2 (0-6):'))-1
                if is_valid_position(board,col):
                    row=get_next_row(board,col)
                    drop_piece(board,row,col,2)
                
                    if winning_move(board,2):
                        # print('Player 2 wins')
                        
                        label=myfont.render('Player 1 wins!!!',1,COLOR_GREEN)
                        screen.blit(label,(40,10))
                        
                        
                        game_over=True
                        
            
            # print_board()
            draw_board(board)
            
            turn+=1
            turn%=2
    
    pygame.display.update()
    
    if game_over:
        pygame.time.wait(3000)#miliseconds
