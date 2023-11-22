import re
from random import randint
from discord.ext import commands

def sanitizeDice(dice):
        dice = ''.join(dice)
        dice.replace(" ", "")
        dice = re.split('[dD+]', dice) #god I love regex
        for i in range(len(dice)):
            dice[i] = int(dice[i])
        return dice
    
def calcDice(dice):
    dice = sanitizeDice(dice)
    total = 0
    numbers = []
    for i in range(dice[0]):
        ranNum = randint(1, dice[1])
        numbers.append(ranNum)
        total += ranNum
    if len(dice)>2:
        total += dice[2]
    return numbers, total

class ttrpgCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    # doing something when the cog gets loaded
    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    # doing something when the cog gets unloaded
    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")

    @commands.command() #used for ttrpgs and other stuff like that
    async def roll(self, ctx, *args):
        ctx.message.add_reaction("🎲")
        numbers, total = calcDice(args)
        await ctx.send(f'Numbers rolled: {numbers}\nTotal: {total}')

async def setup(bot):
    await bot.add_cog(ttrpgCog(bot=bot))