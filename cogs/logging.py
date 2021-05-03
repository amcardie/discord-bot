import discord
from discord.ext import commands
from datetime import datetime
import json

def write_json(data, filename="logging.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def write_pref(data, filename="logging.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def log(self, ctx, channel: discord.TextChannel = None):
        """
        Enables Logging.
        """
        if channel is None:
            return await ctx.send("Please specify a channel to send logs to")

        ap = {
            "server_id": str(ctx.guild.id),
            "channel_id": str(channel.id),
        }
        with open("logging.json") as pre:
            data = json.load(pre)
            
        temp = data["logs"]
        y = ap
        write_json(data)

        temp.append(y)
        write_json(data)
   
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.bot.user.id: return
        with open("logging.json") as pre:
            data = json.load(pre)
            for key in data["logs"]:
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
            for key in data["logs"]:
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

def setup(bot):
    bot.add_cog(Logging(bot))
