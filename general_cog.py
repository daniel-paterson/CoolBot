import discord
from discord import commands

class general_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.helpMessage = """
```
General Commands:
/help - Displays all avalible commands

Music commands:
/p <search terms> - Searches for a song and plays it in a voice channel
/q - Displays the current song queue
/skip - Skips the currently playing song
/clear - Stops the current song and clears the queue
/leave - Kicks the bot from the voice channel
/pause - Pauses the current song, or resumes it if already paused
/resume - Resumes the current song
```
"""

    @commands.HelpCommand()
    async def help(self, ctx, arg):
        if arg == None:
            await ctx.send(self.helpMessage)
        else:
            await ctx.send(ctx.send_command_help(arg))
    

    @commands.command() #turns off the bot, only usable by me
    async def shutdown(self, ctx):
        if await self.is_owner(ctx.message.author):
            await ctx.send("Logging off...")
            await self.close()
        else:
            await ctx.send("Only the bot owner can use this command") #note to self, figure out the other better way of checking if the owner is sending the message
    
    @commands.command() #useful for bug testing
    async def test(self, ctx, *args):
        userSaid = " ".join(args)
        await ctx.send(f"{ctx.message.author} said {userSaid}")