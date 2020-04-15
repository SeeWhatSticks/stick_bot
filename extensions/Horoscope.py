from discord.ext import commands
import discord

from pyaztro import Aztro

SIGNS = {
    '♈': "Aries",
    '♉': "Taurus",
    '♊': "Gemini",
    '♋': "Cancer",
    '♌': "Leo",
    '♍': "Virgo",
    '♎': "Libra",
    '♏': "Scorpius",
    '♐': "Sagittarius",
    '♑': "Capricorn",
    '♒': "Aquarius",
    '♓': "Pisces"
}

class Horoscope(commands.Cog):
    """Provides horoscope."""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(usage="star_sign|sign_emoji")
    async def readtealeaves(self, ctx: commands.Context, sign: str):
        """Gets horoscope from pyaztro."""
        async with ctx.channel.typing():
            if sign in SIGNS:
                sign = SIGNS[sign]
            horoscope = Aztro(sign=sign)
            await ctx.channel.send(embed=discord.Embed(
                    title="Your horoscope for {} for a {}".format(
                            horoscope.day,
                            sign.capitalize()),
                    description=horoscope.description
            ))

def setup(bot):
    bot.add_cog(Horoscope(bot))
