import discord
from discord.ext import commands
import json

def write_json(data, filename="logging.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["log", "lc"])
    async def logchannel(self, ctx, channel: discord.TextChannel = None):
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
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.bot.user.id:
            return
        else:
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