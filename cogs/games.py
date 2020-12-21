import discord
from discord.ext import commands
import random
from datetime import datetime

class Games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def flip(self, ctx):
        """
        Flips heads or tails.
        """
        hf = ["Heads", "Tails"]
        ch = random.choice(hf)
        await ctx.send(ch)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def rps(self, ctx, *, choice = None):
        """
        Plays a game of rock paper scissors.
        """
        if choice is None:
            return await ctx.send("You need to pick from rock paper and scissors")

        choices = ["rock", "paper", "scissors"]
        pick = random.choice(choices)

        embed = discord.Embed(colour=discord.Colour.purple(), title="Rock Paper Scissors")

        if pick == choice.lower():
            embed.add_field(name="Tie!", value=f"`You picked {choice} and I picked {pick}.`")
            await ctx.send(embed=embed)

        elif pick == "rock" and choice.lower() == "scissors":
            embed.add_field(name="You Lose!", value=f"`You picked {choice} and I picked {pick}.`")
            await ctx.send(embed=embed) 

        elif pick == "rock" and choice.lower() == "paper":
            await embed.add_field(name="You Win!", value=f"`You picked {choice} and I picked {pick}.`")
            await ctx.send(embed=embed) 

        elif pick == "paper" and choice.lower() == "rock":
            embed.add_field(name="You Lose!", value=f"`You picked {choice} and I picked {pick}.`")
            await ctx.send(embed=embed) 

        elif pick == "paper" and choice.lower() == "scissors":
            embed.add_field(name="`You Win!", value=f"You picked {choice} and I picked {pick}.`")
            await ctx.send(embed=embed) 

        elif pick == "scissors" and choice.lower() == "rock":
            embed.add_field(name="You Win!", value=f"`You picked {choice} and I picked {pick}.`")
            await ctx.send(embed=embed) 
            
        else:
            await embed.add_field(name="You Lose!", value=f"`You picked {choice} and I picked {pick}.`")
            await ctx.send(embed=embed) 

def setup(bot):
    bot.add_cog(Games(bot))
