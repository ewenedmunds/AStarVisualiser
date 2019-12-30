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
        
    def revertColour(self):
        if self.isWall:
            self.colour = (100,100,100)
        elif self.isTerminal:
            self.colour = (0,150,0)
        else:
            self.colour = (150,150,150)
        
    def draw(self, display):
        pygame.draw.rect(display,self.colour,[self.x,self.y,self.cellSize,self.cellSize])
        
    def swapWall(self):
        if self.isWall:
            self.isWall = False
            self.colour = (150,150,150)
        elif not self.isTerminal:
            self.isWall = True
            self.colour = (100,100,100)
            
    def getLinearCost(self, target):
        return abs(target.x//self.cellSize - self.x//self.cellSize) + abs(target.y//self.cellSize - self.y//self.cellSize)
            
    def getNeighbours(self, allCells):
        neighbours = []
        for cell in allCells:
            if not cell.isWall:
                for offset in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
                    if cell.x//self.cellSize == self.x//self.cellSize + offset[0] and cell.y//self.cellSize == self.y//self.cellSize + offset[1]:
                        neighbours.append(cell)
        return neighbours
        
    def backtrack(self):
        if self.previousCell != None:
            self.previousCell.colour = (0,0,150)
            self.previousCell.backtrack()
        
    def swapTerminal(self):
        self.isTerminal = not self.isTerminal
        
        if self.isTerminal:
            if self.isWall:
                self.swapWall()
            self.colour = (0,150,0)
            
        else:
            self.colour = (150,150,150)
        


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
        
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    isRunning = False
                elif event.key == pygame.K_r and not isPathfinding:
                    for cell in cellSprites:
                        cell.revertColour()
                elif event.key == pygame.K_c and not isPathfinding:
                    for cell in cellSprites:
                        if cell.isWall:
                            cell.swapWall()
                            cell.revertColour()
                elif event.key == pygame.K_p and len(terminalCells) == 2:
                    if isPathfinding:
                        isPathfinding = False
                        for cell in cellSprites:
                            cell.revertColour()
                    else:
                        isPathfinding = True
                        openCells = [terminalCells[0]]
                        for cell in cellSprites:
                            cell.previousCell = None
                            cell.pathCost = 9999
                            cell.totalCost = 9999
                            cell.predictedCost = cell.getLinearCost(terminalCells[1])
                            cell.revertColour()
                        terminalCells[0].pathCost = 0
           
        
        if pygame.mouse.get_pressed()[0]:
            (mouseX, mouseY) = (cellSize*(pygame.mouse.get_pos()[0]//cellSize), cellSize*(pygame.mouse.get_pos()[1]//cellSize))

            for cell in cellSprites:
                if cell.x == mouseX and cell.y == mouseY and not cell.isWall:
                    cell.swapWall()
                    
        if pygame.mouse.get_pressed()[2]:
            (mouseX, mouseY) = (cellSize*(pygame.mouse.get_pos()[0]//cellSize), cellSize*(pygame.mouse.get_pos()[1]//cellSize))
                
            
            
            for cell in cellSprites:
                if cell.x == mouseX and cell.y == mouseY:
                    selectedCell = cell
                    break

            if selectedCell not in terminalCells:
                if len(terminalCells) >= 2:
                    oldestCell = terminalCells[0]
                    oldestCell.swapTerminal()
                    terminalCells.remove(oldestCell)
                    
                terminalCells.append(cell)
                selectedCell.swapTerminal()
            
            
        if isPathfinding and len(terminalCells) == 2:
            pathfindingTick += 1
            if pathfindingTick >= 1:
                pathfindingTick = 0
                
                if openCells != []:
                    nextSearchCell = openCells[0]
                    openCells.remove(nextSearchCell)
                    
                    if nextSearchCell == terminalCells[1]:
                        isPathfinding = False
                        terminalCells[1].backtrack()
                    else:
                        for neighbour in nextSearchCell.getNeighbours(cellSprites):
                            potentialScore = nextSearchCell.pathCost + 1
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