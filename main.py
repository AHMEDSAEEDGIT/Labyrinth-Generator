import sys
import pygame
from random import choice

#constants
RES = WIDTH , HEIGHT = 1202 , 902
TILE = 40
COLS,ROWS =WIDTH//TILE ,HEIGHT //TILE
RUNNING = True


#Intitialise pygame# Initialize Pygame
pygame.init()

# Create the window
sc = pygame.display.set_mode(RES)
pygame.display.set_caption("Labyrinth") 

# Create a clock object to control the frame rate
Clock = pygame.time.Clock()



# cell class
class Cell:

    # Cell parameterised ctor 
    def __init__(self , x , y):
        self.X ,self.Y = x , y
        # dictionary of the walls for each cell
        self.Walls = {'Top' : True , 'Right' : True , 'Bottom' : True , 'Left' : True}
        self.Visited = False

    def DrawCurrentCell(self):
        x,y = self.X*TILE , self.Y * TILE
        pygame.draw.rect(sc,pygame.Color('saddlebrown'),(x+2,y+2,TILE-2,TILE-2))

    def Draw(self):
        x,y = self.X * TILE,self.Y * TILE
        # Colorize the cell with black
        if self.Visited:
            pygame.draw.rect(sc,pygame.Color('black') ,(x , y ,TILE , TILE))

        # Draw the borders
        if self.Walls['Top'] :
            pygame.draw.line(sc,pygame.Color('darkorange') ,(x,y) , (x+TILE , y),2)
        if self.Walls['Right'] :
            pygame.draw.line(sc,pygame.Color('darkorange') ,(x+TILE,y) , (x+TILE , y+TILE),2)
        if self.Walls['Bottom'] :
            pygame.draw.line(sc,pygame.Color('darkorange') ,(x+TILE , y+TILE) , (x, y+TILE ),2)
        if self.Walls['Left'] :
            pygame.draw.line(sc,pygame.Color('darkorange') ,(x,y+TILE) , (x , y),2)

    # break the wall between two cells just by not drawing two lines for each cell
    @staticmethod
    def BreakWalls(current , next):
        #           (x,y-1)     
        # (x-1,y)    (x,y)    (x+1 ,y)
        #           (x,y+1)
        
        #There are two walls for each cell so we check based on the difference
        dx = current.X - next.X
        # in case of moving to thr right or left neighbor
        if dx == 1:
            current.Walls ['Left'] = False
            next.Walls['Right'] = False

        if dx == -1 :
            current.Walls['Right']=False 
            next.Walls['Left'] = False

        dy = current.Y - next.Y
        # in case of moving to thr Top or bottom neighbor
        if dy == 1:
            current.Walls ['Top'] = False
            next.Walls['Bottom'] = False

        if dy == -1 :
            current.Walls['Bottom']=False 
            next.Walls['Top'] = False
    

    # Returns Current Cell index in the 1D list if it is valid otherwise return false
    def CheckCell(self , x ,y):
        # if the cooridnates out of the maze boundires terminate
        if x < 0 or x > COLS-1 or y < 0 or y >ROWS-1 :
            return False
        
        # Lambda expression (function) that takes two input param x , y and returns the cell Index in 1D array
        GetIndex = lambda x,y : x + y * COLS
        return grid_cells[GetIndex(x,y)]
    
    
    # check each neighbor if valid and randomly pick one between them if they are not visited
    def CheckNeighbors (self):
        neighbors = []
        # Check if each neighbor is valid 
        top = self.CheckCell(self.X , self.Y-1)
        right = self.CheckCell(self.X +1 , self.Y)
        bottom = self.CheckCell(self.X  , self.Y+1)
        left = self.CheckCell(self.X -1 , self.Y)

        # Check if each neighbor not vistied and append it to neighbors list
        if top and not top.Visited :
            neighbors.append(top)
        if right and not right.Visited :
            neighbors.append(right)
        if bottom and not bottom.Visited :
            neighbors.append(bottom)
        if left and not left.Visited :
            neighbors.append(left)
        
        # Randomly pick one
        return choice(neighbors) if neighbors else False





# Iterate over each cell using list comprehension nested loop and append them into 1D List
grid_cells = [Cell(col,row) for row in range(ROWS) for  col in range(COLS) ]
#get first cell (current Cell)
CurrentCell = grid_cells[0]
#Stack for DFS
stack = []

   


while RUNNING :
    sc.fill(pygame.Color('darkslategray'))
    # if the window is closed
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
    
    # Draw each not visted cell with 
    [cell.Draw() for cell in grid_cells]
    # Mark current cell as visited to start exploring its neighbors
    CurrentCell.Visited=True
    # Colorize it with different color thant the not visited ones
    CurrentCell.DrawCurrentCell()

    NextCell = CurrentCell.CheckNeighbors()
    if NextCell:
        NextCell.Visited = True
        Cell.BreakWalls(CurrentCell , NextCell)
        stack.append(CurrentCell)
        CurrentCell=NextCell
    elif stack:
        CurrentCell = stack.pop()

    pygame.display.flip()
    Clock.tick(40)



pygame.quit()
sys.exit()