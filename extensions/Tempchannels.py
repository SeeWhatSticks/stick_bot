from datetime import datetime, timedelta
from discord import Embed
from discord.ext import tasks, commands

config_file = 'extensions/tempchannels_category_id.txt'

class Tempchannels(commands.Cog):
    """Allows users to create temporary channels."""
    def __init__(self, bot, category_id):
        self.bot = bot
        self.category = bot.get_channel(category_id)
        self.category_name = "\U000023F2 Temporary Channels"

        self.lifespan = timedelta(hours=48)

        self.cleanup_channels.start()

    @tasks.loop(minutes=1.0)
    async def cleanup_channels(self):
        if self.category is not None:
            for channel in self.category.channels:
                last_message = await channel.fetch_message(channel.last_message_id)
                age = datetime.utcnow()-last_message.created_at
                if age >= self.lifespan:
                    await channel.delete()

    @commands.group(aliases=["tempchan", "tc"])
    @commands.guild_only()
    async def tempchannels(self, ctx):
        """Principal TempChannels Command."""
        if ctx.invoked_subcommand is None:
            pass

    @tempchannels.command()
    async def new(self, ctx, name):
        """Create a new Temporary Channels category."""
        if self.category is None:
            await ctx.channel.send(embed=ctx.bot.error_embed("The Temporary Channels Category is not set up yet."))
            return
        channel = await ctx.guild.create_text_channel(name, category=self.category)
        member = ctx.guild.get_member(ctx.author.id)
        await channel.set_permissions(member, manage_channels=True, manage_messages=True)
        await channel.send(embed=Embed(
                title="Welcome to {}!".format(str(channel)),
                description="A new Temporary Channel moderated by {}.".format(member.display_name),
                color=ctx.bot.colors['default']))

    @tempchannels.command()
    @commands.check_any(
            commands.is_owner(),
            commands.has_role('Operator'))
    # TODO: Check for any role in config.json
    async def setup(self, ctx):
        """Setup the Temporary Channels category."""
        self.category = await ctx.guild.create_category(self.category_name)
        with open(config_file, 'w') as file:
            file.write(str(self.category.id))
        await ctx.channel.send(embed=ctx.bot.confirm_embed("Temporary Channels Category is set up."))

def setup(bot):
    category_id = None
    try:
        with open(config_file, 'r') as file:
            category_id = int(file.read())
    except Exception as exc:
        print("Failed to load config file")
        print(repr(exc))
    bot.add_cog(Tempchannels(bot, category_id))
def teardown(bot):
    pass
