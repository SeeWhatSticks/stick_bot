import json, requests
from math import radians, cos, sin, asin, sqrt
from discord import Embed, Member
from discord.ext import commands
from discord.ext.commands import ExtensionFailed

key_file = "extensions/howfar_key.txt"
data_file = "extensions/howfar_data.json"
url_prefix = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"

class Howfar(commands.Cog):
    """Tells you how far away from you another user is."""
    def __init__(self, bot, key):
        self.bot = bot
        self.key = key
        try:
            with open(data_file, 'r') as file:
                data = json.loads(file.read)
        except Exception as exc:
            print("Failed to load data file")
            print(repr(Exception))
            data = {
            }
        self.data = data

    @commands.group(aliases=["hf"])
    @commands.guild_only()
    async def howfar(self, ctx):
        """Principal Howfar Command."""
        if ctx.invoked_subcommand is None:
            pass

    @howfar.command()
    async def me(self, ctx, *, location_text):
        """Set your location."""
        url = "{}?key={}&inputtype=textquery&fields=formatted_address,geometry,name&input={}".format(
                url_prefix,
                self.key,
                location_text)
        try:
            response = requests.get(url)
        except Exception as exc:
            print("API request failed")
            print(repr(exc))
            await ctx.channel.send(embed=ctx.bot.error_embed("Something went wrong while looking up your location."))
            return
        if response.status_code != 200:
            await ctx.channel.send(embed=ctx.bot.error_embed("Something went wrong with the location lookup service."))
            return
        result = json.loads(response.text)
        if result['status'] == "ZERO_RESULTS":
            await ctx.channel.send(embed=ctx.bot.error_embed("Google couldn't find that place. Where are you really?"))
            return
        if result['status'] != "OK":
            await ctx.channel.send(embed=ctx.bot.error_embed("Something went wrong at Google. What did you break?"))
            return
        user_data = {
            'loc': result['candidates'][0]['formatted_address'],
            'lat': result['candidates'][0]['geometry']['location']['lat'],
            'lng': result['candidates'][0]['geometry']['location']['lng']
        }
        await ctx.channel.send(embed=Embed(
                title="Location found",
                description="Your co-ordinates are {}° N, {}° E".format(
                        round(user_data['lat'], 4),
                        round(user_data['lng'], 4)),
                color=ctx.bot.colors['default']))
        self.data[str(ctx.author.id)] = user_data
        with open(data_file, 'w') as file:
            json.dump(self.data, file, indent=2)

    @howfar.command()
    async def to(self, ctx, target: Member):
        """Find out how far you are from someone."""
        if str(ctx.author.id) not in self.data:
            await ctx.channel.send(embed=ctx.bot.error_embed("Sorry, I don't know where you are!"))
            return
        user_info = self.data[str(ctx.author.id)]
        if str(target.id) not in self.data:
            await ctx.channel.send(embed=ctx.bot.error_embed("Sorry, I don't know where they are!"))
            return
        target_info = self.data[str(target.id)]
        lat1 = radians(user_info['lat'])
        lng1 = radians(user_info['lng'])
        lat2 = radians(target_info['lat'])
        lng2 = radians(target_info['lng'])
        diff_lng = lng2 - lng1
        diff_lat = lat2 - lat1
        angle = sin(diff_lat/2)**2+cos(lat1)*cos(lat2)*sin(diff_lng/2)**2
        distance = 2*asin(sqrt(angle))*3958.758
        e = Embed(
                title="Distance calculated",
                description="It's {} miles from {} to {}".format(
                        round(distance, 0),
                        user_info['loc'],
                        target_info['loc']),
                color=ctx.bot.colors['default'])
        e.add_field(
                name=ctx.author.display_name,
                value="{}° N, {}° E".format(
                        round(user_info['lat'], 4),
                        round(user_info['lng'], 4)),
                inline=True)
        e.add_field(
                name=target.display_name,
                value="{}° N, {}° E".format(
                        round(target_info['lat'], 4),
                        round(target_info['lng'], 4)),
                inline=True)
        await ctx.channel.send(embed=e)

def setup(bot):
    try:
        with open(key_file, 'r') as file:
            key = file.read()
    except Exception as exc:
        print("Failed to load key file")
        print(repr(exc))
        raise exc
    else:
        bot.add_cog(Howfar(bot, key))
def teardown(bot):
    pass
