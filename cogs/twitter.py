"""

  I reccommend creating a new twitter account and using that instead of a personal twitter account, not mandatory
  You need to sign up for a developer account at https://developer.twitter.com/en/apply-for-access to use this correctly
  
  I used Twython for this because it seemed pretty easy, learn the basics at https://twython.readthedocs.io/en/latest/usage/starting_out.html
  
"""


import discord
from discord.ext import commands
import discord.utils
import requests
import shutil
from twython import Twython
from secret import secrets

class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitter = Twython(secrets.get('api'), secrets.get('api-secret'), secrets.get('access'), secrets.get('access-secret'))

    @commands.command()
    @commands.has_permissions(administrator=True) # Remove this if you want anyone to be able to tweet
    async def tweet(self, ctx, *, content: str = None):
        if not content:
            return await ctx.send("You need to put something to omething to tweet")
        else:
            self.twitter.update_status(status=content)
            tweet = self.twitter.get_user_timeline(screen_name="your_accounts_username", count=1)
            gettweet = [d['id'] for d in tweet]
            tweetid = gettweet[0]
            url = f"https://twitter.com/oogoog13/status/{tweetid}"
            await ctx.send(url)
    
    @commands.command(aliases=["search"])
    @commands.has_permissions(administrator=True) # Remove this if you want anyone to be able to search up tweets
    async def searchtweets(self, ctx, *, query: str = None):
        if query is None:
            return await ctx.send("You need a term to search")
        else:
            results = self.twitter.search(q=query, count=3, result_type='recent')
            result = results['statuses']
            for tweet in result:
                await ctx.send(f"```{tweet['text']}```")
    
    @commands.command()
    @commands.has_permissions(administrator=True) # Remove this if you want anyone to be able to follow people
    async def follow(self, ctx, user: str = None):
        if user is None:
            return await ctx.send("You need to give a person to follow")
        else:
            self.twitter.create_friendship(screen_name=user)
            await ctx.send(f"Followed https://twitter.com/{user}")
    
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.message.guild.id) == "your_guild_id": # You can remove this if you want this to be done in every server your bot is in
            if str(reaction.emoji.name) == "tweet":
                if reaction.count >= 3:
                    if reaction.message.attachments[0]:
                        image_url = reaction.message.attachments[0].url
                        filename = "capture.png"
                        r = requests.get(image_url, stream = True)
                        if r.status_code == 200:
                            r.raw.decode_content = True
                            with open(filename,'wb') as f:
                                shutil.copyfileobj(r.raw, f)
                            
                            print("Image sucessfully Downloaded")
                        else:
                            print("Image Couldn't be retreived")
                        
                        photo = open('capture.png', 'rb')
                        response = self.twitter.upload_media(media=photo)

                        if reaction.message.content:
                            try:
                                self.twitter.update_status(status=reaction.message.content, media_ids=[response['media_id']])
                            except Exception:
                                await ctx.send("Something went wrong")
                        else:
                            try:
                                self.twitter.update_status(status=None, media_ids=[response['media_id']])
                            except Exception:
                                await ctx.send("Something went wrong")
                    else:
                        try:
                            self.twitter.update_status(status=reaction.message.content)
                        except Exception:
                            await ctx.send("Something went wrong")

                    tweet = self.twitter.get_user_timeline(screen_name="oogoog13", count=1)
                    gettweet = [d['id'] for d in tweet]
                    tweetid = gettweet[0]
                    url = f"https://twitter.com/oogoog13/status/{tweetid}"
                    await reaction.message.channel.send(url)                   

def setup(bot):
    bot.add_cog(Twitter(bot))
