import discord 
from discord.ext import commands, tasks
from discord.utils import get
import os
import asyncio
import random
import json



client = commands.Bot(command_prefix=">",case_insensitive=True)
owner_id=OWNER_ID
client.remove_command("help")


#loads all the cogs inside the cogs folder on startup
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')    


@client.command()
#to load a cog
async def load(ctx,cname):
    author=ctx.message.author.id #gets the author's id.
    if author==OWNER_ID: #checks if the authors id matches the owner's id.
        client.load_extension(f"cogs.{cname}")
        await ctx.send(f"Successfully loaded {cname}")
    else:
        await ctx.send("Only the bot owner can use this command.")

@client.command()
# to unload a cog
async def unload(ctx,cname):
    author=ctx.message.author.id #gets the author's id.
    if author==OWNER_ID: #checks if the authors id matches the owner's id.
        client.unload_extension(f"cogs.{cname}")
        await ctx.send(f"Successfully unloaded {cname}")
    else:
        await ctx.send("Only the bot owner can use this command!")
    
@client.command()
#to reaload an ALREADY LOADED cog
async def reload(ctx,cname):
    author=ctx.message.author.id #gest the author's id.
    if author==397648789793669121: #checks if the authors id matches the owner's id.
        client.unload_extension(f"cogs.{cname}")
        client.load_extension(f"cogs.{cname}")
        await ctx.send(f"Successfully reloaded {cname}.")
    else:
        await ctx.send("Only the bot owner can use this command!")





client.run(BOT_TOKEN)



 

