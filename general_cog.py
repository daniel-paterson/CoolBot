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