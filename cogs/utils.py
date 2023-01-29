import discord
from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup as soup
import os 
import json
import asyncio
import sqlite3
import datetime

conn=sqlite3.connect('bugs.db')
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS bugs (bugid TEXT,bug TEXT,reporter TEXT, guild TEXT,date TEXT,status INT)")
conn.commit()
c.close()
conn.close()
BUG_CHANNEL_ID = ""
OWNER_ID = " "
class Utils(commands.Cog):
    def __init__(self,client):
        self.client=client


    @commands.command()
    async def ping(self,ctx):
        lag=round(self.client.latency*1000)
        embed=discord.Embed(
        
            colour=discord.Colour.blue()
        )
        embed.add_field(name="Ping! :ping_pong:", value=lag)
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self,ctx):
    
        embed=discord.Embed(
            title= "Blacklist commands",
            description="These are all the available blacklist commands.",
            colour= discord.Colour.red()

        )   
        embed.set_footer(text="Experimental feature!Contact Rusher#3394 to report bugs")  
    
        embed.set_author(name="NoobBot",
        icon_url="https://cdn.discordapp.com/attachments/585061146541686794/586085286648348672/botdp.jpg")
        embed.add_field(name="blacklist",value="Adds a member to the blacklist",inline=False)
        embed.add_field(name="unblacklist",value="Removes a user from the blacklist",inline=False)
        embed.add_field(name="blacklistcheck",value="Checks if the user is blacklisted.",inline=False)

        embed_one=discord.Embed(
            title= "Economy commands.",
            description="These are all the available economy commands.",
            colour= discord.Colour.green()

        )   
        embed_one.set_footer(text="Contact Rusher#3394 to report bugs")  
    
        embed_one.set_author(name="NoobBot",
        icon_url="https://cdn.discordapp.com/attachments/585061146541686794/586085286648348672/botdp.jpg")
        embed_one.add_field(name="balance",value="Shows your current balance.You begin with $5000.",inline=False)
        embed_one.add_field(name="bet",value="Bets the specified amount of money. You win if you roll a higher number than the bot.\n The cooldown is 10 seconds.",inline=False)
        embed_one.add_field(name="jobs",value="Lists the available jobs.You may choose a new one every 3 hours.",inline=False)   
        embed_one.add_field(name="startjob",value="Starts the specified job",inline=False)
        embed_one.add_field(name="myjob",value="Shows your current job.",inline=False)
        embed_one.add_field(name="resign",value="Resigns from your current job.",inline=False)
    
        embed_two=discord.Embed(
                title= "Fun commands.",
                description="These are all the available fun commands.",
                colour= discord.Colour.gold()
        )   
        embed_two.set_footer(text="Contact Rusher#3394 to report bugs")  
        
        embed_two.set_author(name="NoobBot",
        icon_url="https://cdn.discordapp.com/attachments/585061146541686794/586085286648348672/botdp.jpg")
        embed_two.add_field(name="gaytest",value="Runs a gaytest on someone. Usually accurate",inline=False)
        embed_two.add_field(name="doge",value="Try it!",inline=False)
        embed_two.add_field(name="roast",value="Roasts someone.",inline=False)
        embed_two.add_field(name="dank",value="Makes someone dank.",inline=False)
        embed_two.add_field(name="normie",value="Makes someone a normie.",inline=False)
        embed_two.add_field(name="chuck",value="Tells you a random chuck norris joke.",inline=False)
        embed_two.add_field(name="rhyme",value="Shows you the rhyming words for a given word.",inline=False)
        embed_two.add_field(name="bigtext",value="Converts the given message into big texts!",inline=False)
        embed_two.add_field(name="8ball",value="Answers with a yes or no. Must be supplied with a question.",inline=False)
        embed_two.add_field(name="toss",value="Tosses a coin.",inline=False)
        embed_two.add_field(name="dice",value="Rolls a dice.",inline=False)
        embed_two.add_field(name="rps",value="Starts the rock paper scissors game.\n Syntax: rps [rock,paper or scissor]",inline=False)
        embed_two.add_field(name="say",value="Says something. Or does it..?",inline=False)

        embed_three=discord.Embed(
                title= "Moderation commands.",
                description="These are all the available Moderation commands.",
                colour= discord.Colour.blue()
        )   
        embed_three.set_footer(text="Contact Rusher#3394 to report bugs")  
        
        embed_three.set_author(name="NoobBot",
        icon_url="https://cdn.discordapp.com/attachments/585061146541686794/586085286648348672/botdp.jpg")
        embed_three.add_field(name="kick",value="Kicks a member.",inline=False)
        embed_three.add_field(name="ban",value="Bans a member",inline=False)
        embed_three.add_field(name="mute",value="Mutes a member. \n Please ensure you have a muted role all set up.",inline=False)
        embed_three.add_field(name="unmute",value="Unmutes a muted member.",inline=False)
        embed_three.add_field(name="clear",value="Clears a given number of messages.\n Default value for number of messages that are cleared is 5",inline=False)
        embed_three.add_field(name="slowmode",value="Implements a slowmode in the channel for given seconds.\n The default slowmode is 10 seconds long.\n To remove the slowmode , use slowmode 0 in the channel with slowmode.",inline=False)
        embed_three.add_field(name="settopic",value="Sets the topic of the channel the command in run in.",inline=False)

        embed_four=discord.Embed(
            title= "Utility commands.",
            description="These are all the available Utility commands.",
            colour= discord.Colour.purple()

        )   
        embed_four.set_footer(text="Contact Rusher#3394 to report bugs")  
    
        embed_four.set_author(name="NoobBot",
        icon_url="https://cdn.discordapp.com/attachments/585061146541686794/586085286648348672/botdp.jpg")
        embed_four.add_field(name="ping",value="Shows your latency to the bot.",inline=False)
        embed_four.add_field(name="help",value="Displays this message.",inline=False)
        embed_four.add_field(name="bug",value="Reports a bug to the developer.",inline=False)

        

        embed_five=discord.Embed(
            title= "Reddit commands.",
            description="These are all the available Utility commands.",
            colour=0xFF5700

        )   
        embed_five.set_footer(text="Contact Rusher#3394 to report bugs")  
    
        embed_five.set_author(name="NoobBot",
        icon_url="https://cdn.discordapp.com/attachments/585061146541686794/586085286648348672/botdp.jpg")
        embed_five.add_field(name="subreddit [subredditname]",value="Shows you the information on a subreddit.",inline=False)
        embed_five.add_field(name="redditor [redditusername]",value="Shows you the information of a reddit user",inline=False)
        embed_five.add_field(name="srsearch [subreddit] [query]",value="Searches the mentioned subreddit for your query",inline=False)
        embed_five.add_field(name="rsearch [query]",value="Searches reddit for your query",inline=False)
        embed_five.add_field(name="hot [subreddit]",value="Shows you the 10 hottest posts from the mentioned subreddit",inline=False)
        embed_five.add_field(name="nosleep/ns ",value="Sends a random story from r/nosleep into the channel",inline=False)
        embed_five.add_field(name="ra/relationshipadvice ",value="Sends a random post from r/relationship_advice to the channel",inline=False)
        embed_five.add_field(name="tifu ",value="Sends a random post from r/tifu to the channel",inline=False)
        embed_five.add_field(name="st/showerthoughts ",value="Sends a random post from r/Showerthoughts to the channel",inline=False)
        embed_five.add_field(name="meme ",value="Sends a random meme from either r/memes or r/dankmemes ",inline=False)

        

        await ctx.author.send(embed=embed)
        await ctx.author.send(embed=embed_one)
        await ctx.author.send(embed=embed_two)
        await ctx.author.send(embed=embed_three)
        await ctx.author.send(embed=embed_four)
        await ctx.author.send(embed=embed_five)
        
        await ctx.send(f"Check your DMS! {ctx.author.mention} ")

    #BUG REPORTING SYSTEM UPDATE SOON!
    @commands.command()
    async def bug(self,ctx,*,bug):
        BugID= ctx.message.id
        channel=self.client.get_channel(BUG_CHANNEL_ID)
        reporter=ctx.message.author.id
        guild=ctx.message.guild.id
        date= datetime.date.today()
        conn=sqlite3.connect('bugs.db')
        c=conn.cursor()
        c.execute("INSERT INTO bugs (bugid,bug,reporter,guild,date,status) VALUES (?,?,?,?,?,?)",(BugID,bug,reporter,guild,date,0))
        conn.commit()
        
        
        c.close()
        conn.close()
        embed=discord.Embed(
            colour=discord.Colour.red(),
            description = f"{bug}"
        )
        embed.set_author(name="Bug reported!")
        embed.set_footer(text=f"BugID : {BugID}")
        
        await channel.send(embed=embed)
        embed=discord.Embed(
            colour=discord.Colour.green(),
            description="The bug has been reported successfully"
        )
        embed.set_author(name="Bug reported!")
        await ctx.send(embed=embed)

    @commands.command()
    async def markbug(self,ctx,bugid,pstatus):
        Check = is_owner(ctx.message.author.id)
        if Check=="Yes":
            pstatus=pstatus.lower()
            status={
                "solved":1,
                "pending":2,
                "nei":3,
                "nab":4
            }
            conn=sqlite3.connect('bugs.db')
            c=conn.cursor()
            try:
                c.execute(f"UPDATE bugs SET status={status[pstatus]} WHERE bugid={bugid}")
                
                c.execute(f"SELECT reporter FROM bugs WHERE bugid={bugid}")
                reporter=c.fetchone()
                reporter=reporter[0]
                reporter = self.client.get_user(int(reporter))
                
                c.execute(f"SELECT bug FROM bugs WHERE bugid={bugid}")
                bug=c.fetchone()
                
                
                conn.commit()
                c.close()
                conn.close()
                await ctx.send(f"The bug has been marked as {pstatus.title()}.")
            except KeyError:
                await ctx.send("Invalid bug status!")
        else:
            await ctx.send("Only the developer can run this command!")

        embed=discord.Embed(
            colour=0x6B6AB5,
            description= f"The dev team has responded to your bug report! It has been marked as {pstatus}."
        )
        embed.add_field(name="You reported:",value=bug[0])
        embed.set_author(name="Bug report update!")
        await reporter.send(embed=embed)

    @commands.command()
    async def buginfo(self,ctx,bugid):
        status={
                "0" :"Unresolved",
                "1":"Solved",
                "2":"Pending",
                "3":"NEI",
                "4":"NAB"
            }
        conn=sqlite3.connect('bugs.db')
        c=conn.cursor()
        c.execute(f"SELECT * FROM bugs WHERE bugid={bugid}")
        buginfo=c.fetchone()
        BugId= buginfo[0]
        Bug= buginfo[1]
        ReportedBy= buginfo[2]
        ReportedInGuild= buginfo[3]
        ReportDate= buginfo[4]
        BugStatus= status[buginfo[5]]

        
        embed=discord.Embed(
            colour=discord.Colour.red(),
            description= Bug

        )
        embed.set_author(name="Bug info!")
        embed.add_field(name="BugId  ",value=BugId)
        embed.add_field(name="Bug status  ",value=BugStatus)
        embed.add_field(name="Report Date  ",value=ReportDate)
        embed.add_field(name="Reported By  ",value=ReportedBy)
        embed.add_field(name="Reported in guild  ",value=ReportedInGuild)
        
        await ctx.send(embed=embed)
        



    @commands.command()
    async def motdset(self,ctx,*,message):
        f=open("motd.txt","w+")
        f.write(message)
        f.close()
        global motd_message
        author=ctx.message.author.id #Gets the authors id.
        OwnerCheck=is_owner(author)
        if OwnerCheck== "Yes":
            motd_message= message
        else:
            await ctx.send("Only the bot owner can run this command.")

    @commands.command()
    async def motd(self,ctx):
        f=open("motd.txt","r")
        motd_message=f.read()
        f.close()
    
        embed=discord.Embed(
            colour=discord.Colour.green(),
        )
        embed.add_field(name="Message of the day",value=motd_message)
        await ctx.send(embed=embed)

    @commands.command()
    async def playing(self,ctx,*,game):
        f=open("status.txt","w+")
        f.write(game)
        f.close()
        author=ctx.message.author.id #gest the author's id.
        OwnerCheck=is_owner(author)
        print(OwnerCheck)
        if OwnerCheck =="Yes":
            await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game(game))
        else:
            await ctx.send("Only the bot owner can run this command!")


    
    @commands.command()
    async def setrole(self,ctx,member: discord.Member,role):
        if ctx.message.author.guild_permissions.administrator: 
            role=discord.utils.get(ctx.guild.roles,name=role)
            if role in ctx.guild.roles:
                await member.add_roles(role)
            else:
                await ctx.send("The mentioned role does not exist.")
        else:
            await ctx.send("You don't have the required permissions to perform this action.")
  
   
    @setrole.error
    async def  setrole_error(self,ctx,error):
        if isinstance(error,commands.MissingPermissions):
            await ctx.send("I don't have the required permission to do this.")


    @commands.command()
    async def changenick(self,ctx,member:discord.Member,*,nick):
        if ctx.message.author.guild_permissions.administrator:
            await member.edit(nick=nick)
            await ctx.send(f"Done!")

    @changenick.error
    async def changenick_error(self,ctx,error):
        if isinstance (error,commands.MissingPermissions):
            await ctx.send("I don't have the required permission to carry this action and/or the specified user has a higher role than me!")
        elif isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please specify all the needed parmateres.")

   
    
    @commands.command()
    async def corona(self,ctx):
        my_url='https://www.worldometers.info/coronavirus/'
        headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers'}
        page= requests.get(my_url, headers= headers)
       
        page_soup=soup(page.text,"html.parser")
        Cases=page_soup.findAll("div",{"class":"maincounter-number"})
        CaseNumber= Cases[0].text
        DeathNumber=Cases[1].text
        RecoveredNumber= Cases[2].text
        Date=page_soup.find("div",{"style":"font-size:13px; color:#999; margin-top:5px; text-align:center"})
        print(Date)
        embed=discord.Embed(
            colour=discord.Colour.red(),
            title=f"Corona Virus Status - {Date.text}"
        )
        embed.set_footer(text=f"The numbers represent an approximate value and are not 100% accurate")
        embed.add_field(name="Number of identified cases",value=CaseNumber)
        embed.add_field(name="Number of confirmed deaths",value=DeathNumber)
        embed.add_field(name="Number of recovered cases",value=RecoveredNumber)


        await ctx.send(embed=embed)
   
    
    
        
   
    @commands.command()
    async def invite(self,ctx):
        await ctx.send("https://discordapp.com/api/oauth2/authorize?client_id=584402956804161536&permissions=8&scope=bot")
        

    @commands.command(aliases=["reminder","rem"])
    async def remindme(self,ctx,hour,minute,second,*,message):
        ihour = int(hour)*60*60
        iminute= int(minute)*60
        second= int(second)
        time = ihour+iminute+second
        embed=discord.Embed(
            colour= discord.Colour.green(),
            description=f"Reminder set  for {hour}:{minute}:{second}!"
        )
        embed.set_author(name="⏰Reminder")
        await ctx.send(embed=embed)
        time = int(time)
        author=ctx.message.author
        await asyncio.sleep(time)
        embed=discord.Embed(
            colour=discord.Colour.red(),
            description=f"{message}"
        )
        embed.set_footer(text=f"Reminder was set in {ctx.message.guild}")
        embed.set_author(name="⏰Reminder!")
        await author.send(embed=embed)

    @remindme.error
    async def remindme_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please input the reminder time in H-M-S format (use space instead of -)")


    
        

def is_owner(id):
    if id==ONWER_ID:  
        Check="Yes"
    else:
        Check="No"
    return Check

    



        
   
        
        



       


            




            
        
            
        
        


            
        
def setup(client):
    client.add_cog(Utils(client))
