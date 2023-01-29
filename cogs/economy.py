import discord
from discord.ext import commands
import sqlite3
import random

conn=sqlite3.connect('userdata.db')
c=conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS userbal (userid TEXT,bal INT)")
conn.commit()
c.close()
conn.close()




class Economy(commands.Cog):
    def __init__(self,client):
        self.client=client


    @commands.command()
    async def bal(self,ctx,user:discord.Member=0):
        if user == 0:
            user = ctx.message.author
            
        entry_check_and_create(str(user.id))
        Balance = get_bal(user.id)

        embed=discord.Embed(
            colour=discord.Colour.gold(),
            title = f"**{user}'s balance**",
            description= f"You currently have ${Balance}."
        
        )
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/693104930717827092/693104965480087672/money_bag.png")
        await ctx.send(embed=embed)

   

    @commands.command()
    async def bet (self,ctx,amount):
        conn=sqlite3.connect('userdata.db')
        c=conn.cursor()
        entry_check_and_create(str(ctx.message.author.id))
        Balance = get_bal(ctx.message.author.id)
        #print(Balance)
        if Balance >= int(amount):
            BotRolled=random.randint(1,12)
            YouRolled=random.randint(1,12)
            if YouRolled > BotRolled:
                embed=discord.Embed(
                    colour=discord.Colour.gold(),
                    title="Win"
                )
                embed.set_author(name="Betting")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/693086568197390346/693131332271734916/Dice.png")
                embed.add_field(name="You rolled",value=YouRolled, inline=True)
                embed.add_field(name="Bot rolled",value=BotRolled, inline=True)
                embed.add_field(name="You won:",value= amount, inline=False)
                await ctx.send(embed=embed)
                
                NewBalance = Balance + int(amount)
                
                c.execute(f"UPDATE userbal SET bal={NewBalance} WHERE userid={str(ctx.message.author.id)}")
                conn.commit()
            elif YouRolled < BotRolled:
                NewBalance = Balance - int(amount)
                c.execute(f"UPDATE userbal SET bal={NewBalance} WHERE userid={str(ctx.message.author.id)}")
                conn.commit()
                
                embed=discord.Embed(
                    colour=discord.Colour.red(),
                    title="Loss"
                )
                embed.set_author(name="Betting")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/693086568197390346/693131332271734916/Dice.png")
                embed.add_field(name="You rolled",value=YouRolled, inline=True)
                embed.add_field(name="Bot rolled",value=BotRolled, inline=True)
                embed.add_field(name="You lost:",value= amount, inline=False)
                await ctx.send(embed=embed)
                
            else:
                embed=discord.Embed(
                    colour=discord.Colour.green(),
                    title="Draw"
                )
                embed.set_author(name="Betting")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/693086568197390346/693131332271734916/Dice.png")
                embed.add_field(name="You rolled",value=YouRolled, inline=True)
                embed.add_field(name="Bot rolled",value=BotRolled, inline=True)
                embed.add_field(name="Draw!",value= 0, inline=False)
                await ctx.send(embed=embed)

                
                

        else:
            await ctx.send("You don't have enough balance in your account to bet that much!")

        c.close()
        conn.close()

    @commands.command()
    async def pay(self,ctx,amount,user:discord.User):
        conn=sqlite3.connect('userdata.db')
        c=conn.cursor()
        PayerBalance = get_bal(ctx.message.author.id)
        ReceiverBalance= get_bal(user.id)
        entry_check_and_create(user.id)
        
        if PayerBalance >= int(amount):
            NewPayerBalance= PayerBalance - int(amount)
            NewReceiverBalance = ReceiverBalance + int(amount)
            c.execute(f"UPDATE userbal SET bal={NewPayerBalance} WHERE userid={ctx.message.author.id}")
            c.execute(f"UPDATE userbal SET bal={NewReceiverBalance} WHERE userid={user.id}")
            conn.commit()
            c.close()
            conn.close()
            await ctx.send("Payment successful!")
        else:
            await ctx.send("You don't have enough money to perform that transaction!")

    @commands.command()
    async def give(self,ctx,amount,user:discord.User):
        Check = is_owner(ctx.message.author.id)
        if Check== "Yes":
            conn=sqlite3.connect('userdata.db')
            c=conn.cursor()
            ReceiverBalance= get_bal(user.id)
            entry_check_and_create(user.id)
            NewReceiverBalance = ReceiverBalance + int(amount)
            c.execute(f"UPDATE userbal SET bal={NewReceiverBalance} WHERE userid={user.id}")
            conn.commit()
            c.close()
            conn.close()
            await ctx.send("Payment successful!")
        else:
            await ctx.send("Only the bot owner can run this command!")
        

    


def get_bal(passedid):
    conn=sqlite3.connect('userdata.db')
    c=conn.cursor()
    c.execute(f"SELECT bal FROM userbal WHERE userid={passedid}")
    bal= c.fetchone()
       
    if bal is None:
        Balance = 100
    if bal is not None:
        balint= int(bal[0])
        Balance = balint
    return Balance
    

def entry_check_and_create(userid):
    conn=sqlite3.connect('userdata.db')
    c=conn.cursor()
    c.execute(f"SELECT userid FROM userbal WHERE userid={userid}")
    result = c.fetchone()
    if result is None:
        c.execute(f"INSERT INTO userbal (userid,bal) VALUES(?,?)",(userid,100))
        conn.commit()
    if result is not None:
        pass
    
    c.close()
    conn.close()


def is_owner(id):
    if id==ONWER_ID:  
        Check="Yes"
    else:
        Check="No"
    return Check
 
def setup(client):
    client.add_cog(Economy(client))
