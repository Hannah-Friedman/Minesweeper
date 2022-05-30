# "I hereby certify that this program is solely the result of my own work and 
# is in compliance with the Academic Integrity policy of the course syllabus 
# and the academic integrity policy of the CS department.”


# Instructions: Select a mode of difficulty and then click anywhere to begin.
# A left click will reveal a box and right click will place a flag at the box. 

import Draw
import random
import math
import time

GRID_SIZE = 16  # the size of the board according to how many boxes 
CELL_SIZE = 40  # the size of each box


# displays the start screen, which prompts the player to choose a mode
def startScreen():
    
    Draw.clear()
    
    Draw.setBackground(Draw.LIGHT_GRAY)
    # Displays the title of the game Minesweeper
    Draw.setColor(Draw.BLACK)
    Draw.setFontItalic(True)
    Draw.setFontSize(50)           
    Draw.string("Minesweeper", 175, 20)
    
    # sets the font for the rest od the words
    Draw.setFontSize(35)
    Draw.setFontItalic(False)
    Draw.setFontBold(False)
    Draw.setColor(Draw.WHITE)
    
    # draw the boxes indicating the different modes
    Draw.filledRect(210, 100, 200 ,100) # easy 
    Draw.filledRect(210, 270, 200 ,100) # medium
    Draw.filledRect(210, 450, 200 ,100) # hard
    
    # labels each box
    Draw.setColor(Draw.BLACK)
    Draw.string("EASY", 263, 130)
    Draw.string("MEDIUM", 237, 300)
    Draw.string("HARD", 261, 480)
 
    Draw.show() 


# creates a dictionary of randomly assigned rows and cols that are set to 1
# which indicated a "mine" is located there. 
def makeMines(numMines, rw, cl):
    
    mines = {}
    
    # add mines until there are numMines of tuples in the dictionary
    # numMines is determined by the difficulty level selected by the player
    while len(mines) < numMines:
        
        # generates a rondom integer to assign to a new row and col
        randRow = random.randint(0, GRID_SIZE-1)
        randCol = random.randint(0, GRID_SIZE-1)
        
        # make sure the generated row and col are not where the player clicked
        if (randRow != rw and randCol != cl):
            
            # make sure the generated row and col is not already in mines in order to avoid duplicates
            if (randRow,randCol) not in mines:
                
                # add the new tuple to the dictionary 
                mines[(randRow,randCol)] = 1
                
    return mines


# determines how many mines are touching the row and col given. The row and col
# are based of where the player clicked
def countAdjacentMines(row, col, mines):
    
    count = 0
    
    # loop through all the surounding boxes
    for rowOut in range(-1,2):
        for colOut in range(-1,2):
            newRow = row+rowOut
            newCol = col+colOut
            # add up all of the surrounding boxes containing mines
            if (newRow,newCol) in mines:
                count += 1
    return count


# draws a grid
def drawBoard():
    
    Draw.clear()
    
    # Every line is GRID_SIZE apart
    for i in range (0, GRID_SIZE * CELL_SIZE , CELL_SIZE):
        Draw.line(i,0, i, GRID_SIZE * CELL_SIZE )
        Draw.line(0,i,GRID_SIZE * CELL_SIZE ,i) 
        
    Draw.show()


# displays the number at the given row and col which was determind by countAdjacentMines()
def displayNumber(row, col, mines, revealed):
    
    numDisplayed = countAdjacentMines(row, col, mines)
    
    # turn every revealed box to a white sqaure 
    Draw.setColor(Draw.WHITE)
    Draw.filledRect(row*CELL_SIZE + 1, col*CELL_SIZE + 1 , CELL_SIZE -2 , CELL_SIZE- 2)
    
    Draw.setColor(Draw.BLACK)
    Draw.setFontSize(30)
    
    # display the number in the box, unless it's a 0
    if numDisplayed != 0:
        Draw.string(str(numDisplayed), row*CELL_SIZE + 11, col*CELL_SIZE + 4)
    
    # keep track of every box that the player uncovers
    revealed[(row,col)] = 1
    
    return numDisplayed


