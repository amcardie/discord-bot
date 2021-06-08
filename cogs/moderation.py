import discord
from discord.ext import commands
import re
import asyncio

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k] * float(v)
            except KeyError:
                raise commands.BadArgument(f"{k} is an invalid time key, h/m/s/d are valid")
            except ValueError:
                raise commands.BadArgument(f"{v} is not a number")
        return time

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount: int = 1):
        """
        Purges number of messages.
        """
        if amount > 500:
            return await ctx.reply("Too many messages, limit is 500", delete_after=3)
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        if amount >= 2:
            await ctx.send(f"Purged {amount} mesages", delete_after=3)
        else:
            await ctx.send(f"Purged {amount} message", delete_after=3)
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):
        """
        Kicks a given member.
        """
        if reason is None:
            reason = f"No reason given, kicked by {ctx.author}"

        if reason:
            reason += f" kicked by {ctx.author}"

        if member is None:
            return await ctx.reply("Please specify a member to kick", delete_after=5)

        if member.id == self.bot.user.id:
            return await ctx.reply("I cant kick myself", delete_after=5)

        try:
            await member.kick(reason=reason)
            await ctx.reply(f"{member.name} has been kicked for `{reason}`")

        except Exception as e:
            await ctx.reply(e, delete_after=5)
            return print(e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.User = None, *, reason: str = None):
        """
        Bans a given member.
        """
        try:
            if user is None:
                return await ctx.reply("Please specify a member to ban", delete_after=3)
                
            if user.id == self.bot.user.id:
                return await ctx.reply("I can't ban myself", delete_after=3)

            if reason is None:
                reason = f"banned by {ctx.author.name}"
                await ctx.guild.ban(discord.Object(id=user.id), reason=f"banned by {ctx.author.name}")
                return await ctx.reply(f"{user.mention} has been banned", mention_author=False)

            else:
                await ctx.reply(f"{user.mention} has been banned for **`{reason}`**", mention_author=False)
                reason += f" banned by {ctx.author.name}"
                await ctx.guild.ban(discord.Object(id=user.id), reason=reason)

        except Exception as e:
            await ctx.reply(e, delete_after=5)
            return print(e)

    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User = None):
        if member is None:
            return

        else:
            try:
                await ctx.guild.unban(member)
                await ctx.reply(f"Unbanned {member.name}")
                
            except Exception as e:
                print(e)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, time:TimeConverter = None):
        """Mutes a member for the specified time"""

        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        await ctx.reply((f"Muted {member} for {time}s" if time else f"Muted {member}"))

        if time:
            await asyncio.sleep(time)
            await member.remove_roles(role)
    
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if not member:
            return await ctx.reply("You need to mention someone to unmute", delete_after=5)
        
        role = discord.utils.get(ctx.guild.roles, name="Muted")
    
        if not role:
            return
        
        if self.bot.user == member:
            return

        else:
            if role in member.roles:
                await member.remove_roles(role)
                await ctx.reply(f"Unmuted {member.mention}")
            else:
                await ctx.reply(f"{member.name} is not muted")
        
def setup(bot):
    bot.add_cog(Moderation(bot))
