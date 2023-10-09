import os, discord
from discord.ext import commands
import random
from gtts import gTTS
import subprocess
from asyncio import sleep

class SunTzu(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.assets = './assets/sun_tzu'
        self.file = open(f'{self.assets}/sun_tzu.txt', 'r')
        self.lines = self.file.readlines()
        # self.lines.remove('\n')
        self.num_lines = len(self.lines)


    @commands.command(aliases=['st'])
    async def suntzu(self, ctx, channel = 'text'):
        """
        Gives a 100% real totally not made up quote from ancient Chinese general Sun Tzu

        Arguments:
            channel: Whether you want the message to be sent through text or voice (user must be connected to voice channel)
        """

        line = random.choice(self.lines)

        sun_tzu_image = 'https://almabooks.com/wp-content/uploads/2019/08/Sun-Tzu.jpg'

        embed = discord.Embed(color=0xede4b2)

        embed.set_author(name='Sun Tzu', url='https://en.wikipedia.org/wiki/Sun_Tzu', icon_url='https://upload.wikimedia.org/wikipedia/commons/c/cf/%E5%90%B4%E5%8F%B8%E9%A9%AC%E5%AD%99%E6%AD%A6.jpg')
        embed.set_thumbnail(url=sun_tzu_image)
        embed.set_footer(text='The Art of War - Sun Tzu')
        embed.add_field(name='', value=line)

        await ctx.send(embed=embed)



        # create audio file for sun tzu quote
        if channel != 'voice' and channel != 'vc':
            return
        if ctx.message.author.voice == None:
            return
        
        tts = gTTS(text = 'Sun Tzu in The Art of War once said: ' + line, lang = 'en', slow = False)
        tts_path = f'{self.assets}/tmp/sun_tzu.mp3'
        tts.save(tts_path)
        # os.system("mpg321 {self.assets}/tmp/sun_tzu.mp3")

        # choose music accounting for special cases
        music_path = self.choose_music(line)
        output_path = f'{self.assets}/tmp/output.mp3'
        self.combine_audio(tts_path, music_path, output_path)

        # enter voice channel and play audio
        channel = ctx.message.author.voice.channel
        voice_client = await channel.connect()

        source = discord.FFmpegPCMAudio(output_path)
        if not voice_client.is_playing():
            voice_client.play(source, after = lambda e: print('DONE'))

            while voice_client.is_playing():
                await sleep(0.1)

            await voice_client.disconnect()

        os.system(f'rm {output_path} {tts_path}')

        return
    
    def choose_music(self, text):
        special_audio = ["Yankee Doodle (Fife and Drum).mp3", "Yankee Doodle (Fife and Drum) trim.mp3"]
        
        # assign special audio
        if text.startswith('I own a musket for home defense, since that\'s what the founding fathers intended.'):
            return f'{self.assets}/audio/Yankee Doodle (Fife and Drum).mp3'

        # choose music at random
        available_music = os.listdir(f'{self.assets}/audio')
        for i in special_audio:
            available_music.remove(i)
        music_path = f'{self.assets}/audio/' + random.choice(available_music)
        # print(f'Using music: {music}')

        return music_path
    

    def combine_audio(self, tts_path, music_path, output_path):
        if music_path == f'{self.assets}/audio/Yankee Doodle (Fife and Drum).mp3':
            os.system(f'ffmpeg -v quiet -stats -i {tts_path} -i "{music_path}" -filter_complex amix=inputs=2:duration=first:dropout_transition=3:weights="1 0.8" -y {output_path}')
            return


        # add random offset to music
        proc = subprocess.Popen(f'ffprobe -v quiet -stats -i {tts_path} -show_entries format=duration -v quiet -of csv="p=0"', shell = True, stdout = subprocess.PIPE, )
        text_duration = proc.communicate()[0].decode('utf-8')
        proc.kill()
        # print(float(text_duration))
        proc = subprocess.Popen(f'ffprobe -v quiet -stats -i "{music_path}" -show_entries format=duration -v quiet -of csv="p=0"', shell = True, stdout = subprocess.PIPE, )
        music_duration = proc.communicate()[0].decode('utf-8')
        proc.kill()
        # print(float(music_duration))


        music_start = random.uniform(0, float(music_duration) - float(text_duration))
        music_end = music_start + float(text_duration)
        # print(music_start, music_end)

        os.system(f'ffmpeg -v quiet -stats -i "{music_path}" -ss {music_start} -to {music_end} -y {self.assets}/tmp/music_trim.mp3')

        os.system(f'ffmpeg -v quiet -stats -i {tts_path} -i "{self.assets}/tmp/music_trim.mp3" -filter_complex amix=inputs=2:duration=first:dropout_transition=3:weights="1 0.6" -y {output_path}')
        os.system(f'rm "{self.assets}/tmp/music_trim.mp3"')
        # os.system("mpg321 output.mp3")


    @commands.command(aliases=['reloadst', 'rst'])
    async def reloadsuntzu(self, ctx):
        """
        Reloads the list of quotes that Sun Tzu can give (only usable by bot owner)
        """

        if ctx.message.author.id != 389616181331361803:
            # print('not valid user')
            return
        self.file = open(f'{self.assets}/sun_tzu.txt', 'r')
        self.lines = self.file.readlines()
        # self.lines.remove('\n')
        self.num_lines = len(self.lines)
        print('reloaded sun tzu')
        return
    
    @commands.command(aliases=['stinput'])
    async def suntzuinput(self, ctx, *, arg):
        """
        Submits a quote for consideration by Sun Tzu
        
        Arguments:
            args: The quote to be submitted. Must be on a single line
        """

        file = open(f'{self.assets}/sun_tzu_input.txt', 'a')
        file.write(''.join(arg))
        print (''.join(arg))
        file.write('\n')
        file.close
