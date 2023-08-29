import discord, pafy, asyncio, random
from discord.ext import commands

bot = commands.Bot(command_prefix = '$') #sets up the bot, names it 'bot', and sets the command prefix

class WrongChannelError(commands.CheckFailure): #custom error for trying to call the bot in the wrong channel
    pass
    
def in_Bot_Commands(): #checks to make sure the command is being run in the correct channel
    async def predicate(ctx):
        if ctx.channel.name != 'bot-commands':
            raise WrongChannelError("Sorry, thats the wrong channel!") #maybe add a way to display who made the bad call?
        return True
    return commands.check(predicate)

@bot.event #prints 'online' in the command line once the bot comes online
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
    print('------')
        
        
        
    
class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command() #provides diagnostic data
    async def hello(self, ctx):
        await ctx.send('Hello!')
        
        
    @commands.command() #rolls some dice
    @in_Bot_Commands()
    async def roll(self, ctx, dice: str):
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
        
        await ctx.send('Numbers rolled: '+numbers )
        """result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))"""
        await ctx.send('Total: '+str(result))
        
        

class AudioSorce(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    
    @commands.command() 
    @in_Bot_Commands()
    async def getSource(self, ctx, url):
        try:
            video = pafy.new(url)
        except ValueError:
            await ctx.send("Error: Not a valid link")
        
        audio = video.getbestaudio()
        
        
            

class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @in_Bot_Commands()
    async def join(self, ctx): #joins the vc that the person who made the command is currently in
        
        try:
            channel = ctx.author.voice.channel
            
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)

            await channel.connect()
            
        except AttributeError:
            await ctx.send("Enter the voice chat you want me to join first.")
        
    @commands.command()
    @in_Bot_Commands()
    async def leave(self, ctx): #leaves the current vc
        
        if ctx.voice_client is not None:
            await ctx.disconnect()
        else:
            await ctx.send("I need to be in a voice chat before I can leave one")
            
            
    """@commands.command()
    @in_Bot_Commands()
    async def p(self, ctx, *, url): #streams audio from a url
        
        
        async with ctx.typing():
            
            
        await ctx.send('Now playing')"""


def getToken():
    with open("apiKey.txt") as keyFile:
        key = keyFile.readlines()
    return key


bot.add_cog(Misc(bot))
bot.add_cog(AudioSorce(bot))
bot.add_cog(Player(bot))

bot.run(getToken()) #runs the bot, establishing a link with Discord using the API token. Needs to reman the final line in the script
#TOKEN NEEDS TO REMAIN A SECRET, REGENERATE ASAP IF LEAKED!!!