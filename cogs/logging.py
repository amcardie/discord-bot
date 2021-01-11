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

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_guild=True)
    async def log(self, ctx):
        return await ctx.send(f"Availabe log commands: channel, enable, disable. Note: Log comes defaulted as disabled so you must do {ctx.prefix}log enable after/before setting channel")
    
    # @log.command()
    # @commands.has_permissions(manage_guild=True)
    # async def channel(self, ctx, channel: discord.TextChannel = None):
    #     """
    #     Sets the channel for the logs to be sent to.
    #     """
    #     if channel is None:
    #       return await ctx.send("Please specify a channel to send logs to")
    #     ap = {
    #         "server_id": str(ctx.guild.id),
    #         "channel_id": str(channel.id)
    #     }

    #     with open("logging.json") as json_file:
    #         data = json.load(json_file)
    #         temp = data["logs"]
    #         y = ap
    #         write_json(data)

    #         temp.append(y)
    #         write_json(data)
    
    @log.command()
    @commands.has_permissions(manage_guild=True)
    async def enable(self, ctx, channel: discord.TextChannel = None):
        """
        Enables Logging.
        """
        if channel is None:
            return await ctx.send("Please specify a channel to send logs to")

        ap = {
            "server_id": str(ctx.guild.id),
            "channel_id": str(channel.id),
            "log": "True",
        }
        with open("logging.json") as json_file:
            data = json.load(json_file)
            for key in data["logs"]:
                 if key['server_id'] == str(ctx.guild.id):
                     if key["log"] == "True":
                        return await ctx.send("Logging already enabled")
                        
            temp = data["logs"]
            y = ap
            write_json(data)

            temp.append(y)
            write_json(data)
    
    # @log.command()
    # @commands.has_permissions(manage_guild=True)
    # async def disable(self, ctx):
    #     """
    #     Disables Logging.        
    #     """
    #     ap = {
    #         "server_id": str(ctx.guild.id),
    #         "log": "False",
    #     }
    #     with open("logging.json") as json_file:
    #         data = json.load(json_file)
    #         for key in data["logs"]:
    #             if key['server_id'] == str(ctx.guild.id):
    #                 if key["log"] == "False":
    #                     return await ctx.send("Logging already disabled")
    #                 else:
    #                     key['log'] = "False"
    #                     write_json(data)
    #                     return
        
    #         data.append(ap)
    #         write_json(ap)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.bot.user.id:
            return
        with open("logging.json") as pre:
            data = json.load(pre)
            for key in data["logs"]:
                if key["server_id"] == str(message.guild.id) and key["log"] == "True":
                    ft = "gif" if message.author.is_avatar_animated() else "png"
                    now = datetime.now()
                    embed = discord.Embed(title=f"Message deleted in {message.channel.name}", colour=discord.Colour.purple())
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url_as(format=ft))
                    embed.add_field(name=f"**{message.content}**", value=f"\u200b")
                    embed.set_footer(text=f"Author ID: {message.author.id} | Message ID: {message.id}\nChannel ID: {message.channel.id} | Time: {now.strftime('%Y-%m-%d %I:%M:%S')}")
                    for key in data["logs"]:
                        if key['server_id'] == str(message.guild.id):
                            chid = int(key['channel_id'])
                            channel = self.bot.get_channel(chid)
                            return await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.id == self.bot.user.id:
            return
        with open("logging.json") as pre:
            data = json.load(pre)
            for key in data["logs"]:
                if key["server_id"] == str(after.guild.id) and key["log"] == "True":
                            ft = "gif" if after.author.is_avatar_animated() else "png"
                            now = datetime.now()
                            embed = discord.Embed(title=f"Message edited in {after.channel.name}", colour=discord.Colour.purple())
                            embed.set_author(name=after.author.name, icon_url=after.author.avatar_url_as(format=ft))
                            embed.add_field(name="Before Edit:", value=before.content)
                            embed.add_field(name="After Edit:", value=after.content, inline=False)
                            embed.set_footer(text=f"Author ID: {after.author.id}\nChannel ID: {after.channel.id} | Time: {now.strftime('%Y-%m-%d %I:%M:%S')}")
                            for key in data["logs"]:
                                if key['server_id'] == str(after.guild.id):
                                    chid = int(key['channel_id'])
                                    channel = self.bot.get_channel(chid)
                                    return await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Logging(bot))
