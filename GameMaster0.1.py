
#TODO: allows fuctionaly to either dig or flag a square
#TODO: at the start everything show us as a :blue_box: 

from random import choice
import copy

difficulties = {
    "Beginner" : [9,9,10],
    "Intermediate" : [16,16,40],
    "Expert" : [16,30,99]
#[row length, number of rows, number of mines]
}
def initalization(difficulty):
#This makes and sets the grid variables acording to the difficulty
    for x in difficulties:
        if difficulty == x:
            global rowlength
            global rowquantity
            global minequantity
            rowlength = difficulties[x][0]
            rowquantity = difficulties[x][1]
            minequantity = difficulties[x][2]
            difficultychosen = True
    CreateGrid()
def CreateGrid():
#create the grid by putting a new list in the gird for each row and then apeending to each row to make collumns
    global grid
    grid = list()
    for x in range(rowquantity):
        grid.append(list())
        for y in range(rowlength):
            grid[x].append(0)
    placeMines()

def placeMines():
#This is the function that generates the mines
    minesplaced = 0
    while minesplaced < minequantity:
        randomrow = choice(range(len(grid)))
        randomspot = choice(range(len(grid[0])))
        if grid[randomrow][randomspot] != -1:
            grid[randomrow][randomspot] = -1
            minesplaced += 1
#prints the gird before the numbers around the mines are added
    for x in grid:
        print(x)
    addNumbersAroundBombs()

#This is the function that generates the numbers around the mines

differences = [[0,-1],[0,1],[-1,0],[-1,-1],[-1,1],[1,0],[1,-1],[1,1]]
#TODO: remover the spoilers after generation testing is done
discordspoilers = {
-2 : ":zero:",
0 : "||:zero:||",
1 : "||:one:||",
2 : "||:two:||",
3 : "||:three:||",
4 : "||:four:||",
5 : "||:five:||",
6 : "||:six:||",
7 : "||:seven:||",
8 : "||:eight:||",
9 : "||:bomb:||"
}
def addNumbersAroundBombs():
    for x in grid:
        for y in x:
            if y == -1:
                row = grid.index(x)
                spot = x.index(y)
                for z in differences:
                    if (row+z[0]) >= 0:
                        if (row+z[0]) <= len(grid)-1:
                            if (spot+z[1]) >= 0:
                                if (spot+z[1]) <= len(x)-1:
                                    if grid[row+z[0]][spot+z[1]] != -1:
                                        if grid[row+z[0]][spot+z[1]] != 9:
                                            grid[row+z[0]][spot+z[1]] += 1
                grid[row][spot] = 9
    #this creats a copy grid with the numbers around the mines
    global newgrid
    newgrid = copy.deepcopy(grid)
    startingSpot()
#create new grid to store the discord spoilers


def startingSpot():
#chose a random spot to be the first spot to be revealed
    zeropicked = False
    while zeropicked == False:
        randomrow = choice(range(len(grid)))
        randomspot = choice(range(len(grid[0])))
        #i stole this from stackoverflow ^, it's so beautiful
        if grid[randomrow][randomspot] == 0:
            grid[randomrow][randomspot] = -2
            zeropicked = True
    printGridWithSpoilersAndEmojis()

#this takes the grid and swaps out each number for its corresponding string from discordspoilers            
def printGridWithSpoilersAndEmojis():
    for x in grid:
        for y in x:
            row = grid.index(x)
            spot = x.index(y)
            for z in discordspoilers:
                if y == z:
                    grid[row][spot] = discordspoilers[z]
    finalPrints()

def finalPrints():
#this prints the original grid
    for x in newgrid:
        print(x)

    print("SEPERATOR")
    #this prints the copy/paste without the square brackets and commas
    for x in grid:
        print(' '.join(x))


#plase hepl