def playGame(numMines):
    
    firstClick = True
    
    flags = {} # a dictionary tracking the flags that were placed on the board
    
    revealed = {} # a dictionary keeping track of the spaces on the board 
    # that have already been "revealed" by the user 
    # meaning their number is being displayed
    
    drawBoard()
    
    gameOver = False
    
    # while the player has not lost 
    while not gameOver:
        if Draw.mousePressed(): 
            x = Draw.mouseX()
            y = Draw.mouseY()
            
            # convert the x and y coordinates of the users click into rows and cols
            row = x // CELL_SIZE
            col = y // CELL_SIZE 
            
            
            if Draw.mouseRight():
                
                # if there was already a flag present, than erase and remove that flag
                if (row,col) in flags:
                    
                    # color over the flag
                    Draw.setColor(Draw.LIGHT_GRAY)
                    Draw.filledRect(row*CELL_SIZE + 1, col*CELL_SIZE + 1 , CELL_SIZE -2 , CELL_SIZE- 2)
                    
                    del flags[row,col]
                    
                else:
                    # if there was no flag present and the row and col are an unrevealed square
                    # then draw a flag and add it to the flags dictionary
                    if (row,col) not in revealed:
                        Draw.picture("flag.gif", row*CELL_SIZE + 5, col*CELL_SIZE + 5)
                        flags[row,col] = 1 
    
            else: # if it was not a right click
                
                if firstClick:
                    # if it was the first click of the game, call makeMines()
                    firstClick = False
                    mines = makeMines(numMines, row, col)
                    
                    
                    # the first click reveals the clicked box, all surounding boxes 
                    # and any boxes around a blank labeled box 
                    que = [(row,col)]
            
                    # while que is not empty 
                    while len(que) > 0:
                        tup = que[0]
                        
                        # loop through and reveal all the surrounding boxes
                        for rowOut in range(-1,2):
                            for colOut in range(-1,2):
                                
                                # calculate using the current row and col to refer to the surrounding boxes   
                                newRow =  tup[0] + rowOut
                                newCol = tup[1] + colOut
                                
                                # if the box is valid (meaning, it's in the bounds of the grid, 
                                # and it's not in mines and it has not already been revealed) then reveal it
                                if newRow >= 0 and newRow < GRID_SIZE and newCol >= 0 and newCol < GRID_SIZE and \
                                   (newRow, newCol) not in mines and (newRow, newCol) not in revealed:
                                    
                                    num = displayNumber(newRow, newCol, mines, revealed)
                                    
                                    # if the revealed number in the box is 0, add it to the que
                                    # in order to reveal its surrounding boxes
                                    if num == 0:
                                        que.append((newRow,newCol))
                        del que[0] 
                            
                            
                # if it wasn't the first click, and a box where a mine was located was clicked, 
                # then the game is over   
                elif (row,col) in mines and (row,col) not in flags:
                    
                    # gameOver = True
                    Draw.clear()
                    
                    Draw.setColor(Draw.BLACK)
                    Draw.setFontSize(50)
                    Draw.string("GAME OVER!", 150, 270)
                    Draw.setFontSize(18)
                    Draw.string("Better Luck Next Time", 230, 330)
                    
                    Draw.show()
                    time.sleep(1.5)
                    
                    return # start game over
                
                
                else:
                    # if there is no mine and no flag located at the box,
                    # display the number of mines surrounding that box
                    if (row,col) not in flags:
                        displayNumber(row, col, mines, revealed)
            
            
            # if all of the possible spaces have been revealed, then the user has won
            if len(revealed) == ( (GRID_SIZE**2) - numMines):
                Draw.clear()
                
                Draw.setColor(Draw.BLACK)
                Draw.setFontSize(50)
                Draw.string("YOU WON!", 190, 290)
                Draw.setFontSize(18)
                Draw.string("Nice job!", 283, 342)               
                
                Draw.show()
                time.sleep(1.5)
                return # start game over
                  

def main():
    # display the background
    Draw.setCanvasSize(GRID_SIZE * CELL_SIZE ,GRID_SIZE * CELL_SIZE )
    
    easyMode = 45
    mediumMode = 55
    hardMode = 65 
    
    # determines the mode chosen, and begins the game
    while True:
        if Draw.mousePressed():
            
            x = Draw.mouseX()
            y = Draw.mouseY()
        
            # if the easy button was selected...
            if x > 210 and x < 410 and y > 100 and y < 200:
                playGame(easyMode)
            
            # if the medium button was selected...
            elif x > 210 and x < 410 and y > 270 and y < 370:
                playGame(mediumMode)
                
            # if the hard button was selected...
            elif x > 210 and x < 410 and y > 450 and y < 550:
                playGame(hardMode)
                
        startScreen()
        
main()