import discord
from discord.ext import commands,tasks
from datetime import datetime
import json
import asyncio
import random



class Events(commands.Cog):
    def __init__(self,client):
        self.client=client

    #@commands.Cog.listener()
    #async def on_message(self,message):
       


    @commands.Cog.listener()
    async def on_ready (self):
        
        f=open("status.txt","r") #reads the status from the file and sets it in line 25
        playing=f.read()
        f.close()
        global time
        time=datetime.now().time().minute
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game(playing))
        print("Bot is ready")

    
    @commands.Cog.listener()
    async def on_member_join(self,member):
        
        print(f"{member} has joined a server.")
        with open("blacklist.json","r") as f:
            State=json.load(f)
        
        if State[str(member.id)] == "1":
            await member.ban(reason="blacklist")

   

        
        
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        print(f"{member} has left a server.")


    #@commands.Cog.listener()
    #async def on_message_delete(self,message):
    #   channel=message.channel
    #   await channel.send(message.content)






def setup(client):
    client.add_cog(Events(client))

