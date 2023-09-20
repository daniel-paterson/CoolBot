from discord.ext import commands

class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="ping")
    async def pingcmd(self, ctx):
        await ctx.send(f"{ctx.author.mention} pong!")
        await ctx.message.add_reaction("👋")


    # doing something when the cog gets loaded
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    # doing something when the cog gets unloaded
    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")
    
    @commands.Cog.listener()
    async def on_load(self, ctx):
        print("CoolBot is now online")


async def setup(bot):
    await bot.add_cog(GeneralCog(bot=bot))