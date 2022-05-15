import asyncio
import discord
from discord.ext import commands
import youtube_dl
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
}
ffmpeg_options = {
    'options': '-vn'
}
FFMPEG_BEFORE_OPTS = '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
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
            source = discord.PCMVolumeTransformer(
            discord.FFmpegPCMAudio(link, before_options=FFMPEG_BEFORE_OPTS), volume=1.0)
            
            #player = await YTDLSource.from_url(link, loop=asyncio.get_event_loop())
            ctx.message.author.guild.voice_client.play(source, after=lambda e: print(
                'Player error: %s' % e) if e else None)
            await ctx.message.channel.send(f'{player.title}を再生しています！')
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
