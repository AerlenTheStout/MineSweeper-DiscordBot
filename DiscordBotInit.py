
#basic imports
import asyncio
from time import sleep
import discord
import os
import re
#import mine and grid generation
import GameMaster02
#speedtesting
#from profilehooks import profile

#TODO: edit the message https://javascript.tutorialink.com/how-to-make-a-bot-edit-its-own-message-on-discord/
#TODO: add help command with info on how to 
#TODO: make end condition either win or loss
#TODO: block startying new game untill other one is over


#XXX: OKAY FOR THIS PAGE TOMMOROOW
#when i dig with a capital letter at the start it take an incredibly long time to respond
#when i dig withOUT a capital letter at the start it responds almsot instantly

#dotenv to store discord token securly
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('TOKEN')
is_printing_grid = False

#
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

async def printGrid(message):
    is_printing_grid = True
    
    try:
        print("Is printing grid: " + str(is_printing_grid))
        global msgIDs
        msgIDs = []
        GameMaster02.userToEmojiGrid()
        GameMaster02.finalPrints()
        for i in range(len(GameMaster02.emojiGrid)):
            tempMsg = await message.channel.send((str(GameMaster02.emojiGrid[i]).translate(GameMaster02.target)))
            msgIDs.append(tempMsg.id)
    finally:
        print("Is printing grid: " + str(is_printing_grid))
        is_printing_grid = False
        #gridID = message.id




async def editPrintedGrid(Y,message):
    wantedMSGID = msgIDs[Y]
    wantedMSG = await message.channel.fetch_message(wantedMSGID)
    GameMaster02.userToEmojiGrid()
    GameMaster02.finalPrints()
    await wantedMSG.edit(content=(str(GameMaster02.emojiGrid[Y]).translate(GameMaster02.target)))


async def digOrFlag(message):
    digOrFlagMatchResults = re.match('(\\$dig|\\$flag)\\s*([a-zA-Z]),([1-9]?[0-9])', message.content)
    if digOrFlagMatchResults is not None:
        action = digOrFlagMatchResults.group(1)
        X = digOrFlagMatchResults.group(2)
        Y = int(digOrFlagMatchResults.group(3))

        X = GameMaster02.XLetters(X)
        Y = GameMaster02.rowCoordinates(Y)

        print(action,X,Y)
        
        if action.lower() == '$dig':
            print('digging')
            await GameMaster02.Dig(X,Y,message,client)
            print('digged')
            await editPrintedGrid(Y,message)
            sleep(10)
            message.delete()
        if action.lower() == '$flag':
            print('flagging')
            await GameMaster02.Flag(X,Y,message,client)
            print('flagged')
            await editPrintedGrid(Y,message)
            sleep(10)
            message.delete()
        #await GameMaster02.win(message)
        GameMaster02.win()
        if GameMaster02.Win == True:
            for i in range(GameMaster02.rowquantity):
                await editPrintedGrid(i)
            await message.channel.send("YOU WIN!")
        if GameMaster02.Lost == True:
            for i in range(GameMaster02.rowquantity):
                await editPrintedGrid(i)
            await message.channel.send("YOU LOSE!")


#@profile(immediate=True)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global is_printing_grid
    is_printing_grid = False

    
# \$dig\s*([1-3]?[0-9]),([1-3]?[0-9])   
    if message.content.startswith('$'):

        #$play msg with diffuculty
        playAndDiffcultyMatchResults = re.match('(\\S{5})\\s*(\\S+)', message.content)
        if playAndDiffcultyMatchResults is not None:
            await GameMaster02.initalization(playAndDiffcultyMatchResults.group(2),client,message)

        if GameMaster02.badDifficulty == False:
            if re.match('\\$play', message.content):
                await printGrid(message)
            elif re.match('\\$lose', message.content):
                GameMaster02.Lost = True
                GameMaster02.originToEmojiGrid()
            #elif re.match('\\$win', message.content):
                #await GameMaster02.win(message)
            elif re.match('(\\$dig|\\$flag)\\s*([a-zA-Z]),([1-9]?[0-9])', message.content):
                await digOrFlag(message)
            else:
                await message.channel.send('Send a working command please', delete_after=5)
        
    if is_printing_grid == True and message.content != ('') :
            await message.delete()
client.run(TOKEN) # type: ignore