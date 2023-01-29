#Yes i can make functions for the embeds
#Yes i only realized that after finishing coding
#No i wont edit it now
#If it aint broken dont fix it
#Dont judge me
#Bye



import praw
import discord
from discord.ext import commands,tasks
from datetime import datetime
import requests
import json
import os
import random

reddit=praw.Reddit(client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                username=USERNAME,
                password=PASSWORD,
                user_agent=USER_AGENT
            )


class Reddit(commands.Cog):
    def __init__(self,client):
        self.client= client

    @commands.command()
    async def subreddit(self,ctx,sName):
        try:
            await ctx.send("Fetching subreddit info...")
            subreddit= reddit.subreddit(sName)
            displayName= subreddit.display_name
            description = subreddit.public_description
            isNSFW = subreddit.over18
            subscribers= subreddit.subscribers
            icon= subreddit.icon_img
            dateCreated = subreddit.created_utc
            dateCreated=dateCreated=datetime.utcfromtimestamp(dateCreated).strftime('%Y-%m-%d ')
            color = 0xFF5700
                

            embed=discord.Embed(
                title=f"r/{displayName}",
                color = color,
                description= f"{description}"
            )
            embed.set_author(name=f"Reddit info")
            embed.set_thumbnail (url=icon)
            embed.add_field(name="Subscribers:",value = subscribers,inline=False)
            embed.add_field(name="NSFW:",value=isNSFW,inline=False)
            embed.add_field(name="Created at:",value=dateCreated)
            
            
            await ctx.send (embed=embed)
        except Exception as e:
            await ctx.send("No subreddit found!")    

    @commands.command()
    async def redditor(self,ctx,redditorName):
        redditor = reddit.redditor(redditorName)
        userName= redditor.name
        commentKarma= redditor.comment_karma
        linkKarma= redditor.link_karma
        premium = redditor.is_gold
        icon=redditor.icon_img
        dateCreated = redditor.created_utc
        dateCreated=datetime.utcfromtimestamp(dateCreated).strftime('%Y-%m-%d ')
        color = 0xFF5700
        embed=discord.Embed(
            color= color,
            title=f"u/{userName}",
            description = f"[Click here to view {userName}'s reddit profile](https://reddit.com/user/{userName})"

        )
        embed.set_author(name="Redditor lookup")
        embed.add_field(name="Link Karma",value=linkKarma)
        embed.add_field(name="Comment Karma",value=commentKarma)
        embed.add_field(name="Premium",value=premium)
        embed.add_field(name="Join Date",value=dateCreated)
        
        embed.set_thumbnail(url=icon)
        comments = redditor.comments.new(limit= 3)
        for comment in comments:
            embed.add_field(name=f"Commented on {comment.subreddit}",value=f"{comment.body[0:60]}......[Full comment](https://reddit.com/{comment.permalink})",inline=False)
        
        await ctx.send(embed=embed)

    @commands.command()
    async def srsearch(self,ctx,subName,query):
        num= 1
        subreddit= reddit.subreddit(subName)
        icon=subreddit.icon_img
        color = 0xFF5700
        embed=discord.Embed(
            color=color,
            description = f"Search results for {query} in r/{subName}",
        )
        for result in subreddit.search(query,limit =5):
            
            embed.add_field(name=f"Search results #{num}",value=f"{result.title[0:120]}... \n[VIEW POST]({result.url})\n",inline=False)
            num = num+1
        embed.set_thumbnail(url=icon)        
        await ctx.send(embed=embed)

    @commands.command()
    async def rsearch(self,ctx,query):
        
        subreddit= reddit.subreddit('all')
        
        color = 0xFF5700

        embed=discord.Embed(
            color=color,
            description = f"Search results for {query}",
        )
        for result in subreddit.search(query,limit =5):
            
            embed.add_field(name=f"Posted in r/{result.subreddit}",value=f"{result.title[0:120]}... \n[VIEW POST]({result.url})\n",inline=False)
            
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/589083129852198914/706922330240057354/3928_SN_Reddit_512x512.png')        
        await ctx.send(embed=embed)

    @commands.command()
    async def hot(self,ctx,subreddit):
        subreddit= reddit.subreddit(subreddit)
        
        embed=discord.Embed(
            title=f"r/{subreddit}",
            description= f"The 10 hottest posts in r/{subreddit}",
            color=0xFF5700
        )
        for hot in subreddit.hot(limit=10):
            embed.add_field(name=f"Posted by {hot.author.name} ({hot.ups} upvotes)",value=f"[{hot.title}]({hot.url})",inline=False)
            
        embed.set_thumbnail(url=subreddit.icon_img)
        await ctx.send(embed=embed)

    @commands.command(aliases=['ns'])
    async def nosleep(self,ctx):
        color=0xFF5700
        maxMessageLen = 1800
        subreddit= reddit.subreddit('nosleep')
        post = subreddit.random()
        postContent = post.selftext
        postLength = len(post.selftext)
        oneMessageLen = 1800
        embed=discord.Embed(
            color=color,
            title=f"{post.title}",
            description= f"[Click here to view the post on reddit]({post.url})"
        )
        embed.set_author(name=f"Posted by u/{post.author}")
        embed.set_thumbnail(url=post.author.icon_img)
        await ctx.send(embed=embed)
        
        embed=discord.Embed(
            color=color,
            description = post.selftext [0:oneMessageLen]
        )
        await ctx.send(embed=embed)
        
        while postLength > oneMessageLen:
            
            embed=discord.Embed(
                color=color,
                description = post.selftext [oneMessageLen: oneMessageLen +1800]
        )
            oneMessageLen = oneMessageLen +1800
            await ctx.send(embed=embed)

        embed=discord.Embed(
            color=color,
            title="End of story",
            description=f"If you enjoyed this story then please [upvote it on reddit]({post.url}) and appreciate the writer"
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/498812163776053253/707145057509179494/8f23ec4c40984427e44c0d55d9bab4de_according-to-jardon-this-post-should-be-upvoted-because-it-_413-549.png')
        embed.set_footer(text=f'Submission ID: {post.id}')
        await ctx.send(embed=embed)

    @commands.command()
    async def upvote(self,ctx,ID):
        color=0xFF5700
        submission = reddit.submission(id=ID)
        if ctx.message.author.id==397648789793669121:
            
            submission.upvote()
            embed=discord.Embed(
                color=color,
                description="Upvoted!"
                
            )
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(
                color= discord.Color.red(),
                description= f"Sorry! Only the bot owner can run this command.However, you can [upvote this post here]({submission.url})."
            )
            await ctx.send(embed=embed)


    @commands.command(aliases=['relationshipadvice','radvice'])
    async def ra(self,ctx):
        
        color=0xFF5700
        maxMessageLen = 1800
        subreddit= reddit.subreddit('relationship_advice')
        post=subreddit.random()
       
        postContent = post.selftext
        postLength = len(post.selftext)
        oneMessageLen = 1800
        embed=discord.Embed(
            color=color,
            title=f"{post.title}",
            description= f"[Click here to view the post on reddit]({post.url})"
        )
        embed.set_author(name=f"Posted by u/{post.author}")
        embed.set_thumbnail(url=post.author.icon_img)
        await ctx.send(embed=embed)
        
        embed=discord.Embed(
            color=color,
            description = post.selftext [0:oneMessageLen]
        )
        await ctx.send(embed=embed)
        
        while postLength > oneMessageLen:
            
            embed=discord.Embed(
                color=color,
                description = post.selftext [oneMessageLen: oneMessageLen +1800]
        )
            oneMessageLen = oneMessageLen +1800
            await ctx.send(embed=embed)

        embed=discord.Embed(
            color=color,
            title="End of post",
            description=f"If you enjoyed this post then please [upvote it on reddit]({post.url})."
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/498812163776053253/707145057509179494/8f23ec4c40984427e44c0d55d9bab4de_according-to-jardon-this-post-should-be-upvoted-because-it-_413-549.png')
        embed.set_footer(text=f'Submission ID: {post.id}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['st'])
    async def showerthoughts(self,ctx):
        
        color=0xFF5700
        maxMessageLen = 1800
        subreddit= reddit.subreddit('Showerthoughts')
        post=subreddit.random()
       
        postContent = post.selftext
        postLength = len(post.selftext)
        oneMessageLen = 1800
        embed=discord.Embed(
            color=color,
            title=f"{post.title}",
            description= f"[Click here to view the post on reddit]({post.url})"
        )
        embed.set_author(name=f"Posted by u/{post.author}")
        embed.set_thumbnail(url=post.author.icon_img)
        await ctx.send(embed=embed)
        if postLength !=0:
            embed=discord.Embed(
                color=color,
                description = post.selftext [0:oneMessageLen]
            )
            await ctx.send(embed=embed)
            
            while postLength > oneMessageLen:
                
                embed=discord.Embed(
                    color=color,
                    description = post.selftext [oneMessageLen: oneMessageLen +1800]
            )
                oneMessageLen = oneMessageLen +1800
                await ctx.send(embed=embed)
            else:
                pass
        #embed=discord.Embed(
        #    color=color,
        #    title="End of post",
        #    description=f"If you enjoyed this story then please [upvote it on reddit]({post.url})."
        #)
        #embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/498812163776053253/707145057509179494/8f23ec4c40984427e44c0d55d9bab4de_according-to-jardon-this-post-should-be-upvoted-because-it-_413-549.png')
        #embed.set_footer(text=f'Submission ID: {post.id}')
        #await ctx.send(embed=embed)

    

    @commands.command(aliases=['tifu'])
    async def todayifuckedup(self,ctx):
        
        color=0xFF5700
        maxMessageLen = 1800
        subreddit= reddit.subreddit('tifu')
        post=subreddit.random()
       
        postContent = post.selftext
        postLength = len(post.selftext)
        oneMessageLen = 1800
        embed=discord.Embed(
            color=color,
            title=f"{post.title}",
            description= f"[Click here to view the post on reddit]({post.url})"
        )
        embed.set_author(name=f"Posted by u/{post.author}")
        embed.set_thumbnail(url=post.author.icon_img)
        await ctx.send(embed=embed)
        if postLength !=0:
            embed=discord.Embed(
                color=color,
                description = post.selftext [0:oneMessageLen]
            )
            await ctx.send(embed=embed)
            
            while postLength > oneMessageLen:
                
                embed=discord.Embed(
                    color=color,
                    description = post.selftext [oneMessageLen: oneMessageLen +1800]
            )
                oneMessageLen = oneMessageLen +1800
                await ctx.send(embed=embed)
            else:
                pass
        embed=discord.Embed(
            color=color,
            title="End of post",
            description=f"If you enjoyed this post then please [upvote it on reddit]({post.url})."
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/498812163776053253/707145057509179494/8f23ec4c40984427e44c0d55d9bab4de_according-to-jardon-this-post-should-be-upvoted-because-it-_413-549.png')
        embed.set_footer(text=f'Submission ID: {post.id}')
        await ctx.send(embed=embed)

    @commands.command()
    async def meme(self,ctx):
        subreddits=['memes','dankmemes']
        subreddit=reddit.subreddit(random.choice(subreddits))
        
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers'}
        post = subreddit.random()
        redditLink= 'https://reddit.com/'+post.permalink
        memeer= post.author
        upvotes= post.ups
        postURL= post.url
        image=  requests.get(postURL)
        with open(f'{ctx.message.id}.png','wb') as f:
            f.write(image.content)
        
        myfile= discord.File(f'{ctx.message.id}.png')
        embed=discord.Embed(
            color=0xFF5700,
            
            description=f"**[{post.title}]({redditLink})**"
        )
        embed.set_footer(text=f"Posted by {post.author} in r/memes")
        embed.set_image(url=f"attachment://{ctx.message.id}.png")
        await ctx.send(file=myfile,embed=embed)
        
        os.remove(f"{ctx.message.id}.png")

    
    
    @commands.command()
    async def upvote(self,ctx,ID):
        color=0xFF5700
        submission = reddit.submission(id=ID)
        if ctx.message.author.id==397648789793669121:
            
            submission.upvote()
            embed=discord.Embed(
                color=color,
                description="Upvoted!"
                
            )
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(
                color= discord.Color.red(),
                description= f"Sorry! Only the bot owner can run this command.However, you can [upvote this post here]({submission.url})."
            )
            await ctx.send(embed=embed)
        


def setup(client):
    client.add_cog(Reddit(client))
