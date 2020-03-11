import discord
from discord.ext import commands
import json

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        if amount > 1000:
            return await ctx.send("Too many messages, limit is 1k", delete_after=10)
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        if amount >= 2:
            await ctx.send(f"Purged {amount} mesages", delete_after=10)
        else:
            await ctx.send(f"Purged {amount} message", delete_after=10)

def setup(bot):
    bot.add_cog(Moderation(bot))
        

