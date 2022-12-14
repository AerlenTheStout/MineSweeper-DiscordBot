from random import choice

difficulties = {
    "Beginner" : [9,9,10],
    "Intermediate" : [16,16,40],
    "Expert" : [16,30,99]
#[row length, number of rows, number of mines]
}
difficultychosen = False
while difficultychosen == False:
    difficulty = input("What difficulty level?")
    for x in difficulties:
        if difficulty == x:
            rowlength = difficulties[x][0]
            rowquantity = difficulties[x][1]
            minequantity = difficulties[x][2]
            difficultychosen = True
    if difficultychosen == False:
        print("Input invalid, please try again")
            
grid = list()
for x in range(rowquantity):
    grid.append(list())
    for y in range(rowlength):
        grid[-1].append(0)
for x in grid:
    print(x)

commands = {
        "dig" : 1,
        "flag" : 2
    }
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
grid[coordy][coordx] = modifier
for x in grid:
    print(x)