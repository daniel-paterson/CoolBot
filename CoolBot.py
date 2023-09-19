import discord
from discord.ext import commands

class bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = ";",
            intents = discord.Intents.all()
        )
    
    async def setup_hook(self):
        await self.load_extension("general_cog")


#for obvious reasons, the api key is not stored on git
def getKey():
    with open("apiKey.txt") as keyFile:
        key = keyFile.readline()
    return key

bot().run(getKey())