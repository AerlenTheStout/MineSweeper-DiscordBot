from argparse import Action
from ast import IsNot
from importlib.resources import contents
import re
from GameMaster0.2 import Reveal
#TODO: delete users msg after TBD seconds
#TODO: edit the message https://javascript.tutorialink.com/how-to-make-a-bot-edit-its-own-message-on-discord/
#TODO: add help command with info on how to 

#basic imports
import discord
import os
#import mine and grid generation
import GameMaster

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
        
        splitMsg = message.content.split(' ' and ',')

        #see if msg matches with a command and if it does run the respective action
        #cureent regex... it can fiund $dig or $flag... but after that cant find the numbers... im going to sob
        matchResults = re.match('(\\$dig|\\$flag)\\s*([1-9]?[0-9]),([1-3]?[0-9]', message.content)
        if matchResults is not None:
            
            action = matchResults.group(1)
            row = int(matchResults.group(2))
            spot = int(matchResults.group(3))
            if action == '$dig':
                GameMaster.Dig(row,spot)
            if action == '$flag':
                GameMaster.Flag(row,spot)
            
            message = await message.channel.fetch_message(message.id)

        if re.match('\\Q$\\E[[:alpha:]]*', splitMsg[0]):
            await message.channel.send('Starting a new game')
            GameMaster.initalization(splitMsg[1])

        
        print("Is printing grid: " + str(is_printing_grid))
        is_printing_grid = True
        try:
            for x in GameMaster.grid:
                await message.channel.send(' '.join(x))
        finally:
            print("Is printing grid: " + str(is_printing_grid))
            is_printing_grid = False
            gridID = message.id
    else :
        if is_printing_grid and message.content != ('') :
            await message.delete()

client.run(TOKEN) # type: ignore