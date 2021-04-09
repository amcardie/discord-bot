import discord
from discord.ext import commands
import asyncio

def getMemberRoles(member):
    mroles = []
    for role in member.roles:
        if role.name != "@everyone":
            mroles.append(role)
    return mroles

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 10):
        """
        Purges number of messages.
        """
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
        """
        Kicks a given member.
        """
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
        """
        Bans a given member.
        """
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
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member = None, time: int = 1, s: str = 'm'):
        """
        Mutes a given member.
        """
        if not member:
            return await ctx.send("You need to mention people to mute", delete_after=5)
        
        role = discord.utils.get(ctx.guild.roles, name="Muted")

        memroles = getMemberRoles(member)

        if not role:
            return await ctx.send("Couldn't find mute role, make sure theres a role called 'Muted'")

        for memrole in memroles:
            await member.remove_roles(memrole)

        if self.bot.user == member:
            return await ctx.send("I can't mute myself")
        else:
            await member.add_roles(role)
            await ctx.send(f"Muted {member} for {time} {s}")

            if s == "s":
                await asyncio.sleep(time)
            elif s == "m":
                await asyncio.sleep(time * 60)
            elif s == "h":
                await asyncio.sleep(time*60*60)
            elif s == "d":
                await asyncio.sleep(time*60*60*24)
            
            await member.remove_roles(role)
            await ctx.send(f"automatically unmuted {member}")

            for memrole in memroles:
                await member.add_roles(memrole)
    
def setup(bot):
    bot.add_cog(Moderation(bot))
        
