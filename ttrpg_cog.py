import discord, random
from discord.ext import commands

class ttrpg_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command() #used for ttrpgs and other stuff like that. TODO: add support for addition, ie "2d10 + 2" or "1d6 + 3d4 + 2"
    async def roll(ctx, dice: str):
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
        
        await ctx.send(f'Numbers rolled: {numbers}\nTotal: {result}')