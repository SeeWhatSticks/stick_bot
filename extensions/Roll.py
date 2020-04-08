from random import randint, choice
from discord import Embed
from discord.ext import commands

COLOR = 0xff9933

class Roll(commands.Cog):
    """Introduces some different kinds of random chance."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def flip(self, ctx):
        """Flip a coin."""
        await ctx.channel.send(embed=Embed(
                title="Flipped a coin for {}:".format(ctx.author.display_name),
                description="It came up {}!".format(choice(["heads", "tails"])),
                color=COLOR))

    @commands.command()
    async def roll(self, ctx, input_str):
        """Roll some dice."""
        await ctx.channel.send(embed=Embed(
            title="Rolled dice for {}:".format(ctx.author.display_name),
            description="It came up {}!".format(choice(["heads", "tails"])),
            color=COLOR))
    #     sum = 0
    #     while any([v in input_str for v in ["+", "-"]]):
    #         index =
    #         bit, add, input_str = input_str.partition(input_str[index])

    @commands.command()
    async def choose(self, ctx, *, input_str):
        """Choose from a list."""
        options = input_str.split(sep="/")
        await ctx.channel.send(embed=Embed(
                title="Made a choice for {}:".format(ctx.author.display_name),
                description="From {} options: {}".format(
                        len(options),
                        choice(options)),
                color=COLOR))

def setup(bot):
    bot.add_cog(Roll(bot))
