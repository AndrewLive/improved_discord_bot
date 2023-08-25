import os, discord
from discord.ext import commands
from mcstatus import JavaServer

class Minecraft(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ip = "127.0.0.1"
        self.server = JavaServer.lookup(self.ip)
        self.query = self.server.query()

    @commands.command()
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
            embed.add_field(name="IP", value="nile.puresynergy.com:1987", inline=False)
            embed.add_field(name="Version", value=self.query.software.version, inline=False)
            embed.add_field(name="MOTD", value=self.query.motd.raw, inline=False)
            embed.add_field(name="Modpack", value="DarkRPG 7.2.3 with a few additions", inline=False)

            players = self.query.players.online
            embed.add_field(name=f"Online Players [{self.query.players.online}/{self.query.players.max}]", value=f"{players} {'player' if players == 1 else 'players'} online: {', '.join(self.query.players.names)}", inline=False)

        except Exception as e:
            embed.add_field(name="Unable to reach server", value=e)

        await ctx.send(embed=embed)