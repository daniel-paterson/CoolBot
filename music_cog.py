import discord, asyncio
from discord.ext import commands
import yt_dlp

#number of songs displayed when the queue command is used
queueDisplayLength = 4

yt_dlp.utils.bug_reports_message = lambda: ''


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
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)

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
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)



class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.musicQueue = []



    #
    #non-command functions
    #
        
    async def playNext(self, ctx):
        if len(self.musicQueue) > 0: #if there is music in the queue...


            url = self.musicQueue.pop() #remove the next song from the queue and store it

            async with ctx.typing(): #play the music
                player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                ctx.voice_client.play(player, after=await self.playNext(ctx)) #after playing, run this function again
            
            await ctx.send(f'Now playing: {player.title}')

        else: #if the queue is empty...
            await ctx.send("Reached end of music queue")



    #
    #commands
    #

    @commands.command(name="play", alieses=['p'])
    async def play(self, ctx, *, url):
        self.musicQueue.append(url) #add the song to the queue
        await ctx.message.add_reaction("✅")

        if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused(): #if we aren't already playing stuff, start playing stuff
            await self.playNext(ctx)


    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()
    
    @commands.command(name="pause", alieses=['resume'])
    async def pause(self, ctx):
        if not ctx.voice_client.is_paused():
            ctx.voice_client.pause()
            await ctx.message.add_reaction("⏸")
        else:
            ctx.voice_client.resume()
            await ctx.message.add_reaction("▶")



    # @commands.command()
    # async def volume(self, ctx, volume: int):
    #     """Changes the player's volume"""

    #     if ctx.voice_client is None:
    #         return await ctx.send("Not connected to a voice channel.")

    #     ctx.voice_client.source.volume = volume / 100
    #     await ctx.send(f"Changed volume to {volume}%")


    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.message.add_reaction("🛑")



    #
    #other
    #

    @play.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
    

    async def cog_load(self):
        print(f"{self.__class__.__name__} loaded!")

    async def cog_unload(self):
        print(f"{self.__class__.__name__} unloaded!")



async def setup(bot):
    await bot.add_cog(MusicCog(bot=bot))