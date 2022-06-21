from random import randint
import threading
from time import sleep
from tkinter import *

intWidth = 30
intHeight = 30

maze = []
for i in range(intHeight*2+1):
    row = []
    for i in range(intWidth*2+1):
        row.append("■")
    maze.append(row)

canvas = None
cellSize = 10
borderSize  = 5

def show():
    ventana = Tk()
    ventana.title('Maze Generation')     
    h = intHeight * cellSize + (intHeight + 1) * borderSize
    w = intWidth * cellSize + (intWidth + 1) * borderSize
    global canvas
    canvas = Canvas(ventana, bg="black", height=h, width=w)
    canvas.pack()
    ventana.bind("<space>", callback)
    ventana.mainloop()

def printMaze():
    strText = ""
    for row in maze:
        for cell in row:
            strText += cell + "  "
        strText += "\n"
    print(strText)
    
def getCellWallsFrom(tuple):
    row = tuple[0]
    column = tuple[1]
    walls = []
    #up
    if row>0:
        if maze[row*2+1-2][column*2+1] != " ":
            walls.append(((row, column),(row - 1, column)))
    #right
    if column < intWidth-1:
        if maze[row*2+1][column*2+1+2] != " ":
            walls.append(((row, column),(row, column+1)))
    #down
    if row < intHeight-1:
        if maze[row*2+1+2][column*2+1] != " ":
            walls.append(((row, column),(row+1, column)))
    #left
    if column > 0:
        if maze[row*2+1][column*2+1-2] != " ":
            walls.append(((row, column),(row, column-1)))
    return(walls)

def markCell(tuple):    
    row = tuple[0] * 2 + 1 
    column = tuple[1] * 2 + 1
    maze[row][column] = " "
    row = (borderSize+cellSize)*tuple[0] + borderSize
    column = (borderSize+cellSize)*tuple[1] + borderSize
    #For GUI    
    canvas.create_rectangle(column, row, column+cellSize, row+cellSize, outline="", fill="white")

step = False

def setStartEndCell():
    cells = [(0,0),(intHeight-1, intWidth-1)]
    for tuple in cells:
        row = tuple[0] * 2 + 1 
        column = tuple[1] * 2 + 1
        maze[row][column] = " "
        row = (borderSize+cellSize)*tuple[0] + borderSize
        column = (borderSize+cellSize)*tuple[1] + borderSize
        #For GUI
        canvas.create_rectangle(column, row, column+cellSize, row+cellSize, outline="", fill="red")

def makeGap(wall):
    cell1 = wall[0]
    cell2 = wall[1]
    rowOp = cell2[0] - cell1[0]
    colOp = cell2[1] - cell1[1]
    row = cell1[0] * 2 + 1 + rowOp
    column = cell1[1] * 2 + 1 + colOp
    maze[row][column] = " "
    #For GUI
    row = (borderSize+cellSize)*cell1[0] + borderSize + rowOp * cellSize 
    column = (borderSize+cellSize)*cell1[1] + borderSize + colOp * cellSize
    canvas.create_rectangle(column, row, column+cellSize, row+cellSize, outline="", fill="white")
    if step:
        sleep(delay)

def addNewWalls(newWalls):
    global walls
    walls += newWalls
    for wall in newWalls:
        cell1 = wall[0]
        cell2 = wall[1]
        rowOp = cell2[0] - cell1[0]
        colOp = cell2[1] - cell1[1]
        row = cell1[0] * 2 + 1 + rowOp
        column = cell1[1] * 2 + 1 + colOp
        #For GUI
        if step:
            row = (borderSize+cellSize)*cell1[0] + borderSize + rowOp * cellSize 
            column = (borderSize+cellSize)*cell1[1] + borderSize + colOp * cellSize        
            color = "#F00"
            if rowOp > 0:
                canvas.create_rectangle(column, row, column+cellSize, row+borderSize, outline="", fill=color)
            elif rowOp < 0:
                canvas.create_rectangle(column, row+cellSize-borderSize, column+cellSize, row+cellSize, outline="", fill=color)
            elif colOp > 0:
                canvas.create_rectangle(column, row, column+borderSize, row+cellSize, outline="", fill=color)
            elif colOp < 0:
                canvas.create_rectangle(column+cellSize-borderSize, row, column+cellSize, row+cellSize, outline="", fill=color)

def removeWall(wall):
    walls.remove(wall)
    cell1 = wall[0]
    cell2 = wall[1]
    rowOp = cell2[0] - cell1[0]
    colOp = cell2[1] - cell1[1]
    row = cell1[0] * 2 + 1 + rowOp
    column = cell1[1] * 2 + 1 + colOp
    #For GUI 
    if step:  
        if(maze[row][column] != " "):        
            row = (borderSize+cellSize)*cell1[0] + borderSize + rowOp * cellSize 
            column = (borderSize+cellSize)*cell1[1] + borderSize + colOp * cellSize        
            color = "#000"
            if rowOp > 0:
                canvas.create_rectangle(column, row, column+cellSize, row+borderSize, outline="", fill=color)
            elif rowOp < 0:
                canvas.create_rectangle(column, row+cellSize-borderSize, column+cellSize, row+cellSize, outline="", fill=color)
            elif colOp > 0:
                canvas.create_rectangle(column, row, column+borderSize, row+cellSize, outline="", fill=color)
            elif colOp < 0:
                canvas.create_rectangle(column+cellSize-borderSize, row, column+cellSize, row+cellSize, outline="", fill=color)
        sleep(delay)

def paintSelectedWall(wall):
    cell1 = wall[0]
    cell2 = wall[1]
    rowOp = cell2[0] - cell1[0]
    colOp = cell2[1] - cell1[1]
    row = cell1[0] * 2 + 1 + rowOp
    column = cell1[1] * 2 + 1 + colOp
    if step:
        row = (borderSize+cellSize)*cell1[0] + borderSize + rowOp * cellSize 
        column = (borderSize+cellSize)*cell1[1] + borderSize + colOp * cellSize        
        color = "#0F0"
        if rowOp > 0:
            canvas.create_rectangle(column, row, column+cellSize, row+borderSize, outline="", fill=color)
        elif rowOp < 0:
            canvas.create_rectangle(column, row+cellSize-borderSize, column+cellSize, row+cellSize, outline="", fill=color)
        elif colOp > 0:
            canvas.create_rectangle(column, row, column+borderSize, row+cellSize, outline="", fill=color)
        elif colOp < 0:
            canvas.create_rectangle(column+cellSize-borderSize, row, column+cellSize, row+cellSize, outline="", fill=color)

delay = 0.0001



def pickRandomWallFrom(walls):
    wall =  walls[randint(0, len(walls)-1)]
    paintSelectedWall(wall)
    sleep(delay)
    return wall

def onlyOneCellIsMarked(cell1, cell2):
    return maze[ cell2[0] * 2 + 1 ][ cell2[1] * 2 + 1] != " "



walls = []

def prim():
    global walls
    cell = (0,0)
    markCell(cell)
    walls = getCellWallsFrom(cell)
    while(len(walls)>0):
        wall = pickRandomWallFrom(walls)
        cell1 = wall[0]
        cell2 = wall[1]     
        if onlyOneCellIsMarked(cell1, cell2):
            markCell(cell2)
            makeGap(wall)
            newWalls = getCellWallsFrom(cell2)                             
            addNewWalls(newWalls)                      
        removeWall(wall)
    setStartEndCell()





    
           
    
                   


















def callback(event):    
    hilo = threading.Thread(target=prim)
    hilo.start()    

show()