# The libraries im gonna be using
import discord
import json
import time
import os
import logging
from discord.ext import commands

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Getting token and prefix from a seperate file
with open("preferences.json") as f:
    t = json.load(f)
    token = t["token"]
    prefix = t["prefix"]

# Setting up the bot
bot = commands.Bot(command_prefix=prefix)

# From https://gist.github.com/InterStella0/b78488fb28cadf279dfd3164b9f0cf96
class CustomHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)
    
    async def send_command_help(self, command):
        embed = discord.Embed(colour=discord.Colour.purple(), title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
    
        channel = self.get_destination()
        await channel.send(embed=embed)

bot.help_command = CustomHelp()

# On ready function to let me know when the bot is online
@bot.event
async def on_ready():
    print("Bot online")
    print(f"Ready for commands in {len(bot.guilds)} server(s)")
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            bot.load_extension(f"cogs.{file[:-3]}")
            print(f"loaded cog: {file}")

@bot.command()
async def ping(ctx):
    # From Modelmat#8218's tag in discord.py discord server
    start = time.perf_counter()
    message = await ctx.send("Pong!")
    end = time.perf_counter()
    duration = (end - start) * 1000
    await message.edit(content='Pong! {:.2f}ms'.format(duration))

# The code above is pretty much the only thing thats gonna be in this file for now for commands i'm gonna be using cogs because its much faster
# The code below is all for loading/unloading cogs

@bot.command()
async def load(ctx, *, cog):
    bot.load_extension(f"cogs.{cog}")
    await ctx.send(f"Loaded cog: {cog}")

@bot.command()
async def unload(ctx, cog):
    bot.unload_extension(f"cogs.{cog}")
    await ctx.send(f"Unloaded cog: {cog}")

@bot.command()
async def reload(ctx, ext):
    bot.reload_extension(f"cogs.{ext}")
    await ctx.send(f"Reloaded cog: {ext}")

bot.run(token)
