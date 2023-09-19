from discord.ext import commands

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def pingcmd(self, ctx):
        await ctx.send(ctx.author.mention)

    # doing something when the cog gets loaded
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    # doing something when the cog gets unloaded
    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

    @commands.command() #turns off the bot, only usable by me
    async def shutdown(self, ctx):
        if await self.is_owner(ctx.message.author):
            await ctx.send("Logging off...")
            await self.close()
        else:
            await ctx.send("Only the bot owner can use this command") #note to self, figure out the other better way of checking if the owner is sending the message
    
    

async def setup(bot):
    await bot.add_cog(GeneralCog(bot=bot))