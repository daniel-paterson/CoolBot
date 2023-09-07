import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound

from general_cog import general_cog
from music_cog import music_cog
from ttrpg_cog import ttrpg_cog


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix = ';', intents=intents)

@bot.event
async def on_ready():
    await bot.add_cog(general_cog(bot))
    await bot.add_cog(music_cog(bot))
    await bot.add_cog(ttrpg_cog(bot))
    print(f'Logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
       await ctx.send("I don't know what that means")



#for obvious reasons, the api key is not stored on git
def getKey():
    with open("apiKey.txt") as keyFile:
        key = keyFile.readline()
    return key






bot.run(getKey())