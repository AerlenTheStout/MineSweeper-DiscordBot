
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
        splitMsg = message.content.split(' ')
        if splitMsg[0] == '$Play':
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
    else :
        if is_printing_grid and message.content != ('') :
            await message.delete()

client.run(TOKEN) # type: ignore