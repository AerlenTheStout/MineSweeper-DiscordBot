
#TODO: allows fuctionaly to either dig or flag a square
#TODO: at the start everything show us as a :blue_box: 

from random import choice
import copy

difficulties = {
    #[row length, number of rows, number of mines]
    "Beginner" : [9,9,10],
    "Intermediate" : [16,16,40],
    "Expert" : [16,30,99]

}

Emojis = {
-1 : ":blue_square:",
0 : ":zero:",
1 : ":one:",
2 : ":two:",
3 : ":three:",
4 : ":four:",
5 : ":five:",
6 : ":six:",
7 : ":seven:",
8 : ":eight:",
9 : ":bomb:"
}

commands = {
    "dig" : 1,
    "flag" : 2
}

def initalization(difficulty):
#This makes and sets the grid variables acording to the difficulty
    global rowlength
    global rowquantity
    global minequantity
    for x in difficulties:
        if difficulty == x:
            rowlength = difficulties[x][0]
            rowquantity = difficulties[x][1]
            minequantity = difficulties[x][2]
    CreateGrid()



def CreateGrid():
#create the grid by putting a new list in the gird for each row and then apeending to each row to make collumns
    global originGrid
    originGrid = list()
    for x in range(rowquantity):
        originGrid.append(list())
        for y in range(rowlength):
            originGrid[x].append(0)
    placeMines()

def placeMines():
#This is the function that generates the mines
    minesplaced = 0
    while minesplaced < minequantity:
        randomrow = choice(range(len(originGrid)))
        randomspot = choice(range(len(originGrid[0])))
        if originGrid[randomrow][randomspot] != -1:
            originGrid[randomrow][randomspot] = -1
            minesplaced += 1
#prints the gird before the numbers around the mines are added
    for x in originGrid:
        print(x)
    addNumbersAroundBombs()

#This is the function that generates the numbers around the mines

differences = [[0,-1],[0,1],[-1,0],[-1,-1],[-1,1],[1,0],[1,-1],[1,1]]
#TODO: remover the spoilers after generation testing is done

def addNumbersAroundBombs():
    for x in originGrid:
        for y in x:
            if y == -1:
                row = originGrid.index(x)
                spot = x.index(y)
                for z in differences:
                    if (row+z[0]) >= 0:
                        if (row+z[0]) <= len(originGrid)-1:
                            if (spot+z[1]) >= 0:
                                if (spot+z[1]) <= len(x)-1:
                                    if originGrid[row+z[0]][spot+z[1]] != -1:
                                        if originGrid[row+z[0]][spot+z[1]] != 9:
                                            originGrid[row+z[0]][spot+z[1]] += 1
                originGrid[row][spot] = 9
    #this creats a copy grid with the numbers around the mines
    global userGrid
    userGrid = copy.deepcopy(originGrid)
    createUserGrid()
    
#create new grid to store the discord spoilers

def createUserGrid():
    for x in range(rowquantity):
        userGrid.append(list())
        for y in range(rowlength):
            userGrid[x].append(-1)

#TODO: change to dig and flag
def Reveal(row,spot):
    #this is a function that takes in a x,y cordiate and returns the correct emoji
    if userGrid[row][spot] == -1:
        userGrid[row][spot] = originGrid[row][spot]

def ToBeDetermined():

    validinput = False
    while validinput == False:
        userinput = input("Please input the coordinates and command")
        userinput = userinput.split(",")
        coordx = (int(userinput[0]))-1
        coordy = int(userinput[1])
        command = userinput[2]
        for x in commands:
            if command == x:
                modifier = commands[x]
                validinput = True
        if validinput == False:
            print("Input invalid, please try again")

    coordTable = {}
    for x in range(rowquantity):
        coordTable[x] = list(reversed(range(1,(rowquantity+1))))[x]
    print(coordTable)
    for x in coordTable:
        if coordTable[x] == coordy:
            coordy = x
    originGrid[coordy][coordx] = modifier
    for x in originGrid:
        print(x)

def startingSpot():
#chose a random spot to be the first spot to be revealed
    zeropicked = False
    while zeropicked == False:
        randomrow = choice(range(len(originGrid)))
        randomspot = choice(range(len(originGrid[0])))
        #i stole this from stackoverflow ^, it's so beautiful
        if originGrid[randomrow][randomspot] == 0:
            originGrid[randomrow][randomspot] = Reveal(randomrow,randomspot)
            zeropicked = True
    printGridWithEmojis()

#this takes the grid and swaps out each number for its corresponding string from discordspoilers            
def printGridWithEmojis():
    for x in originGrid:
        for y in x:
            row = originGrid.index(x)
            spot = x.index(y)
            for z in Emojis:
                if y == z:
                    originGrid[row][spot] = Emojis[z]
    finalPrints()

def finalPrints():
#this prints the original grid
    for x in userGrid:
        print(x)

    print("SEPERATOR")
    #this prints the copy/paste without the square brackets and commas
    for x in originGrid:
        print(' '.join(x))


#plase hepl