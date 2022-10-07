
#TODO: allows fuctionaly to either dig or flag a square
#TODO: at the start everything show us as a :blue_box: 
#TODO: make diffuculties use regex

from random import choice
import copy
from time import sleep
import re


difficulties = {
    #[row length, number of rows, number of mines]
    "beginner" : [9,9,10],
    "intermediate" : [16,16,40],
    "expert" : [16,30,99]

}

Emojis = {
-2 : ":trianglular_flag_on_post:",
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
    "dig" : -1,
    "flag" : -2
}
                  #beginner
def initalization(difficulty):
#This makes and sets the grid variables acording to the difficulty
    global rowlength
    global rowquantity
    global minequantity
    for x in difficulties:
        difficulty = difficulty.lower()
        if re.match(x,difficulty):
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
    global plotGrid
    for x in originGrid:
        plotGrid = copy.deepcopy(originGrid)
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
        for y in range(rowlength):
            userGrid[x][y] = -1
    startingSpot()

def editSentGrid():
    #get row from cordinates, edit corosponding row from msg[x]
    #edit with corosponding row from userGrid[x]

    return

#TODO: change to dig and flag
def Dig(row,spot,message,client):
    #this is a function that takes in a x,y cordiate and returns the correct emoji
    if userGrid[row][spot] == -1:
        userGrid[row][spot] = originGrid[row][spot]
        editSentGrid()


        client.loop.create_task(message.reply("You have dug this spot", delete_after=4))
        sleep(10)
        message.delete
        
    else :
        client.loop.create_task(message.reply("You have already dug this spot", delete_after=4))
        sleep(10)
        message.delete
    
def Flag(row,spot,message,client):
    #this is a function that takes in a x,y cordiate and sets that cordinate to a flag(-2)
    if userGrid[row][spot] == -1:
        userGrid[row][spot] = -2
        editSentGrid()
        client.loop.create_task(message.reply("You have flagged this spot", delete_after=4))
        sleep(10)
        message.delete
        
    else :
        client.loop.create_task(message.reply("You have already flagged this spot", delete_after=4))
        sleep(10)
        message.delete

#next
#TODO: make it so that if you dig a zero it digs all the zeros around it
# make it so when givem a cordiante it reveal() the number
# print the grid with emojis

def spotCoordinates(spot,row):  
    spot = (int(spot))-1
    row = int(row)
    coordTable = {}
    for x in range(rowquantity):
        coordTable[x] = list(reversed(range(1,(rowquantity+1))))[x]
    for x in coordTable:
        if coordTable[x] == row: # type: ignore
            row = x
            yield row
            yield spot
            

def startingSpot():
#chose a random spot to be the first spot to be revealed
    zeropicked = False
    while zeropicked == False:
        randomrow = choice(range(len(originGrid)))
        randomspot = choice(range(len(originGrid[0])))
        #i stole this from stackoverflow ^, it's so beautiful
        if originGrid[randomrow][randomspot] == 0:
            userGrid[randomrow][randomspot] = originGrid[randomrow][randomspot]
            zeropicked = True
    finalPrints()

#this takes the grid and swaps out each number for its corresponding string from discordspoilers            


def finalPrints():
#this prints the original grid
#prints the grid with only bombs
    for x in plotGrid:
        print(x)

    print("SEPERATOR")
# prints the copy/paste without the square brackets and commas
    for x in originGrid:
        print(' '.join(str(x)))

    print("SEPERATOR")
#prints the user grid
    for x in userGrid:
        print(x)



initalization("beginner")

#plase hepl ~ BbrDbr
#save my soul ~ Aerlen