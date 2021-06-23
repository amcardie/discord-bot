# The libraries im gonna be using
import discord
import json
import time
import os
import logging
import asyncio
from discord.ext import commands
intents = discord.Intents.all()

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def get_prefix(bot, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

# Getting token from a seperate file
with open("token.json") as f:
    t = json.load(f)
    token = t["token"]

# Setting up the bot
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

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

@bot.command()
async def ping(ctx):
    # From Modelmat#8218's tag in discord.py discord server
    start = time.perf_counter()
    message = await ctx.send("Pong!")
    end = time.perf_counter()
    duration = (end - start) * 1000
    await message.edit(content='Pong! {:.2f}ms'.format(duration))

@bot.command()
@commands.has_permissions(administrator=True)
async def prefix(ctx, prefix = None):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    if not prefix:
        return await ctx.send(f"This servers prefix is `{ctx.prefix}`, to change it run the command again with the prefix you want at the end of the command. To add a space put space at the end of the prefix like [prefixspace]")
    
    if prefix.endswith("space"):
        prefix = prefix.replace("space", " ")
    
    prefixes[str(ctx.guild.id)] = prefix

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)
    
    await ctx.send(f"This servers prefix has been changed to `{prefix}`")

@bot.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = ";"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f)

# The code above is pretty much the only thing thats gonna be in this file for now for commands i'm gonna be using cogs because its much faster
# The code below is all for loading/unloading cogs

cogs = []
for cog in os.listdir("./cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        cogs.append(cog)
        bot.load_extension(f"cogs.{cog[:-3]}")

print("loaded " + ', '.join(cogs))
        

@bot.command()
async def load(ctx, *, cog):
    if not ctx.author.id == bot_owner_id: return
    bot.load_extension(f"cogs.{cog}")
    await ctx.send(f"Loaded cog: {cog}")

@bot.command()
async def unload(ctx, cog):
    if not ctx.author.id == bot_owner_id: return
    bot.unload_extension(f"cogs.{cog}")
    await ctx.send(f"Unloaded cog: {cog}")

@bot.command(aliases=["r"])
async def reload(ctx, ext = None):
    if not ctx.author.id == bot_owner_id: return
    cogs = "" 
    if not ext:
        for cog in os.listdir("./cogs"):
            if cog.startswith("_"):
                continue
            if cog.endswith(".py"):
                bot.reload_extension(f"cogs.{cog[:-3]}")
                cogs += f"{cog[:-3].upper()}, "
        await ctx.send(f"Reloaded```{cogs}```")
    else:
        bot.reload_extension(f"cogs.{ext}")
        return await ctx.send(f"Reloaded cog: {ext}")

bot.run(token)
