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

        elif pick == "rock" and choice.lower() == "scissors":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Lose!")

        elif pick == "rock" and choice.lower() == "paper":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Win!")

        elif pick == "paper" and choice.lower() == "rock":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Lose!")

        elif pick == "paper" and choice.lower() == "scissors":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Win!")

        elif pick == "scissors" and choice.lower() == "rock":
            await ctx.send(f"You picked {choice} and I picked {pick}. You Win!")

        else:
            await ctx.send(f"You picked {choice} and I picked {pick}. You Lose!")

def setup(bot):
    bot.add_cog(Games(bot))
