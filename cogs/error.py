import discord
import traceback
import sys
from discord.ext import commands

class Error(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, "on_error"):
            return
        
        embed = discord.Embed(title="Error!")
        if isinstance(error, commands.CommandNotFound):
            embed.add_field(name=f"Command not found", value=f"`{error}`")
        else:
            embed.add_field(name=f"Error in command '**{ctx.command}**'", value=f"`{error}`")

        await ctx.send(embed=embed)

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(Error(bot))
