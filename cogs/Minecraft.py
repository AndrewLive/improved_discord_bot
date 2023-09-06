import os, discord
from discord.ext import commands
from mcstatus import JavaServer
from dotenv import load_dotenv

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ip = "127.0.0.1"
        self.port = 25575
        self.server = JavaServer.lookup(self.ip)

        load_dotenv('../.env')
        self.rconPass = os.getenv('RCON')

        try:
            self.query = self.server.query()
        except:
            print("server cannot be reached at this time")

    @commands.command(aliases=["mc"])
    async def minecraft(self, ctx, *args):
        # check if in relevant server
        whitelist = {902602831675138108:"AGD", 960413256814592010:"Denny's"}
        print(ctx.message.guild.id)
        if ctx.message.guild.id not in whitelist.keys():
            print("Not whitelisted server")
            return

        embed = discord.Embed(title="Denny's DarkRPG Minecraft Server",color=0x00FF3F)
        embed.set_thumbnail(url="https://i.kym-cdn.com/photos/images/newsfeed/002/378/234/23a.png")
        try:
            # build embed
            self.query = self.server.query()
            embed.add_field(name="IP", value="nile.puresynergy.com:1987", inline=False)
            embed.add_field(name="Version", value=self.query.software.version, inline=False)
            embed.add_field(name="MOTD", value=self.query.motd.raw, inline=False)
            embed.add_field(name="Modpack", value="DarkRPG 7.2.3 with a few additions", inline=False)

            players = self.query.players.online
            embed.add_field(name=f"Online Players [{self.query.players.online}/{self.query.players.max}]", value=f"{players} {'player' if players == 1 else 'players'} online: {', '.join(self.query.players.names)}", inline=False)

        except Exception as e:
            embed.add_field(name="Unable to reach server", value=e)

        await ctx.send(embed=embed)


    @commands.command(aliases=["rcon"])
    async def rconsay(self, ctx, *args):
        try:
            self.server.ping()
        except:
            ctx.send("Unable to reach server")
            return
        
        msg = ' '.join(args)
        command = f'mcrcon -H {self.ip} -P {self.port} -p {self.rconPass} "say <Discord: {ctx.message.author.name}> {msg}"'
        os.system(command)

        # print(command)

        await ctx.send(f'Sent message to server: <Discord: {ctx.message.author.name}> {msg}')
        return