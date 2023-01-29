import discord
from discord.ext import commands

class Mod(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def kick(self,ctx, member: discord.Member,*,reason=None):
        if ctx.message.author.guild_permissions.administrator:
            await member.kick(reason=reason)
            await ctx.send(f"Admin has kicked {member} for {reason}")
        else:
            await ctx.send(f"You do not have the necessary permissions to carry out this action.")
    
    @kick.error
    async def kick_error(self,ctx,error):
     if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("Please mention the name of the user to kick.")
 
    @commands.command()
    async def ban(self,ctx, member : discord.Member,*, reason=None):
        if ctx.message.author.guild_permissions.administrator:
            await member.ban(reason=reason)
            await ctx.send(f"Admin has banned {member} for {reason}")
        else:
            await ctx.send(f"You do not have the necessary permissions to carry out this action.")


    @ban.error
    async def  ban_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please mention the name of the user to ban.")
   

    @commands.command()
    async def mute(self,ctx,member:discord.Member,reason=None):
   
        role=discord.utils.get(ctx.guild.roles,name="muted")
        if ctx.message.author.guild_permissions.administrator:
            await member.add_roles(role)
            await ctx.send(f"Admin {ctx.message.author} Muted {member} for {reason}")
        else:
            await ctx.send(f"You do not have the necessary permissions to carry out this action.")


    @commands.command()
    async def unmute(self,ctx,member:discord.Member,*,reason=None):
        role=discord.utils.get(ctx.guild.roles,name="muted")
        await member.remove_roles(role)
        await ctx.send(f"Unmuted {member}")

    @mute.error
    async def  mute_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Whom do I mute m'lord?")

    @unmute.error
    async def  unmute_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Whom do I unmute m'lord?")

    @commands.command()
    async def clear(self,ctx,amount=5):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def slowmode(self,ctx,*,time=10):
        if ctx.message.author.guild_permissions.administrator: 
            await ctx.channel.edit(slowmode_delay=time)
            await ctx.message.delete()
        else:
            await ctx.send("You aint got dem perms.")

    @commands.command()
    async def settopic(self,ctx,*,topic):
        if ctx.message.author.guild_permissions.administrator:
            await ctx.channel.edit(topic=topic)
            await ctx.message.delete()
        else:
            await ctx.send("You aint got dem perms!")




def setup(client):
    client.add_cog(Mod(client))

