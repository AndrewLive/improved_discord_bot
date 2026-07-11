import os, discord
from discord.ext import commands, tasks
import random
from datetime import datetime, timedelta


class Ambience(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.assets = './assets/ambience/'
        self.playing = False
        self.current_channel = None
        self.voice_client = None
        self.ambience_loop.start()

    # tasks:    toggle between playing and not playing if done in the same channel
    #           go to new channel and play if done in different channel
    @commands.command(aliases=['amb'])
    async def ambience(self, ctx):
        """
        Plays nice ambience music in the background of the current VC
        """

        if ctx.message.author.voice == None:
            return


        # enter voice channel and play audio
        channel = ctx.message.author.voice.channel
        if (channel != self.current_channel):
            self.voice_client = await channel.connect()
            self.playing = True
            self.current_channel = channel

            new_music = self.choose_music()
            source = discord.FFmpegPCMAudio(new_music)
            self.voice_client.play(source, after = lambda e: print('DONE'))
        else:
            await self.voice_client.disconnect()
            self.voice_client = None
            self.playing = False
            self.current_channel = None
            return


    @tasks.loop(seconds=1)
    async def ambience_loop(self):
        # if in no channel, no need to do anything
        if (self.current_channel == None):
            return

        # if all members leave channel, make bot also leave
        if (len(self.current_channel.members) == 1):
            print("All members left")
            await self.voice_client.disconnect()
            self.voice_client = None
            self.playing = False
            self.current_channel = None
            return

        # if current song is finished, play new song
        if (not self.voice_client.is_playing()):
            print("Song finished, choosing new song")
            new_music = self.choose_music()
            source = discord.FFmpegPCMAudio(new_music)
            self.voice_client.play(source, after = lambda e: print('DONE'))
            return
        
        # else do nothing
        return


    def choose_music(self):
        # choose music at random
        available_music = os.listdir(self.assets)
        music_path = f'{self.assets}' + random.choice(available_music)
        # print(f'Using music: {music}')

        return music_path



        

        