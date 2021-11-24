import discord
from discord.ext import commands
import os
import discord_components

bot = commands.Bot(command_prefix='m.')
cogs = [
    'help'
]

@bot.event
async def on_ready():
    discord_components.DiscordComponents(bot)   
    await bot.change_presence(activity=discord.Game("Stable"))
    for i in cogs:
        bot.load_extension("cogs." + i)
    print("Ready!")

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

@bot.is_owner
@bot.command()
async def managecog(ctx,mode=None,cogname=None):
    if cogname == None:
        await ctx.send('type cog name')
    if mode == 'reload':
        bot.reload_extension('cogs.' + cogname)
        await ctx.send("reloaded " + cogname)
    elif mode == 'unload':
        bot.unload_extension('cogs.' + cogname)
        await ctx.send("unloaded " + cogname)
    elif mode == 'load':
        bot.load_extension('cogs.' + cogname)
        await ctx.send("loaded " + cogname)
    else:
        await ctx.send('reload unload load')

bot.run(os.environ['token'])