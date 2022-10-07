
#basic imports
from time import sleep
import discord
import os
import re
#import mine and grid generation
import GameMaster02

#TODO: edit the message https://javascript.tutorialink.com/how-to-make-a-bot-edit-its-own-message-on-discord/
#TODO: add help command with info on how to 
#TODO: make end condition either win or loss
#TODO: block startying new game untill other one is over


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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    global is_printing_grid

# \$dig\s*([1-3]?[0-9]),([1-3]?[0-9])   
    if message.content.startswith('$'):

        #see if msg matches with a command and if it does run the respective action
        #IT WORKS HAZZZA 
        digOrFlagMatchResults = re.match('(\\$dig|\\$flag)\\s*([1-9]?[0-9]),([1-3]?[0-9])', message.content)
        if digOrFlagMatchResults is not None:
            
            action = digOrFlagMatchResults.group(1)
            spot = int(digOrFlagMatchResults.group(2))
            row = int(digOrFlagMatchResults.group(3))

            if action == '$dig':
                GameMaster02.spotCoordinates(row,spot)

                GameMaster02.Dig(GameMaster02.spotCoordinates(row,spot)[0],spot,message,client)
            if action == '$flag':
                GameMaster02.spotCoordinates(row,spot)
                GameMaster02.Flag(row,spot,message,client)
            
            message = await message.channel.fetch_message(message.id)

        #$play msg with diffuculty
        playAndDiffcultyMatchResults = re.match('(\\S{5})\\s*(\\S+)', message.content)
        if playAndDiffcultyMatchResults is not None:
            await message.channel.send('Starting a new game')
            GameMaster02.initalization(playAndDiffcultyMatchResults.group(2))

        
        
        is_printing_grid = True
        print("Is printing grid: " + str(is_printing_grid))
        try:
            msg = []
            for x in GameMaster02.userGrid:

                tempMsg = await message.channel.send(' '.join(str(x)))
                msg.append(tempMsg.id)
                sleep(0.2)


        finally:
            print("Is printing grid: " + str(is_printing_grid))
            is_printing_grid = False
            gridID = message.id
    else :
        if is_printing_grid and message.content != ('') :
            await message.delete()

client.run(TOKEN) # type: ignore