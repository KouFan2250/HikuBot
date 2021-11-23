import discord
from discord.ext import commands
import os
import tools
import discord_components
pagelist = tools.readconfig()
bot = commands.Bot(command_prefix='m.')
@bot.event
async def on_ready():
    discord_components.DiscordComponents(bot)   
    await bot.change_presence(activity=discord.Game("HikuBot!"))
    print("Ready!")
@bot.event
async def on_button_click(interaction):
    global pagelist
    if interaction.component.label == "back":
        if pagelist['helplist'][interaction.message.id] == 0:
            pass
        else:
            a = await bot.get_channel(interaction.channel_id).fetch_message(interaction.message.id)
            pagelist['helplist'][interaction.message.id] -= 1
            await a.edit(embed=tools.help_pages[pagelist['helplist'][interaction.message.id]])
            tools.saveconfig(pagelist)
    if interaction.component.label == "next":
        if pagelist['helplist'][interaction.message.id] == 3:
            pass
        else:
            a = await bot.get_channel(interaction.channel_id).fetch_message(interaction.message.id)
            pagelist['helplist'][interaction.message.id] += 1
            await a.edit(embed=tools.help_pages[pagelist['helplist'][interaction.message.id]])
            tools.saveconfig(pagelist)

    try:
        await interaction.respond()
    except:
        pass

@bot.command()
async def althelp(ctx):
    lol = await ctx.send(embed=tools.help_pages[0], components=[[discord_components.Button(style=discord_components.ButtonStyle.red, label="back", custom_id="helpback"),discord_components.Button(style=discord_components.ButtonStyle.green, label="next", custom_id="helpnext")]])
    pagelist['helplist'][lol.id] = 0
    tools.saveconfig(pagelist)

bot.run(os.environ['token'])
