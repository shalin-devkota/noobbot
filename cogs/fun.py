import discord
from discord.ext import commands
import random
import requests
import asyncio

activeChannels=[]

class Fun(commands.Cog):
    def __init__(self,client):
        self.client=client

    @commands.command()
    async def gaytest(self,ctx,user):
        a=random.randint(1,100)
        await ctx.send(f"{user} is {a} percent gay :gay_pride_flag:")

    @commands.command()
    async def doge(self,ctx):
        await ctx.send("All hail!")
        await ctx.send("https://imgur.com/a/F4ZoZ9e")

    @commands.command()
    async def roast(self,ctx,user):
        oneliners=["Is your ass jealous of the amount of shit that just came out of your mouth?",
               "It's better to let someone think you are an Idiot than to open your mouth and prove it.",
               "If I wanted to kill myself I'd climb your ego and jump to your IQ.",
               "You have two parts of brain, 'left' and 'right'. In the left side, there's nothing right. In the right side, there's nothing left.",
               "Two wrongs don't make a right, take your parents as an example.",
               "He is so old that he gets nostalgic when he sees the Neolithic cave paintings.",
               "Your family tree must be a cactus because everybody on it is a prick.",
               "You're old enough to remember when emojis were called hieroglyphics.",
               "Your birth certificate is an apology letter from the condom factory.",
               "You're so ugly, when your mom dropped you off at school she got a fine for littering.",
               "You must have been born on a highway because that's where most accidents happen.",
               "I don't engage in mental combat with the unarmed.",
               "I'd like to see things from your point of view but I can't seem to get my head that far up my ass."]

        a=random.randint(1,12)
        await ctx.send(f"{user} {oneliners[a]}")

    @roast.error 
    async def roast_error(self,ctx,error):
     if isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("I need someone to roast!")


    @commands.command()
    async def dank(self,ctx,member: discord.Member):
        role=discord.utils.get(ctx.guild.roles,name="dank")
        await member.add_roles(role)

    @commands.command()
    async def normie(self,ctx,member: discord.Member):
        role=discord.utils.get(ctx.guild.roles,name="normie")
        await member.add_roles(role)

    @commands.command()
    async def chuck(self,ctx):
        request=requests.get("https://api.chucknorris.io/jokes/random")

        chuck_json=request.json()

        await ctx.send(chuck_json['value'])

    @commands.command()
    async def rhyme(self,ctx,word):
        MessageToSend=""
        parameter={"rel_rhy":word}
        request = requests.get("https://api.datamuse.com/words",parameter)

        rhyme_json= request.json()
        for i in rhyme_json[0:3]:
            RhymeWordFetcher=(i['word'])
            MessageToSend=MessageToSend+ "  "+RhymeWordFetcher

        embed=discord.Embed(
        
        colour=discord.Colour.blue()
        )
        embed.set_footer(text="Powered by datamuse!")
        embed.add_field(name="Rhyme :musical_note: ", value=MessageToSend)
    
        await ctx.send(embed=embed)

    @rhyme.error
    async def rhyme_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("What word would you like to get the rhyming word for?")

    @commands.command()
    async def bigtext(self,ctx,*,a):
        counter= len(a)
        a=a.lower()
        flag=int(counter)
        final=""
        for i in range (0,flag):
            letters=a[i]
            if letters=="1":
                extracter=":one:"
            elif letters=="2":
                extracter=":two:"
            elif letters=="3":
                extracter=":three:"
            elif letters=="4":
                extracter=":four:"
            elif letters=="5":
                extracter=":five:"
            elif letters=="6":
                extracter=":six:"
            elif letters=="7":
                extracter=":seven:"
            elif letters=="8":
                extracter=":eight:"
            elif letters=="9":
                extracter=":nine:"
            elif letters=="0":
                extracter=":zero:"
            elif letters==" " :
                extracter="   "
            else:
                extracter=":regional_indicator_"+letters+": "
            final=final+extracter
        await ctx.send(final)

    
    @commands.command(aliases=["8ball"])
    async def _8ball(self,ctx,*,question):
        responses = ["Yes","No"]
        if question=="Is venom gay?":
            await ctx.send(f"Nah mate. But you surely are")
        else:
            await ctx.send(f"Question: {question} \n Answer: {random.choice(responses)}")

    @_8ball.error
    async def _8ball_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please also input a question.")

    @commands.command()
    async def toss(self,ctx):
        responses =["Heads","Tails"]
        await ctx.send(f"You got a {random.choice(responses)}")


    @commands.command ()
    async def dice(self,ctx):
        responses=random.randint(1,6)
        await ctx.send(f"You got a {responses}.")
    

    @commands.command()
    async def rps(self,ctx,player):
        o=["rock","paper","scissors"]
        computer = random.choice(o)
        if player=="rock" or player=="paper" or player=="scissors":
            await ctx.send (computer)
        else:
            await ctx.send("Wrong input!")
        
        if player==computer:
            await ctx.send(f"Draw!")
        elif player=="rock" and computer=="paper":
            await ctx.send("You lost!")
        elif player=="rock" and computer =="scissors":
            await ctx.send("You won!")
        elif player=="scissors" and computer=="rock":
            await ctx.send("You lost!")
        elif player=="scissors" and computer=="paper":
            await ctx.send("You won")
        elif player=="paper" and computer=="rock":
            await ctx.send("You won")
        elif player=="paper" and computer =="scissors":
            await ctx.send("You lost")
    
    @rps.error
    async def rps_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Please input your choice.")

    @commands.command()
    async def say(self,ctx,a):
        await ctx.send(f"I'm not your slave fuck off and say it yourself.")

    @say.error
    async def say_error(self,ctx,error):
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Say wat?")

  




  
        
    @commands.command()
    async def fight(self,ctx,enemy:discord.Member):
        channel = ctx.message.channel
        channelState= checkChannel (channel)
        if channelState == "False":
            activeChannels.append(channel)
            
            Challenger= ctx.message.author
            ChallengerHP= 100
            
            EnemyHP=100
            def CheckAccept(message):
                
                return message.content=="accept" and message.author==enemy
            
            await ctx.send(f"{enemy.mention} {ctx.message.author.name} has invited you to a duel!Type `accept` in chat to accept!")
            try:
                await self.client.wait_for('message',check=CheckAccept,timeout=30)
            
            
                
                #GameState= "Started"
                firstMove=["author","enemy"]
                turn=random.choice(firstMove)
                await ctx.send("Acccepted! The game will start in 5 seconds. Get ready!")
                await asyncio.sleep(5)
                i= 1
                while ChallengerHP > 0 and EnemyHP>0:
                    print (i)
                    i +=1 
                    if turn=="author":
                        await ctx.send(f"{Challenger.mention} make your move! You can either `slap` `punch` or `kick`.")
                        def CheckChallengerMessage(message):
                            fightMoves= ['punch','kick','slap']
                            
                            return message.content.lower() in fightMoves and message.author == Challenger
                        try:
                            fightMove= await self.client.wait_for('message',check=CheckChallengerMessage,timeout=30)
                        except asyncio.TimeoutError:
                            await ctx.send(f"{Challenger.name} didn't respond in time!")
                            break
                        damage = random.randint(2,30)
                        EnemyHP = EnemyHP - damage
                        if EnemyHP < 0 :
                            EnemyHP = 0
                        embed = challengerHit(enemy,Challenger,damage,ChallengerHP,EnemyHP,fightMove)
                        await ctx.send(embed=embed)
                        turn = "enemy"
                        
                    else:
                        
                        await ctx.send(f"{enemy.mention} make your move! You can either `slap` `punch` or `kick`.")
                        def CheckEnemyMessage(message):
                            fightMoves = ['punch','kick','slap']
                            return message.content.lower() in fightMoves and message.author==enemy
                        try:
                            fightMove =await self.client.wait_for('message',check=CheckEnemyMessage,timeout= 30)
                        except asyncio.TimeoutError:
                            await ctx.send(f"{enemy.name} didn't respond in time!")
                            break
                        damage = random.randint(2,30)
                        ChallengerHP = ChallengerHP - damage
                        if ChallengerHP < 0:
                            ChallengerHP = 0
                        embed = enemyHit (enemy,Challenger,damage,ChallengerHP,EnemyHP,fightMove)
                        await ctx.send(embed=embed)
                        turn="author"
                        
                        
                        
                    
                if ChallengerHP > EnemyHP :
                    await ctx.send(f"{Challenger.mention} won with {ChallengerHP} hp remaining.")
                else:
                    await ctx.send(f"{enemy.mention} won with {EnemyHP} hp remaining.")
                activeChannels.remove(channel)
            except asyncio.TimeoutError:
                await ctx.send(f"{enemy.mention} didn't accept in time! Pfft.")
                
                activeChannels.remove(channel) 
    
        else:
            await ctx.send("There is already an ongoing fight in this channel. Please use another channel.")
        
        


def enemyHit(enemy,challenger,damage,ChallengerHP,EnemyHP,fightMove):
    embed = discord.Embed(
        colour= discord.Colour.red(),
        title= "Fight results",
        description= f"{enemy.name}  {fightMove.content}ed {challenger.name}  and dealt  **{damage}** damage!"
    )
    embed.add_field(name=f"{challenger.name}'s HP",value=ChallengerHP)
    embed.add_field(name=f"{enemy.name}'s HP",value=EnemyHP)
    return embed
      
def challengerHit(enemy,challenger,damage,ChallengerHP,EnemyHP,fightMove):
    embed = discord.Embed(
        colour= discord.Colour.red(),
        title= "Fight results",
        description= f"{challenger.name}  {fightMove.content}ed {enemy.name}  and dealt  **{damage}** damage!"
    )
    embed.add_field(name=f"{challenger.name}'s HP",value=ChallengerHP)
    embed.add_field(name=f"{enemy.name}'s HP",value=EnemyHP)
    return embed         


def checkChannel(channel):
    if channel in activeChannels:
        rValue = "True"
    else:
        rValue = "False"
    
    return rValue

def setup(client):
    client.add_cog(Fun(client))









