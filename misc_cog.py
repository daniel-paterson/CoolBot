import discord
from discord import commands
from youtube_dl import YoutubeDL

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False
        self.is_paused = False

        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnected_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def search_yt(self, item): #searches for a youtube video and returns dict with url and title
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0] #search for a video (no download)
            except Exception:
                return False
        return {'source': info['formats'[0]['url']], 'title': info['title']}
    
    def play_next(self): #plays the next song in queue
        if len(self.music_queue) > 0: #if there is still music in the queue...

            self.is_playing = True #we are playing

            music_url = self.music_queue[0][0]['source'] #get the top url in the queue

            self.music_queue.pop(0) #remove that song from the queue

            self.vc.play(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next()) #play the music, and when its done run this function again

        else:
            self.is_playing = False #nothing in the queue? we are not playing
    


    async def play_music(self, ctx): #same as play next, but first makes sure we are in a voice channel

        if len(self.music_queue) > 0:
            self.is_playing = True
            music_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected(): #if not in a vc...
                self.vc = await self.music_queue[0][1].connect() #try and join one

                if self.vc == None: #make sure we joined one
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())



    @commands.command(name="play", alieses=["p"] help="Plays a song based on a given url or search term(s)")
    async def play(self, ctx, *args):
        query = "".join(args) #grab the key words that the user is using, and put them in a string

        voice_channel = ctx.author.voice.channel
        if voice_channel is None: #is the user in a vc?
            await ctx.send("You gotta connect to a voice channel before trying to play something!")
        elif self.is_paused: #are we paused?
            self.vc.resume()
        else:
            song = self.search_yt(query) #get the song
            if type(song) == type(True): #make sure it worked and we got a song
                await ctx.send("Couldn't downoad the song. Incorrect format, try a different keyword.")
            else:
                await ctx.send("Song added to queue") #adds the song to the queue
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False: #if we aren't already playing, start playing
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the song currently being played")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.vc.resume()