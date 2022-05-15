import asyncio
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL
from collections import Iterable
queue = []

YDL_OPTIONS = {
            "format" : "bestaudio",
            "postprocessors" : [{
                "key" : "FFmpegExtractAudio",
                "preferredcodec" : "mp3",
                "preferredquality" : "192",
            }], "noplaylist" : "True"
        }

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

def play_next():
    queue.pop(0)
    if len(queue) >= 1:
        source = queue[0]['source']
        voice.play(discord.FFmpegPCMAudio(queue[0]['source'], FFMPEG_OPTIONS), after=lambda e: play_next())
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.07

def lstr(list : Iterable):
        string = f"{list[0]}"
        for i in range(1, len(list)):
            string += f" {list[i]}"
        return string

def search_yt(item):
        with YoutubeDL(YDL_OPTIONS) as ydl:
            try: 
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception: 
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}



class music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.command(pass_context=True, aliases=['p', 'pla'])
    async def play(ctx, *query):
         query = lstr(query)
         song = search_yt(query)
         queue.append(song)
         global voice
         channel = ctx.message.author.voice.channel
         voice = get(bot.voice_clients, guild=ctx.guild)

         if voice and voice.is_connected():
             await voice.move_to(channel)
         else:
             voice = await channel.connect()

         await voice.disconnect()

         if voice and voice.is_connected():
             await voice.move_to(channel)
         else:
             voice = await channel.connect()
             print(f"The bot has connected to {channel}\n")

         voice.play(discord.FFmpegPCMAudio(queue[0]['source'], FFMPEG_OPTIONS), after=lambda e: play_next())
         voice.source = discord.PCMVolumeTransformer(voice.source)
         voice.source.volume = 0.07
    
def setup(bot):
    bot.add_cog(music(bot))
    print("Ready Music!")
