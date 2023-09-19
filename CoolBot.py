import discord
from discord import commands

class bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = ";",
            intents = discord.Intents.all()
        )
    
    async def setup_hook(self):
        await self.load_extention("general_cog")



@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
       await ctx.send("I don't know what that means")


#for obvious reasons, the api key is not stored on git
def getKey():
    with open("apiKey.txt") as keyFile:
        key = keyFile.readline()
    return key

bot.run(getKey())