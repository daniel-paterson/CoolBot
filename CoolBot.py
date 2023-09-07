import discord, random
from discord.ext import commands
from discord.ext.commands import CommandNotFound


intents = discord.Intents.default()
intents.message_content = True

#sets up the bot, names it 'bot', and sets the command prefix
bot = commands.Bot(command_prefix = ';', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
       await ctx.send("I don't know what that means")

#prints in the terminal when the bot is online
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')



@bot.command()
async def test(ctx, *args):
    userSaid = " ".join(args)
    await ctx.send(f"{ctx.message.author} said {userSaid}")

@bot.command()
async def shutdown(ctx):
    if await bot.is_owner(ctx.message.author):
        await ctx.send("Logging off...")
        await bot.close()
    else:
        await ctx.send("Only the bot owner can use this command")




@bot.command()
async def roll(ctx, dice: str):
    try:
        rolls, limit = map(int, dice.split('d'))
        if (rolls < 1 or limit < 1):
            raise Exception
        if (rolls > 100 or limit > 100):
            await ctx.send('For the sake of keeping things running smoothly, please don\'t use numbers greater than 100.')
    except Exception:
        await ctx.send('Format has to be in NdM where N and M are non-zero integers.')
        return

    numbers = ''
    result = 0
    for r in range(rolls):
        n = random.randint(1, limit)
        numbers += (str(n)+ '  ')
        result += n
    
    await ctx.send(f'Numbers rolled: {numbers}\nTotal: {result}')



def getKey(): #for obvious reasons, the api key is not stored on git
    with open("apiKey.txt") as keyFile:
        key = keyFile.readline()
    return key

bot.run(getKey())