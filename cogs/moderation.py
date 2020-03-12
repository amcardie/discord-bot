import discord
from discord.ext import commands
import asyncio
import json

def write_json(data, filename="logging.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

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
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, reason: str = None):
        if reason is None:
            reason = "No reason given"
        if member is None:
            return await ctx.send("Please specify a member to kick", delete_after=5)
        if member.id == self.bot.user.id:
            return await ctx.send("I cant kick myself", delete_after=5)
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member.name} has been kicked for `{reason}`")

        except Exception as e:
            await ctx.send(e, delete_after=5)
            return print(e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None, reason: str = None):
        if reason is None:
            reason = "No reason given"
        if member is None:
            return await ctx.send("Please specify a member to ban", delete_after=5)
        if member.id == self.bot.user.id:
            return await ctx.send("I can't ban myself", delete_after=5)
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.name} has been banned for `{reason}`")

        except Exception as e:
            await ctx.send(e, delete_after=5)
            return print(e)

    @commands.command()
    @commands.has_permissions(manage_members=True)
    async def mute(self, ctx, members: discord.Member = None, mutetime: int = 0):
        if not members:
            return await ctx.send("You need to mention people to mute", delete_after=5)

        role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not role:
            return await ctx.send("Couldn't find mute role, make sure theres a role called 'Muted'")

        for member in members:
            if self.bot.user == member:
                return await ctx.send("I can't mute myself")
            else:
                await member.add_roles(role)
                if mutetime > 0:
                    await ctx.send(f"Muted {member.name} for {mutetime * 60} minutes")
                elif mutetime == 0:
                    await ctx.send(f"Muted {member.name}")
        
        if mutetime > 0:
            while role in ctx.author.roles:
                await asyncio.sleep(mutetime*60)
                for member in members:
                    await member.remove_roles(role)
                    await ctx.send(f"{member.name} automatically unmuted")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, members: discord.Member = None):
        if not members:
            return await ctx.send("You need to mention people to mute", delete_after=5)

        role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not role:
            return await ctx.send("Couldn't find mute role, make sure theres a role called 'Muted'")

        for member in members:
            if self.bot.user == member:
                return await ctx.send("I can't unmute myself because I can't be muted")
            else:
                await member.remove_roles(role)
                await ctx.send(f"Unmuted {member.name}")
        
def setup(bot):
    bot.add_cog(Moderation(bot))
        

