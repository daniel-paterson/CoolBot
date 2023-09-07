import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

#number of songs displayed when the queue command is used
queueDisplayLength = 4

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.isPlaying = False
        self.isPaused = False

        self.musicQueue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        self.vc = None

    def search_yt(self, item): #searches for a youtube video and returns dict with url and title
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0] #search for a video (no download)
            except Exception:
                return False
        return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    def play_next(self): #plays the next song in queue
        if len(self.musicQueue) > 0: #if there is still music in the queue...

            self.isPlaying = True #we are playing

            music_url = self.musicQueue[0][0]['source'] #get the top url in the queue

            self.musicQueue.pop(0) #remove that song from the queue

            self.vc.play(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next()) #play the music, and when its done run this function again

        else:
            self.isPlaying = False #nothing in the queue? we are not playing
    


    async def play_music(self, ctx): #same as play next, but first makes sure we are in a voice channel

        if len(self.musicQueue) > 0:
            self.isPlaying = True
            music_url = self.musicQueue[0][0]['source']

            if self.vc == None or not self.vc.is_connected(): #if not in a vc...
                self.vc = await self.musicQueue[0][1].connect() #try and join one

                if self.vc == None: #make sure we joined one
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.musicQueue[0][1])
            
            self.musicQueue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(music_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())



    @commands.command(name="play", alieses=["p"], help="Plays a song based on a given url or search term(s)")
    async def play(self, ctx, *args):
        query = "".join(args) #grab the key words that the user is using, and put them in a string

        voice_channel = ctx.author.voice.channel
        if voice_channel is None: #is the user in a vc?
            await ctx.send("You gotta connect to a voice channel before trying to play something!")
        elif self.isPaused: #are we paused?
            self.vc.resume()
        else:
            song = self.search_yt(query) #get the song
            if type(song) == type(True): #make sure it worked and we got a song
                await ctx.send("Couldn't downoad the song. Incorrect format, try a different keyword.")
            else:
                await ctx.send("Song added to queue") #adds the song to the queue
                self.musicQueue.append([song, voice_channel])

                if self.isPlaying == False: #if we aren't already playing, start playing
                    await self.play_music(ctx)

    @commands.command(name="pause", help="Pauses the song currently being played")
    async def pause(self, ctx, *args):
        if self.isPlaying:
            self.isPlaying = False
            self.isPaused = True
            self.vc.pause()
        elif self.isPaused:
            self.vc.resume()

    @commands.command(name="resume", alieses=["r"], help="Unpauses the bot and resumes playing the current song")
    async def resume(self, ctx, *args):
        if self.isPaused:
            self.isPlaying = True
            self.isPaused = False
            self.vc.resume()

    @commands.command(name="skip", alieses=["s"], help="Skips the currently playing song")
    async def skip(self, ctx, *args):
        if self.vc != None and self.vc:
            self.vc.stop()
            await self.play_music(ctx)

    @commands.command(name="queue", alieses=["q"], help=f"Displays the next {queueDisplayLength} songs in the queue")
    async def queue(self, ctx): #TODO update to add link functionality instead of just names
        out = ""

        for i in range(0, len(self.musicQueue)):
            if i > queueDisplayLength: break
            out += self.musicQueue[i][0]['title']+'\n'
        
        if out != "":
            await ctx.send(out)
        else:
            await ctx.send("Queue is empty")
    
    @commands.command(name="clear", alieses=["c","trash"], help="Stops the current song and clears the queue")
    async def clear(self, ctx, *args):
        if self.vc != None and self.isPlaying:
            self.vc.stop()
        self.musicQueue = []
        await ctx.send("Music queue cleared")
    
    @commands.command(name="leave", alieses=["disconnect","l","d"], help="Kicks the bot from the voice channel")
    async def leave(self, ctx,):
        self.isPlaying = False
        self.isPaused = False
        await self.vc.disconnect()