from discord.ext import commands
import discord
import tools
import discord_components

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener(name='on_button_click')
    async def helpaction(self,interaction):
        pagelist = tools.readconfig()
        if interaction.component.label == "back":
            if pagelist['helplist'][str(interaction.message.id)] == 0:
                pass
            else:
                a = await self.bot.get_channel(interaction.channel_id).fetch_message(interaction.message.id)
                pagelist['helplist'][str(interaction.message.id)] -= 1
                th = pagelist['helplist'][str(interaction.message.id)]
                await a.edit(embed=tools.help_pages[int(th)])
                tools.saveconfig(pagelist)
        if interaction.component.label == "next":
            if pagelist['helplist'][str(interaction.message.id)] == 3:
                pass
            else:
                a = await self.bot.get_channel(interaction.channel_id).fetch_message(interaction.message.id)
                pagelist['helplist'][str(interaction.message.id)] += 1
                th = pagelist['helplist'][str(interaction.message.id)]
                await a.edit(embed=tools.help_pages[int(th)])
                tools.saveconfig(pagelist)
        try:
            await interaction.respond()
        except:
            pass
    @commands.command()
    async def althelp(self,ctx):
        pagelist = tools.readconfig()
        lol = await ctx.send(embed=tools.help_pages[0], components=[[discord_components.Button(style=discord_components.ButtonStyle.red, label="back", custom_id="helpback"),discord_components.Button(style=discord_components.ButtonStyle.green, label="next", custom_id="helpnext")]])
        pagelist['helplist'][lol.id] = 0
        tools.saveconfig(pagelist)
def setup(bot):
    bot.add_cog(help(bot))
    print('Help Loaded!')