import discord, random
from discord.ext import commands
from discord.ext.commands import CommandNotFound

def getKey():
    with open("apiKey.txt") as keyFile:
        key = keyFile.readline()
    return key

intents = discord.Intents.default()
intents.message_content = True

#sets up the bot, names it 'bot', and sets the command prefix
bot = commands.Bot(command_prefix = ';', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
       await ctx.send("Yeah, I don't know what that means")

#prints in the terminal when the bot is online
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')



@bot.command()
async def test(ctx, *args):
    userSaid = " ".join(args)
    await ctx.send(f"You said {userSaid}")


bot.run(getKey())