import pygame

pygame.init()

gameWidth = 800
gameHeight = 600
buffer = 125

cellSize = 20

gameDisplay = pygame.Surface((gameWidth,gameHeight+buffer))
screen = pygame.display.set_mode((gameWidth,gameHeight+buffer))

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
        
    def makeWall(self):
        if not self.isTerminal:
            self.isWall = True
            self.revertColour()
            
    def removeWall(self):
        self.isWall = False
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
        

        
class Button():
    def __init__(self, x, y, width, height, text, font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.isActive = False
        
        self.text = text
        self.font = font
        
        
    def draw(self, display):
        if self.isActive:
            colour = (20,200,20)
        else:
            colour = (200,20,20)
            
        pygame.draw.rect(display,colour,[self.x, self.y, self.width, self.height])
        
        text=font.render(self.text, 1,(0,0,0))
        display.blit(text,(self.x+5,self.y+15))
        
        
        
    def mouseClick(self, mousePos):
        if mousePos[0] >= self.x and mousePos[0] <= self.x + self.width and mousePos[1] >= self.y and mousePos[1] <= self.y + self.height:
            self.isActive = True
            return self.text
        return False
        

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
    
    #Create and add buttons
    buttons = []
    buttons.append(Button(0,gameHeight,gameWidth/4.1, 75, "Draw Wall", font))
    buttons[0].isActive = True
    buttons.append(Button(gameWidth/4,gameHeight,gameWidth/4.1, 75, "Rem. Wall", font))
    buttons.append(Button(2*gameWidth/4,gameHeight,gameWidth/4.1, 75, "Set Start/End", font))
    buttons.append(Button(3*gameWidth/4,gameHeight,gameWidth/4.1, 75, "Reset", font))
    
    mouseState = "Draw Wall"
    
    while isRunning:
        
        #Handle inputs from the player
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                isRunning = False
                
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
            
            #Button logic
            for button in buttons:
                if button.mouseClick(pygame.mouse.get_pos()) != False:
                    mouseState = button.mouseClick(pygame.mouse.get_pos())
                    if mouseState == "Reset":
                        button.isActive = False
                        isPathfinding = False
                        for cell in cellSprites:
                            cell.revertColour()
                    else:
                        for otherButton in buttons:
                            if otherButton != button:
                                otherButton.isActive = False
                    break
            
            #Drawing/Removing Walls
            (mouseX, mouseY) = (cellSize*(pygame.mouse.get_pos()[0]//cellSize), cellSize*(pygame.mouse.get_pos()[1]//cellSize))

            for cell in cellSprites:
                if cell.x == mouseX and cell.y == mouseY:
                    if mouseState == "Draw Wall":
                        cell.makeWall()
                    elif mouseState == "Rem. Wall":
                        cell.removeWall()
                    
            #Adding terminal cells
            if mouseState == "Set Start/End":
                (mouseX, mouseY) = (cellSize*(pygame.mouse.get_pos()[0]//cellSize), cellSize*(pygame.mouse.get_pos()[1]//cellSize))

                selectedCell = None
                for cell in cellSprites:
                    if cell.x == mouseX and cell.y == mouseY:
                        selectedCell = cell
                        break

                if selectedCell != None and selectedCell not in terminalCells:
                    if len(terminalCells) >= 2:
                        #Ensure that there are only two terminal cells
                        oldestCell = terminalCells[0]
                        oldestCell.swapTerminal()
                        terminalCells.remove(oldestCell)

                    terminalCells.append(cell)
                    selectedCell.swapTerminal()
            
            
        #A* Algorithm
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
                            
                            distX = abs(neighbour.x//nextSearchCell.cellSize - nextSearchCell.x//nextSearchCell.cellSize)
                            distY = abs(neighbour.y//nextSearchCell.cellSize - nextSearchCell.y//nextSearchCell.cellSize)
                            
                            if  distX + distY > 1:
                                potentialScore = nextSearchCell.pathCost + 1.4
                            
                            
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
        
        text=font.render("Press 'p' to begin pathfinding", 1,(0,0,0))
        gameDisplay.blit(text,(5,gameHeight+buffer-25))
        text=font.render("Press 'c' to clear all walls", 1,(0,0,0))
        gameDisplay.blit(text,(5,gameHeight+buffer-50))
        
        for cell in cellSprites:
            cell.draw(gameDisplay)
            
        for button in buttons:
            button.draw(gameDisplay)
        
        screen.blit(gameDisplay, (0,0))
        clock.tick(120)
        pygame.display.update()
 
font=pygame.font.Font('ReturnOfGanon.ttf',16)
    
cellSprites = []

mainLoop()
pygame.quit()
quit()