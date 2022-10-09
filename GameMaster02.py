
from random import choice
import copy
import re


target = {91:None,93:None,39:None,44:None}
#TODO: custom difficulty
DIFFICULTIES = {
    #[rows length, number of rows, number of mines]
    "beginner" : [9,9,10],
    "intermediate" : [16,16,40],
    "expert" : [16,30,99],
    "mintermediate" : [11,20,34],
    "mexpert" : [11,50,115],
    "ez" : [3,3,1],
    "wtf" : [26,50,270]
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
9 : ":boom:",
10: ":bomb:"
}

ALPHABET = {
    "a" : 0,"b" : 1,"c" : 2,"d" : 3,"e" : 4,"f" : 5,"g" : 6,"h" : 7,"i" : 8,"j" : 9,"k" : 10,"l" : 11,"m" : 12,"n" : 13,"o" : 14,"p" : 15,"q" : 16,"r" : 17,"s" : 18,"t" : 19,"u" : 20,"v" : 21,"w" : 22,"x" : 23,"y" : 24,"z" : 25
}

ALPHABETEMOJI = [":regional_indicator_a:",":regional_indicator_b:",":regional_indicator_c:",":regional_indicator_d:",":regional_indicator_e:",":regional_indicator_f:",":regional_indicator_g:",":regional_indicator_h:",":regional_indicator_i:",":regional_indicator_j:",":regional_indicator_k:",":regional_indicator_l:",":regional_indicator_m:",":regional_indicator_n:",":regional_indicator_o:",":regional_indicator_p:",":regional_indicator_q:",":regional_indicator_r:",":regional_indicator_s:",":regional_indicator_t:",":regional_indicator_u:",":regional_indicator_v:",":regional_indicator_w:",":regional_indicator_x:",":regional_indicator_y:",":regional_indicator_z:"]

async def initalization(requestedDifficulty,client,message):
#def initalization(requestedDifficulty):
#This makes and sets the grid variables acording to the difficulty
    global rowlength
    global rowquantity
    global minequantity
    global Winned
    Winned = False
    global Lost
    Lost = False
    global indexIgnore
    indexIgnore = []
#ugly but it works so shut the fuck up
    global badDifficulty
    badDifficulty = False
    for difficulty in DIFFICULTIES:
        requestedDifficulty = requestedDifficulty.lower()
        if re.match(requestedDifficulty,difficulty):
            await message.channel.send('Starting a new game')
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

differences = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]

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

async def Dig(X,Y,message,client):
    global Lost
    #this is a function that takes in a x,y cordiate and returns the correct emoji
    if originGrid[Y][X] == 9:
        Lost = True
    if userGrid[Y][X] == -1:
        userGrid[Y][X] = originGrid[Y][X]
        if originGrid[Y][X] == 0:
            aroundZero(X,Y)
        finalPrints()
        await message.reply("You dug this spot", delete_after=4)
        
    else :
        await message.reply("You have already dug this spot", delete_after=4)
        
        

async def Flag(X,Y,message,client):
    #this is a function that takes in a x,y cordiate and sets that cordinate to a flag(-2)
    
    if userGrid[Y][X] == -1:
        userGrid[Y][X] = -2
    
        #await editSentGrid()
        await message.reply("You flagged this spot", delete_after=4)
        
    else :
        await message.reply("You have already flagged this spot", delete_after=4)
        



def aroundZero(X,Y):
    
    if [Y,X] not in indexIgnore:
        for z in differences:
            if (Y+z[0]) >= 0:
                if (Y+z[0]) <= len(originGrid)-1:
                    if (X+z[1]) >= 0:
                        if (X+z[1]) <= rowlength-1:
                            userGrid[Y+z[0]][X+z[1]] = originGrid[Y+z[0]][X+z[1]]
                            indexIgnore.append([Y,X])
                            if userGrid[Y+z[0]][X+z[1]] == 0:
                                aroundZero(X+z[1],Y+z[0])


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
    
    
def XLetters(X):
    for i in ALPHABET:
        if X == i:
            X = ALPHABET[i]
            return X
    
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
            aroundZero(randomspot,randomrow)
    userToEmojiGrid()

#this takes the grid and swaps out each number for its corresponding string from discordspoilers            

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
    tempAlphabet = []
    for i in range (rowlength):
        tempAlphabet.append(ALPHABETEMOJI[i])
    tempAlphabet.append("|")
    emojiGrid.append(tempAlphabet)
    

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
        finalEmojiGrid = (str(emojiGrid[i]).translate(target))
        print(finalEmojiGrid)
    print(coordTable)

#plase hepl ~ BbrDbr
#save my soul ~ Aerlen

def originToEmojiGrid():
    emojiGrid = copy.deepcopy(originGrid)
    for i in EMOJIS:
        for y in emojiGrid:
            for z in y:
                if z == i:
                    y[y.index(z)] = EMOJIS[i]
    for i in emojiGrid:
        emojiGrid[emojiGrid.index(i)].append(coordTable[emojiGrid.index(i)])
    tempAlphabet = []
    for i in range (rowlength):
        tempAlphabet.append(ALPHABETEMOJI[i])
    tempAlphabet.append("0")

def win():
    global Winned
    for i in userGrid:
        for n in i:
            if n == -1:
                return
            if n == 9:
                return
    for i in originGrid:
        for n in i:
            if n == 9:
                originGrid[originGrid.index(i)][i.index(n)] = 10
        Winned = True
        return (Winned)