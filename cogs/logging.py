import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import json

def write_json(data, filename="logging.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def log(self, ctx, channel: discord.TextChannel =  None):
        """
        Enables logging.
        """
        if channel is None:
            return await ctx.send("Please specify a channel to send logs to")

        ap = {}
        with open("logging.json") as pre:
            data = json.load(pre)
            for x in data:
                if x["channel_id"] == str(channel.id):
                    return await ctx.reply(f"{channel.mention} is already this servers logging channel", mention_author=False)
                if x["server_id"] == str(ctx.guild.id):
                    x["channel_id"] = str(channel.id)

                    await ctx.reply(f"I've changed this servers logging channel to {channel.mention}", mention_author=False)
                    return write_json(data)
        
        ap["server_id"] = str(ctx.guild.id)
        ap["channel_id"] = str(channel.id)
        data.append(ap)

        await ctx.reply(f"I've made this servers logging channel: {channel.mention}", mention_author=False)
        return write_json(data)

    @commands.command(aliases=["rlogs", "dlogs"])
    @commands.has_permissions(manage_guild=True)
    async def removelogs(self, ctx):
        """
        Disables logging for current server
        """
        new_data = []
        with open("logging.json", "r") as f:
            temp = json.load(f)
        
        for entry in temp:
            if entry["server_id"] == str(ctx.guild.id):
                pass
            else:
                new_data.append(entry)

        await ctx.reply("Successfully removed this servers logging", mention_author=False)
        write_json(new_data)
   
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.bot.user.id: return
        with open("logging.json") as pre:
            data = json.load(pre)
            for key in data:
                if key["server_id"] == str(message.guild.id):
                    ft = "gif" if message.author.is_avatar_animated() else "png"
                    now = datetime.now()

                    embed = discord.Embed(title=f"Message deleted in {message.channel.name}", colour=discord.Colour.purple())
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url_as(format=ft))

                    embed.add_field(name=f"**{message.content}**", value=f"\u200b")
                    embed.set_footer(text=f"Author ID: {message.author.id} | Message ID: {message.id}\nChannel ID: {message.channel.id} | Time: {now.strftime('%Y-%m-%d %I:%M:%S')}")

                    channel = self.bot.get_channel(int(key['channel_id']))
                    return await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.id == self.bot.user.id: return
        with open("logging.json") as pre:
            data = json.load(pre)
            for key in data:
                if key["server_id"] == str(after.guild.id):
                    ft = "gif" if after.author.is_avatar_animated() else "png"
                    now = datetime.now()

                    embed = discord.Embed(title=f"Message edited in {after.channel.name}", colour=discord.Colour.purple())
                    embed.set_author(name=after.author.name, icon_url=after.author.avatar_url_as(format=ft))

                    embed.add_field(name="Before Edit:", value=before.content)
                    embed.add_field(name="After Edit:", value=after.content, inline=False)

                    embed.set_footer(text=f"Author ID: {after.author.id}\nChannel ID: {after.channel.id} | Time: {now.strftime('%Y-%m-%d %I:%M:%S')}")

                    channel = self.bot.get_channel(int(key['channel_id']))
                    return await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        with open("logging.json") as f:
            data = json.load(f)
        
        await asyncio.sleep(1)
        
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            audit = entry

        for key in data:
            if key["server_id"] == str(guild.id):
                ft = "gif" if user.is_avatar_animated() else "png"
                now = datetime.now()

                embed = discord.Embed(description=f"{user} has been banned", colour=discord.Colour.purple())
                embed.set_author(name=user.name, icon_url=user.avatar_url_as(format=ft))
                embed.add_field(name="Member Info", value=f"```Name: {user}\nID: {user.id}```", inline=False)
                embed.add_field(name="Reason:", value=audit.reason, inline=False)
                embed.set_footer(text=f"{audit.user} | {now.strftime('%D %I:%M:%S %p')}", icon_url=audit.user.avatar_url_as(format=ft))

                channel = self.bot.get_channel(int(key['channel_id']))
                await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        with open("logging.json") as f:
            data = json.load(f)
        
        await asyncio.sleep(1)
        
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.unban):
            audit = entry
        
        for key in data:
            if key["server_id"] == str(guild.id):
                ft = "gif" if user.is_avatar_animated() else "png"
                now = datetime.now()

                embed = discord.Embed(description=f"{user} has been unbanned", colour=discord.Colour.purple())
                embed.set_author(name=user.name, icon_url=user.avatar_url_as(format=ft))
                embed.add_field(name="Member Info", value=f"```Name: {user}\nID: {user.id}```", inline=False)
                embed.set_footer(text=f"{audit.user} | {now.strftime('%D %I:%M:%S %p')}", icon_url=audit.user.avatar_url_as(format=ft))

                channel = self.bot.get_channel(int(key["channel_id"]))
                await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Logging(bot))
