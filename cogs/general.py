import discord
from discord.ext import commands
import random

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["info", "ui"])
    @commands.cooldown(1, 5, commands.BucketType.user)
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
        embed.add_field(name="__**General info**__", value=f"**Discord Name:** {user}\n"
                                                           f"**Account created:** {user.created_at.__format__('%A %d %B %Y at %H:%M')}\n")

        embed.add_field(name="__**Server-related information:**__", value=f"**Nickname:** {user.nick}\n"
                                                                          f"**Joined server:** {user.joined_at.__format__('%A %d %B %Y at %H:%M')}\n"
                                                                          f"**Roles:** {' '.join([r.mention for r in user.roles[1:]])}")

        await ctx.send(embed=embed)
    
    # Get a users Avatar
    @commands.command(aliases=["av"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, user: discord.Member = None):
        user = ctx.author if not user else user
        ft = "gif" if user.is_avatar_animated() else "png"
        embed = discord.Embed(colour=discord.Colour.purple(), title=f"{user.name}'s Avatar", url=f"{user.avatar_url_as(format=ft)}")
        await ctx.send(embed=embed.set_image(url=f"{user.avatar_url_as(format=ft)}"))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def say(self, ctx, *, mes):
        mes = mes.replace("@everyone", "@ everyone")
        mes = mes.replace("@here", "@ here")
        await ctx.message.delete()
        await ctx.send(mes)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def flip(self, ctx):
        hf = ["Heads", "Tails"]
        ch = random.choice(hf)
        await ctx.send(ch)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rps(self, ctx, *, choice = None):
        if choice is None:
            return await ctx.send("You need to pick from rock paper and scissors")

        choices = ["rock", "paper", "scissors"]
        pick = random.choice(choices)

        if pick == choice.lower():
            await ctx.send(f"You picked {choice} and I picked {pick}. Tie!")

        if pick == "rock" and choice.lower() == "scissors":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Lose!")

        if pick == "rock" and choice.lower() == "paper":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Win!")

        if pick == "paper" and choice.lower() == "rock":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Lose!")

        if pick == "paper" and choice.lower() == "scissors":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Win!")

        if pick == "scissors" and choice.lower() == "rock":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Win!")

        if pick == "scissors" and choice.lower() == "paper":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Lose!")
        


def setup(bot):
    bot.add_cog(General(bot))