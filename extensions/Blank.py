from discord.ext import commands

class Blank(commands.Cog):
    """Extension description."""
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return  # Ignore bots

    @commands.group()
    async def command_name(self, ctx):
        """Command description."""
        if ctx.invoked_subcommand is None:
            pass

    @command_name.command()
    async def subcommand_name(self, ctx):
        """Subcommand description."""
        pass

def setup(bot):
    bot.add_cog(Blank(bot))
def teardown(bot):
    pass
