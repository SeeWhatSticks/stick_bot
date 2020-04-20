import os
import json

from discord import User, Embed, Colour
from discord.ext import commands


data_file = "profiles_data.json"


class Profiles(commands.Cog):
    """Extension description."""

    def __init__(self, bot):
        self.bot = bot
        if not os.path.exists(data_file):
            with open(data_file, "w") as f:
                json.dump({}, f)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.author.bot:
            return  # Ignore bots

    @commands.group(aliases=["profile"])
    async def profiles(self, ctx):
        """Command group for managing profiles. Defaults to show."""
        if ctx.invoked_subcommand is None:
            await self.show(ctx)

    @profiles.command()
    async def set(self, ctx, user: User, *, profile: str):
        """Adds a new profile."""
        profiles = self.read()
        profiles[str(user.id)] = profile
        self.write(profiles)

        embed = Embed(
            title=f"Set profile for {ctx.guild.get_member(user.id).display_name}",
            color=Colour.green()
        )

        embed.add_field(name="Profile", value=profile, inline=False)

        await ctx.channel.send(embed=embed)

    @profiles.command(aliases=["del"])
    async def delete(self, ctx, user: User):
        """Deletes a profile."""
        profiles = self.read()
        oldProfile = profiles[str(user.id)]
        del profiles[str(user.id)]
        self.write(profiles)

        embed = Embed(
            title=f"Deleted profile for {ctx.guild.get_member(user.id).display_name}",
            color=Colour.green()
        )
        embed.add_field(
            name="Previous content",
            value=oldProfile,
            inline=False
        )

        await ctx.channel.send(embed=embed)

    @profiles.command()
    async def show(self, ctx: commands.Context):
        """Shows all profiles."""
        async with ctx.channel.typing():
            profiles = self.read()
            if len(profiles) == 0:
                ctx.channel.send(embed=Embed(
                    title="No profiles are set!",
                    color=Colour.red(),
                    description="Try using the following to set one: ```!profiles set @User Some profile text```"
                ))
            else:
                await self.send_single_embed(ctx, profiles)

    async def send_single_embed(self, ctx, profiles):
        embed = Embed(
            title="Here's who's around",
            colour=Colour.blue()
        )

        descriptions = []
        for id, profile in profiles.items():
            member = ctx.guild.get_member(int(id))
            if member is None:
                raise commands.errors.CommandError(
                    f"Couldn't find member with id {id}"
                )
            embed.add_field(
                name=member.display_name,
                value=profile,
                inline=False
            )

        description = "\n\n".join(descriptions)

        await ctx.channel.send(embed=embed)

    def read(self) -> dict:
        with open(data_file, "r") as f:
            return json.load(f)

    def write(self, o: dict):
        with open(data_file, "w") as f:
            json.dump(o, f)


def setup(bot):
    bot.add_cog(Profiles(bot))


def teardown(bot):
    pass
