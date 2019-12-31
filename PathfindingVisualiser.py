import pygame

pygame.init()

gameWidth = 800
gameHeight = 600

cellSize = 20

gameDisplay = pygame.Surface((gameWidth,gameHeight))
screen = pygame.display.set_mode((gameWidth,gameHeight))

pygame.display.set_caption("Pathfinding")

clock = pygame.time.Clock()


class Cell():
    def __init__(self, x, y, cellSize):
        
        self.colour = (150,150,150)
        self.x = x
        self.y = y
        self.cellSize = cellSize
        
        self.isTerminal = False
        self.isWall = False
        
        self.value = 9999
        self.linearDistance = 9999
        self.isVisited = False
        self.previousCell = None
        
        
    #Resets the colour of the cell based on what its role
    def revertColour(self):
        if self.isWall:
            self.colour = (100,100,100)
        elif self.isTerminal:
            self.colour = (0,150,0)
        else:
            self.colour = (150,150,150)
        
    #Draws the cell onto the given display
    def draw(self, display):
        pygame.draw.rect(display,self.colour,[self.x,self.y,self.cellSize,self.cellSize])
        
    #Makes a cell a wall if it isn't a terminal cell, or resets it to normal
    def swapWall(self):
        if self.isWall:
            self.isWall = False
        elif not self.isTerminal:
            self.isWall = True
            
        self.revertColour()
        
    #Returns the linear distance from this cell to the target cell
    def getLinearCost(self, target):
        return abs(target.x//self.cellSize - self.x//self.cellSize) + abs(target.y//self.cellSize - self.y//self.cellSize)
            
    #Returns a list of cells adjacent to this cell within allCells (includes diagonal adjacencies)
    def getNeighbours(self, allCells):
        neighbours = []
        for cell in allCells:
            if not cell.isWall:
                for offset in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
                    if cell.x//self.cellSize == self.x//self.cellSize + offset[0] and cell.y//self.cellSize == self.y//self.cellSize + offset[1]:
                        neighbours.append(cell)
        return neighbours
        
    #Changes the colour of the cell, and attempts to backtrack from the previous cell
    def backtrack(self):
        if self.previousCell != None:
            self.previousCell.colour = (0,0,150)
            self.previousCell.backtrack()
        
    #Swaps the cell from terminal to non terminal or vice versa
    def swapTerminal(self):
        self.isTerminal = not self.isTerminal
        
        if self.isTerminal:
            if self.isWall:
                self.swapWall()
                
        self.revertColour()
        


def mainLoop():
    global cellSize
    global gameWidth
    global gameHeight
    
    isRunning = True
    
    for y in range(gameHeight//cellSize):
        for x in range(gameWidth//cellSize):
            cellSprites.append(Cell(x*cellSize,y*cellSize,cellSize))
            
    terminalCells = []
    
    pathfindingTick = 0
    
    isPathfinding = False
    
    while isRunning:
        
        #Handle inputs from the player
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    isRunning = False
                #Resets all the cell colours
                elif event.key == pygame.K_r and not isPathfinding:
                    for cell in cellSprites:
                        cell.revertColour()
                #Removes all walls
                elif event.key == pygame.K_c and not isPathfinding:
                    for cell in cellSprites:
                        if cell.isWall:
                            cell.swapWall()
                            cell.revertColour()
                #Start pathfinding
                elif event.key == pygame.K_p and len(terminalCells) == 2:
                    if isPathfinding:
                        isPathfinding = False
                        for cell in cellSprites:
                            cell.revertColour()
                    else:
                        isPathfinding = True
                        openCells = [terminalCells[0]]
                        #Initialise attributes for pathfinding purposes
                        for cell in cellSprites:
                            cell.previousCell = None
                            cell.pathCost = 9999
                            cell.totalCost = 9999
                            cell.predictedCost = cell.getLinearCost(terminalCells[1])
                            cell.revertColour()
                        terminalCells[0].pathCost = 0
           
        #Add walls
        if pygame.mouse.get_pressed()[0]:
            (mouseX, mouseY) = (cellSize*(pygame.mouse.get_pos()[0]//cellSize), cellSize*(pygame.mouse.get_pos()[1]//cellSize))

            for cell in cellSprites:
                if cell.x == mouseX and cell.y == mouseY and not cell.isWall:
                    cell.swapWall()
                    
        #Add terminal cells
        if pygame.mouse.get_pressed()[2]:
            (mouseX, mouseY) = (cellSize*(pygame.mouse.get_pos()[0]//cellSize), cellSize*(pygame.mouse.get_pos()[1]//cellSize))
                
            
            for cell in cellSprites:
                if cell.x == mouseX and cell.y == mouseY:
                    selectedCell = cell
                    break

            if selectedCell not in terminalCells:
                if len(terminalCells) >= 2:
                    #Ensure that there are only two terminal cells
                    oldestCell = terminalCells[0]
                    oldestCell.swapTerminal()
                    terminalCells.remove(oldestCell)
                    
                terminalCells.append(cell)
                selectedCell.swapTerminal()
            
            
        if isPathfinding and len(terminalCells) == 2:
            pathfindingTick += 1
            if pathfindingTick >= 2:
                pathfindingTick = 0
                
                if openCells != []:
                    nextSearchCell = openCells[0]
                    openCells.remove(nextSearchCell)
                    
                    #If we reach the end point, start backtracking
                    if nextSearchCell == terminalCells[1]:
                        isPathfinding = False
                        terminalCells[1].backtrack()

                    else:
                        for neighbour in nextSearchCell.getNeighbours(cellSprites):
                            potentialScore = nextSearchCell.pathCost + 1
                            
                            #If this path is shorter than this cell's current path, add it to the search list
                            if potentialScore < neighbour.pathCost:
                                neighbour.pathCost = potentialScore
                                neighbour.previousCell = nextSearchCell
                                neighbour.totalCost = potentialScore + neighbour.predictedCost
                                openCells.append(neighbour)
                                
                                neighbour.colour = (200,200,200)
                        
                        openCells.sort(key=lambda x: x.totalCost)
                else:
                    isPathfinding = False
                
                
        
        gameDisplay.fill((255,255,255))
        
        for cell in cellSprites:
            cell.draw(gameDisplay)
        
        screen.blit(gameDisplay, (0,0))
        clock.tick(120)
        pygame.display.update()
    
    
cellSprites = []

mainLoop()
pygame.quit()
quit()