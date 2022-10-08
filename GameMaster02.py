
#TODO: allows fuctionaly to either dig or flag a square
#TODO: at the start everything show us as a :blue_box: 
#TODO: make diffuculties use regex

from random import choice
import copy
from time import sleep
import re
from discord import Emoji

DIFFICULTIES = {
    #[rows length, number of rows, number of mines]
    "beginner" : [9,9,10],
    "intermediate" : [16,16,40],
    "expert" : [16,30,99],
    "mobile" : [11,20,34]
}

EMOJIS = {
-2 : ":triangular_flag_on_post:",
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

COMMANDS = {
    "dig" : -1,
    "flag" : -2
}

async def initalization(requestedDifficulty,client,message):
#def initalization(requestedDifficulty):
#This makes and sets the grid variables acording to the difficulty
    global rowlength
    global rowquantity
    global minequantity
#ugly but it works so shut the fuck up
    global badDifficulty
    badDifficulty = False
    for difficulty in DIFFICULTIES:
        requestedDifficulty = requestedDifficulty.lower()
        if re.match(requestedDifficulty,difficulty):
            await message.channel.send('Starting a new game')
            sleep(0.5)
            rowlength = DIFFICULTIES[difficulty][0]
            rowquantity = DIFFICULTIES[difficulty][1]
            minequantity = DIFFICULTIES[difficulty][2]
            badDifficulty = False
            CreateGrid()

        if re.match(requestedDifficulty,difficulty)== False:
            await message.channel.send("Please chose a valid difficulty")
            badDifficulty = True
            break

def CreateGrid():
#create the grid by putting a new list in the gird for each rows and then apeending to each rows to make collumns
    global originGrid
    originGrid = list()
    for i in range(rowquantity):
        originGrid.append(list())
        for y in range(rowlength):
            originGrid[i].append(0)
    coordTabler()
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
    for i in originGrid:
        plotGrid = copy.deepcopy(originGrid)
    addNumbersAroundBombs()

#This is the function that generates the numbers around the mines

differences = [[0,-1],[0,1],[-1,0],[-1,-1],[-1,1],[1,0],[1,-1],[1,1]]

def addNumbersAroundBombs():
    for i in originGrid:
        for y in i:
            if y == -1:
                Y = originGrid.index(i)
                X = i.index(y)
                for z in differences:
                    if (Y+z[0]) >= 0:
                        if (Y+z[0]) <= len(originGrid)-1:
                            if (X+z[1]) >= 0:
                                if (X+z[1]) <= len(i)-1:
                                    if originGrid[Y+z[0]][X+z[1]] != -1:
                                        if originGrid[Y+z[0]][X+z[1]] != 9:
                                            originGrid[Y+z[0]][X+z[1]] += 1
                originGrid[Y][X] = 9
    #this creats a copy grid with the numbers around the mines
    global userGrid
    userGrid = copy.deepcopy(originGrid)
    createUserGrid()
    
#create new grid to store the discord spoilers

def createUserGrid():
    for i in range(rowquantity):
        for y in range(rowlength):
            userGrid[i][y] = -1
    startingSpot()

async def editSentGrid():
    #get rows from cordinates, edit corosponding rows from msg[i]
    #edit with corosponding rows from userGrid[i]

    return

async def Dig(X,Y,message,client):
    #this is a function that takes in a x,y cordiate and returns the correct emoji
    if userGrid[Y][X] == -1:
        userGrid[Y][X] = originGrid[Y][X]
        if originGrid[Y][X] == 0:
            aroundZero(X,Y)

        await editSentGrid()
        finalPrints()
        await message.reply("You have dug this spot", delete_after=4)
        sleep(10)
        message.delete
        
    else :
        await message.reply("You have already dug this spot", delete_after=4)
        sleep(10)
        message.delete

async def Flag(X,Y,message,client):
    #this is a function that takes in a x,y cordiate and sets that cordinate to a flag(-2)
    if userGrid[Y][X] == -1:
        userGrid[Y][X] = -2
        if originGrid[Y][X] == 0:
            aroundZero(X,Y)
        await editSentGrid()
        await message.reply("You have flagged this spot", delete_after=4)
        sleep(10)
        message.delete
        
    else :
        await message.reply("You have already flagged this spot", delete_after=4)
        sleep(10)
        message.delete

def aroundZero(X,Y):
    for z in differences:
        userGrid[Y+z[1]][X+z[0]] = originGrid[Y+z[1]][X+z[0]]

#next
#TODO: make it so that if you dig a zero it digs all the zeros around it
# make it so when givem a cordiante it reveal() the number
# print the grid with emojis

def coordTabler():  
    global coordTable
    coordTable = {}
    for i in range(rowquantity):
        coordTable[i] = list(reversed(range(1,(rowquantity+1))))[i]
def rowCoordinates(Y):
    Y = int(Y)
    for i in coordTable:
        if coordTable[i] == Y: # type: ignore
            Y = i
    return Y
    
def startingSpot():
#chose a random X to be the first X to be revealed
    zeropicked = False
    while zeropicked == False:
        randomrow = choice(range(len(originGrid)))
        randomspot = choice(range(len(originGrid[0])))
        #i stole this from stackoverflow ^, it's so beautiful
        if originGrid[randomrow][randomspot] == 0:
            userGrid[randomrow][randomspot] = originGrid[randomrow][randomspot]
            zeropicked = True
    userToEmojiGrid()

#this takes the grid and swaps out each number for its corresponding string from discordspoilers            

#TODO: improve this function

def userToEmojiGrid():
    global emojiGrid
    emojiGrid = copy.deepcopy(userGrid)
    for i in EMOJIS:
        for y in emojiGrid:
            for z in y:
                if z == i:
                    y[y.index(z)] = EMOJIS[i]
    for i in emojiGrid:
        emojiGrid[emojiGrid.index(i)].append(coordTable[emojiGrid.index(i)])

def finalPrints():
#this prints the original grid
#prints the grid with only bombs
    for i in plotGrid:
        print(i)

    print("SEPERATOR")
# prints the copy/paste without the square brackets and commas
    for i in originGrid:
        print(' '.join(str(i)))

    print("SEPERATOR")
#prints the user grid
    for i in userGrid:
        print(i)
#prints emoji grid
    for i in range(len(emojiGrid)):
        global target
        target = {91:None,93:None,39:None,44:None}
        finalEmojiGrid = (str(emojiGrid[i]).translate(target))
        print(finalEmojiGrid)
    print(coordTable)
#initalization("beginner")

#plase hepl ~ BbrDbr
#save my soul ~ Aerlen