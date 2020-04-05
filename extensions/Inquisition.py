from discord import Embed, ChannelType
from discord.ext import commands

config_file = 'extensions/inquisition_channel_id.txt'

class Inquisition(commands.Cog):
    """Runs the Inquisition channel."""
    def __init__(self, bot, channel_id):
        self.bot = bot
        self.channel = bot.get_channel(channel_id)
        self.info_suffix = "Use the '!inquisition question' (!inq q <question>) command to ask a question."

    @commands.group(aliases=["inq"])
    @commands.guild_only()
    async def inquisition(self, ctx):
        """Principal Inquisition Command."""
        if ctx.invoked_subcommand is None:
            pass

    @inquisition.command(aliases=["q"])
    @commands.cooldown(1, 900)
    async def question(self, ctx, *, question_text):
        """Ask a question in the Inquisition Channel."""
        if ctx.channel != self.channel:
            await ctx.channel.send("This is not the Inquisition channel.")
            return
        message = await ctx.channel.send(embed=Embed(
                title="{} asked a question:".format(ctx.author.display_name),
                description=question_text,
                color=ctx.bot.colors['default']))
        await message.pin()
        await ctx.channel.edit(topic="{} - {}".format(question_text, self.info_suffix))

    @inquisition.command(hidden=True)
    @commands.check_any(
            commands.is_owner(),
            commands.has_role('Operator'))
    # TODO: Check for any role in config.json
    async def setup(self, ctx):
        """Set the Inquisition Channel"""
        if ctx.channel.type != ChannelType.text:
            await ctx.channel.send(embed=ctx.bot.error_embed("Not available here."))
            return
        self.channel = ctx.channel
        with open(config_file, 'w') as file:
            file.write(str(self.channel.id))
        await ctx.channel.send(embed=Embed(
                title="Inquisition",
                description="Let the Inquisition begin! {}".format(self.info_suffix),
                color=ctx.bot.colors['confirm']))

def setup(bot):
    channel_id = None
    try:
        with open(config_file, 'r') as file:
            channel_id = int(file.read())
    except Exception as exc:
        print("Failed to load inquisition_channel_id.txt")
        print(repr(exc))
    bot.add_cog(Inquisition(bot, channel_id))
def teardown(bot):
    pass
