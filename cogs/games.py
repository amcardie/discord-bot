import discord
from discord.ext import commands
import random
from datetime import datetime


class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    # I saw a timer test thingy in the discord.py discord server a while ago so I wanna try and re-make that
    @commands.command(aliases=["10s", "10"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def ten(self, ctx):
        embed = discord.Embed(colour=discord.Colour.purple(), title="10s timer test")
        ft = "gif" if ctx.author.is_avatar_animated() else "png"
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url_as(format=ft))
        mes = await ctx.send(embed=embed)
        await mes.add_reaction("⏲️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == "⏲️"

        await self.bot.wait_for('reaction_add', check=check)
        begin = mes.created_at
        end = datetime.utcnow()
        final = end - begin
        res = f"{final.seconds} seconds and " + f"{final.microseconds}"[:2]

        # new_embed = discord.Embed(colour=discord.Colour.purple(), title=f"{res}")
        # new_embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url_as(format=ft)
        embed.add_field(name="Results", value=f"{res} milliseconds")
        await mes.edit(embed=embed)
        # await ctx.send(embed=new_embed)
 
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
    bot.add_cog(Games(bot))