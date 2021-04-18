import discord
import mystbin
import json

from discord.ext import commands
from datetime import datetime

"""
Using mystbin to make logging much more clean
You'll need to install the correct library to use this, https://pypi.org/project/mystbin.py/ or pip install mystbin.py
"""

class Myst(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.myst = mystbin.Client()

    @commands.Cog.listener()
    async def on_message(self, message):
        if len(message.attachments) == 1:
            attachment = message.attachments[0]
            if not attachment.filename.endswith(('.txt', '.py', '.json')):
                return

            try:
                contents = await attachment.read()
                contents = contents.decode('utf-8')
            except (UnicodeDecodeError, discord.HTTPException):
                return
            
            if attachment.filename.endswith('.txt'):
                paste = await self.myst.post(contents, syntax="text")
            elif attachment.filename.endswith('.py'):
                paste = await self.myst.post(contents, syntax="python")
            else:
                paste = await self.myst.post(contents, syntax="json")

            await message.delete()        
            await message.channel.send(f"Automatically uploaded file to {paste.url}")

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == self.bot.user.id:
            return
        with open("logging.json") as pre:
            data = json.load(pre)
            for key in data["logs"]:
                if key["server_id"] == str(message.guild.id):
                    now = datetime.now()
                    paste = await self.myst.post(f"Message Content: {message.content}\n\nAuthor: {message.author.name} | {message.author.id}\nChannel: {message.channel.name} | {message.channel.id}\nMessage ID: {message.id}\nTime: {now.strftime('%Y-%m-%d %I:%M:%S')}", syntax="python")
                    channel = self.bot.get_channel(int(key['channel_id']))
                    await channel.send(f"Message deleted uploaded to {paste.url}")

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.id == self.bot.user.id:
            return
        with open("logging.json") as pre:
            data = json.load(pre)
            for key in data["logs"]:
                if key["server_id"] == str(after.guild.id):
                    now = datetime.now()
                    paste = await self.myst.post(f"Message before edit: {before.content}\n\nMessage after edit: {after.content}\n\nAuthor: {after.author.name} | {after.author.id}\nChannel: {after.channel.name} | {after.channel.id}\nMessage ID: {after.id}\nTime: {now.strftime('%Y-%m-%d %I:%M:%S')}", syntax="python")
                    channel = self.bot.get_channel(int(key['channel_id']))
                    await channel.send(f"Message edit uploaded to {paste.url}")

def setup(bot):
    bot.add_cog(Myst(bot))

