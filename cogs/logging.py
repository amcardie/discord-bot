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

def setup(bot):
    bot.add_cog(Logging(bot))
