import asyncio
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

YDL_OPTIONS = {
            "format" : "bestaudio",
            "postprocessors" : [{
                "key" : "FFmpegExtractAudio",
                "preferredcodec" : "mp3",
                "preferredquality" : "192",
            }], "noplaylist" : "True"
        }

class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command()
    async def join(self,ctx):
        await ctx.message.author.voice.channel.connect()      
        await ctx.send("Joined!")
    @commands.command()
    async def leave(self,ctx):
        await ctx.message.author.guild.voice_client.disconnect()
    @commands.command()
    async def play(self,ctx,link):
        await ctx.send("お待ちください...")
        with ctx.message.channel.typing():
            with YoutubeDL(YDL_OPTIONS) as ydl:
                try: 
                    info = ydl.extract_info("ytsearch:%s" % link, download=False)['entries'][0]
                except Exception: 
                    pass

            
            
            
            voice = ctx.message.author.guild.voice_client
            
            voice.play(discord.FFmpegPCMAudio(info['formats'][0]['url'], FFMPEG_OPTIONS))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.07
            
            
         
            await ctx.message.channel.send(f'再生しています！')
    @commands.command(aliases=["resume"])
    async def pause(self, ctx):
        """Pauses any currently playing audio."""
        client = ctx.guild.voice_client
        if client.is_paused():
            client.resume()
        else:
            client.pause()

def setup(bot):
    bot.add_cog(music(bot))
    print("Ready Music!")
