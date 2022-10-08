
#basic imports
import asyncio
import random
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

#@profile(immediate=True)
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global is_printing_grid

# \$dig\s*([1-3]?[0-9]),([1-3]?[0-9])   
    if message.content.startswith('$'):

        #see if msg matches with a command and if it does run the respective action
        #IT WORKS HAZZZA 
        digOrFlagMatchResults = re.match('(\\$dig|\\$flag)\\s*([1-9]?[0-9]),([1-9]?[0-9])', message.content)

        if digOrFlagMatchResults is not None:
            
            action = digOrFlagMatchResults.group(1)
            X = int(digOrFlagMatchResults.group(2))-1
            Y = int(digOrFlagMatchResults.group(3))

            Y = GameMaster02.rowCoordinates(Y)

            print(action,X,Y)

            if action == '$dig':
                await GameMaster02.Dig(X,Y,message,client)
            if action == '$flag':
                await GameMaster02.Flag(X,Y,message,client)
            
        message = await message.channel.fetch_message(message.id)

        #$play msg with diffuculty
        playAndDiffcultyMatchResults = re.match('(\\S{5})\\s*(\\S+)', message.content)
        if playAndDiffcultyMatchResults is not None:
            await GameMaster02.initalization(playAndDiffcultyMatchResults.group(2),client,message)

        
        if GameMaster02.badDifficulty == False:
            is_printing_grid = True
            print("Is printing grid: " + str(is_printing_grid))
            try:
                msg = []
                GameMaster02.userToEmojiGrid()
                GameMaster02.finalPrints()
                for i in range(len(GameMaster02.emojiGrid)):
                    tempMsg = await message.channel.send((str(GameMaster02.emojiGrid[i]).translate(GameMaster02.target)))
                    msg.append(tempMsg.id)
                    sleep(0.5)


            finally:
                print("Is printing grid: " + str(is_printing_grid))
                is_printing_grid = False
                gridID = message.id
        else :
            if is_printing_grid and message.content != ('') :
                await message.delete()

client.run(TOKEN) # type: ignore