import discord
from discord.ext import commands
import asyncio


from general_cog import general_cog
from music_cog import music_cog
from ttrpg_cog import ttrpg_cog


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix = ';', intents=intents)

async def cogLoader():
    await bot.add_cog(ttrpg_cog(bot))
    await bot.add_cog(general_cog(bot))
    await bot.add_cog(music_cog(bot))
    print("exiting cogLoader!")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
       await ctx.send("I don't know what that means")

@bot.command() #useful for bug testing
async def test(ctx, *args):
    userSaid = " ".join(args)
    await ctx.send(f"{ctx.message.author} said {userSaid}")



#for obvious reasons, the api key is not stored on git
def getKey():
    with open("apiKey.txt") as keyFile:
        key = keyFile.readline()
    return key

asyncLoop = asyncio.get_event_loop()
coroutine = cogLoader()
asyncLoop.run_until_complete(coroutine)

bot.run(getKey())