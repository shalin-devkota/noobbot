import discord
from discord.ext import commands
import json


#WORK IN PROGRESS! FINAL VERSION RELEASING SOON!

class blacklist(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def blacklist(self,ctx, member:discord.Member):
        
        with open("blacklist.json","r") as f:
            State=json.load(f)

        State[str(member.id)]="1"

        with open("blacklist.json","w") as f:
            json.dump(State,f,indent=4)

    @commands.command()
    async def unblacklist(self,ctx, member:discord.Member):
        
        with open("blacklist.json","r") as f:
            State=json.load(f)

        State[str(member.id)]="0"

        with open("blacklist.json","w") as f:
            json.dump(State,f,indent=4)
        



   
    @commands.command()
    async def blacklistcheck(self,ctx,member:discord.Member):
        with open("blacklist.json","r") as f:
            State=json.load(f)
        try:
            if State[str(member.id)] == "1":
                await ctx.send("Member is blacklisted.")
            else:
                await ctx.send("Member is not blacklisted currently. Said member was blacklisted in the past and removed from it later on.")
        except KeyError:
            await ctx.send("Member is not blacklisted.")







def setup(client):
    client.add_cog(blacklist(client))
