import discord
import random
import time
from discord.ext import commands
from datetime import datetime, timedelta
from platform import python_version
from psutil import Process, virtual_memory


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["info", "ui"])
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """
        Get a users info from the server
        """

        # If user isnt specified default to author
        if user is None:
            user = ctx.author
        
        # Creating embed
        embed = discord.Embed(
            colour = discord.Colour.purple(), title = f"{user.name}'s Info'")
        embed.set_footer(text=f"ID: {user.id}")
        ft = "gif" if user.is_avatar_animated() else "png"
        embed.set_thumbnail(url=user.avatar_url_as(format=ft))

        # These fields are from a website called programcreek.com / https://www.programcreek.com/python/example/107400/discord.Embed
        embed.add_field(name="__**General Info**__", value=f"**Discord Name:** {user}\n"
                                                           f"**Account created:** {user.created_at.__format__('%A %d %B %Y at %H:%M')}\n")

        embed.add_field(name="__**Server-related Information:**__", value=f"**Nickname:** {user.nick}\n"
                                                                          f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
                                                                          f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}")

        await ctx.send(embed=embed)
    
    # Get a users Avatar
    @commands.command(aliases=["av"])
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def avatar(self, ctx, user: discord.Member = None):
        """
        Gets a users avatar.
        """
        user = ctx.author if not user else user
        ft = "gif" if user.is_avatar_animated() else "png"
        embed = discord.Embed(colour=discord.Colour.purple(), title=f"{user.name}'s Avatar", url=f"{user.avatar_url_as(format=ft)}")
        await ctx.send(embed=embed.set_image(url=f"{user.avatar_url_as(format=ft)}"))
    
    @commands.command(aliases=["stats"])
    async def botstats(self, ctx):
        """
        Displays the bots statistics
        """
        embed = discord.Embed(colour=ctx.author.colour, title="Bot Stats", thumbnail=self.bot.user.avatar_url)

        proc = Process()
        with proc.oneshot():
            now = int(time.time())
            nt = now - proc.create_time()
            uptime = timedelta(seconds=nt)
            memory_total = virtual_memory().total / (1024**3)
            memory_of_total = proc.memory_percent()
            memory_usage = memory_total * (memory_of_total / 100)
        
        ft = "gif" if ctx.author.is_avatar_animated() else "png"
        
        embed.add_field(name="Python Version", value=python_version(), inline=True)
        embed.add_field(name="Discord.py Version", value=discord.__version__, inline=True)
        embed.add_field(name="Uptime", value=uptime, inline=False)
        embed.add_field(name="Memory Usage", value=f"{memory_usage:,.2} / {memory_total:,.0f} GB ({memory_of_total:,.0f}%)", inline=False)

        embed.set_footer(text=f"Requested by {ctx.author.name}")
        embed.set_thumbnail(url=self.bot.user.avatar_url_as(format=ft))

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(General(bot))
