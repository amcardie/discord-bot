import discord
from discord.ext import commands
import random

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