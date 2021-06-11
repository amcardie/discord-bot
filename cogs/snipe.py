import discord
from discord.ext import commands
import json
from disputils import BotEmbedPaginator

def Reverse(lst):
    return [ele for ele in reversed(lst)]

def write_snipes(data, filename="snipes.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def write_edits(data, filename="editsnipes.json"):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.bot.user.id: return

        ap = {}
        with open("snipes.json") as f:
            data = json.load(f)
        
        ap["channel_id"] = str(message.channel.id)
        ap["server_id"] = str(message.guild.id)
        ap["message_content"] = str(message.content)
        ap["message_author"] = str(message.author)
        data.append(ap)
        write_snipes(data)
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.id == self.bot.user.id: return

        ap = {
            "channel_id": str(after.channel.id),
            "server_id": str(after.guild.id),
            "before": str(before.content),
            "after": str(after.content),
            "message_author": str(after.author)
        }
        with open("editsnipes.json") as pre:
            data = json.load(pre)
        
        data.append(ap)
        write_edits(data)
    
    @commands.command(aliases=["s"])
    async def snipe(self, ctx):
        """
        Show most recently deleted message + more
        """
        with open("snipes.json") as f:
            data = json.load(f)
        
        embeds = []
        
        for x in data:
            if x["server_id"] == str(ctx.guild.id):
                if x["channel_id"] == str(ctx.channel.id):
                    channel = self.bot.get_channel(int(x["channel_id"]))
                    author = x["message_author"]
                    content = x["message_content"]
                    embeds  += [discord.Embed(title="Message Snipe", description=f"{author} deleted message in {channel.name}:\n```{content}```", colour=discord.Colour.purple())]
        
        embeds = Reverse(embeds)

        try:
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
        except IndexError:
            await ctx.send("No deleted messages in this channel")

    @commands.command(aliases=["es", "esnipe"])
    async def editsnipe(self, ctx):
        """
        Show most recently edited message + more
        """
        with open("editsnipes.json") as f:
            data = json.load(f)
        
        embeds = []
        
        for x in data:
            if x["server_id"] == str(ctx.guild.id):
                if x["channel_id"] == str(ctx.channel.id):
                    channel = self.bot.get_channel(int(x["channel_id"]))
                    author = x["message_author"]
                    before = x["before"]
                    after = x["after"]
                    embeds  += [discord.Embed(title="Message Edit Snipe", description=f"{author} edited message in {channel.name}:\n\nBefore: `{before}`\nAfter: `{after}`", colour=discord.Colour.purple())]
        
        embeds = Reverse(embeds)

        try:
            paginator = BotEmbedPaginator(ctx, embeds)
            await paginator.run()
        except IndexError:
            await ctx.send("No edited messages in this channel")

                
def setup(bot):
    bot.add_cog(Snipe(bot))
