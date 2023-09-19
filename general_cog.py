import discord
from discord.ext import commands

class general_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command() #turns off the bot, only usable by me (maybe)
    async def shutdown(self, ctx):
        if await self.is_owner(ctx.message.author):
            await ctx.send("Logging off...")
            await self.close()
        else:
            await ctx.send("Only the bot owner can use this command") #note to self, figure out the other better way of checking if the owner is sending the message
    
    @commands.command()
    async def ping(self, ctx):
        await ctx.sent("pong!")