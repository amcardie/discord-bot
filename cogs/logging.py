import discord
from discord.ext import commands
import json

def write_json(data, filename="logging.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def log(self, ctx):
        return await ctx.send(f"Availabe log commands: channel, enable, disable. Note: Log comes defaulted as disabled so you must do {ctx.prefix}log enable after/before setting channel")
    
    @log.command()
    async def channel(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            return await ctx.send("Please specify a channel to send logs to")
        ap = {
            "server_id": str(ctx.guild.id),
            "channel_id": str(channel.id)
        }

        with open("logging.json") as json_file:
            data = json.load(json_file)
            temp = data["logs"]
            y = ap
            for key in temp:
                if key['server_id'] == str(ctx.guild.id):
                    key['channel_id'] = str(channel.id)
                    write_json(data)
                    return

            temp.append(y)
            write_json(data)
    
    @log.command()
    async def enable(self, ctx):
        ap = {
            "server_id": str(ctx.guild.id),
            "logdelete": "True",
            "logedit": "True"
        }
        with open("lp.json") as json_file:
            data = json.load(json_file)
            for key in data["prefs"]:
                if key['server_id'] == str(ctx.guild.id):
                    if key['logdelete'] and key['logedit'] == "True":
                        return await ctx.send("Logging already enabled")
                    else:
                        key['logdelete'] = "True"
                        key['logedit'] = "True"
                        write_json(data)
                        return
        
            data.append(ap)
            write_json(data)
    
    @log.command()
    async def disable(self, ctx):
        ap = {
            "server_id": str(ctx.guild.id),
            "logdelete": "False",
            "logedit": "False"
        }
        with open("lp.json") as json_file:
            data = json.load(json_file)
            for key in data["prefs"]:
                if key['server_id'] == str(ctx.guild.id):
                    if key["logdelete"] and key["logedit"] == "False":
                        return await ctx.send("Logging already disabled")
                    else:
                        key['logdelete'] = "False"
                        key['logedit'] = "False"
                        write_json(data)
                        return
        
            data.append(ap)
            write_json(data)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.bot.user.id:
            return
        with open("lp.json") as pre:
            pref = json.load(pre)
            for key in pref["prefs"]:
                if key["server_id"] == str(message.guild.id):
                    if key["logedit"] == "True":
                        with open("logging.json") as json_file:
                            data = json.load(json_file)
                            ft = "gif" if message.author.is_avatar_animated() else "png"
                            embed = discord.Embed(title=f"Message deleted in {message.channel.name}", colour=discord.Colour.purple())
                            embed.set_author(name=message.author.name, icon_url=message.author.avatar_url_as(format=ft))
                            embed.add_field(name=f"**{message.content}**", value=f"\u200b")
                            embed.set_footer(text=f"Author ID: {message.author.id} | Message ID: {message.id}")

                            for key in data["logs"]:
                                if key['server_id'] == str(message.guild.id):
                                    chid = int(key['channel_id'])
                                    channel = self.bot.get_channel(chid)
                                    await channel.send(embed=embed)
                                    return
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.id == self.bot.user.id:
            return
        with open("lp.json") as pre:
            pref = json.load(pre)
            for key in pref["prefs"]:
                if key["server_id"] == str(after.guild.id):
                    if pref["logedit"] == "True":
                        if before != after:
                            with open("logging.json") as json_file:
                                data = json.load(json_file)
                                ft = "gif" if after.author.is_avatar_animated() else "png"
                                embed = discord.Embed(title=f"Message edited in {after.channel.name}", colour=discord.Colour.purple())
                                embed.set_author(name=after.author.name, icon_url=after.author.avatar_url_as(format=ft))
                                embed.add_field(name="Before Edit:", value=before.content)
                                embed.add_field(name="After Edit:", value=after.content, inline=False)

                                for key in data["logs"]:
                                    if key['server_id'] == str(after.guild.id):
                                        chid = int(key['channel_id'])
                                        channel = self.bot.get_channel(chid)
                                        await channel.send(embed=embed)
                                        return


def setup(bot):
    bot.add_cog(Logging(bot))
