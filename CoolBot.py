import discord, random
from discord.ext import commands

def getKey():
    with open("apiKey.txt") as keyFile:
        key = keyFile.readline()
    return key

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix = ';', intents=intents) #sets up the bot, names it 'bot', and sets the command prefix

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')




client.run(getKey())