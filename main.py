import json, types
from discord import Embed
from discord.ext import commands
from discord.ext.commands import ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPointError, ExtensionFailed
from discord.ext.commands import ExtensionNotLoaded

bot = commands.Bot(command_prefix='!')
try:
    with open('config.json', 'r', encoding='utf8') as file:
        bot.config = json.load(file)
except Exception as exc:
    print("Failed to load config.json")
    print(repr(exc))
    bot.config = {
        'extensions': []
    }

bot.colors = {
    'default': 0x3300cc,
    'confirm': 0x33cc00,
    'error': 0xcc3300
}
bot.load_on_ready = True

def confirm_embed(self, text):
    return Embed(
            title="Confirm",
            description=text,
            color=self.colors['confirm'])
bot.confirm_embed = types.MethodType(confirm_embed, bot)

def error_embed(self, text):
    return Embed(
            title="Error",
            description=text,
            color=self.colors['error'])
bot.error_embed = types.MethodType(error_embed, bot)

async def load_extension(name, channel=None):
    try:
        bot.load_extension("extensions.{}".format(name))
    except (ExtensionNotFound, ExtensionAlreadyLoaded, NoEntryPointError, ExtensionFailed) as exc:
        response = "Failed to load extension: {} ({})".format(name, repr(exc))
    else:
        response = "Loaded extension: {}".format(name)
    finally:
        print(response)
        if channel is not None:
            await channel.send(response)

async def unload_extension(name, channel=None):
    try:
        bot.unload_extension("extensions.{}".format(name))
    except ExtensionNotLoaded:
        response = "Extension was not loaded: {}".format(name)
    else:
        response = "Unloaded extension: {}".format(name)
    finally:
        print(response)
        if channel is not None:
            await channel.send(response)

@bot.event
async def on_command_error(ctx, error):
    await ctx.channel.send(embed=ctx.bot.error_embed(
            str(error)))
    raise

@bot.event
async def on_ready():
    print('We have logged in as {}'.format(bot.user))
    if bot.load_on_ready:
        for val in bot.config['extensions']:
            await load_extension(val)
        bot.load_on_ready = False

@bot.group(aliases=["ext"], hidden=False)
@commands.check_any(
        commands.is_owner(),
        commands.has_role('Operator'))
# TODO: Check for any role in config.json
async def extensions(ctx):
    """List all loaded extensions"""
    if ctx.invoked_subcommand is None:
        embed = Embed(
                title="Extensions",
                description="The following extensions are loaded:",
                colour=bot.colors['default']
        )
        for k, v in bot.cogs.items():
            embed.add_field(
                    name=k,
                    value=v.description,
                    inline=False)
        await ctx.channel.send(embed=embed)

@extensions.command()
async def load(ctx, name):
    """Load an extension"""
    await load_extension(name, channel=ctx.channel)

@extensions.command()
async def unload(ctx, name):
    """Unload an extension"""
    await unload_extension(name, channel=ctx.channel)

@extensions.command()
async def reload(ctx, name):
    """Attempt to reload an extension"""
    await unload_extension(name, channel=ctx.channel)
    await load_extension(name, channel=ctx.channel)

@bot.command(hidden=True)
@commands.is_owner()
async def end(ctx):
    for name in list(bot.cogs):
        await unload_extension(name, channel=ctx.channel)
    await bot.close()

try:
    with open('token.txt', 'r') as file:
        bot.run(file.read())
except Exception as exc:
    print("Failed to load token.txt")
    print(repr(exc))
