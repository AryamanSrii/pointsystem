import discord, json
import asyncio
from discord.ext import commands

class Points(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def h(self, message):
        with open('points.json', 'r', encoding='utf8') as f:
            user = json.load(f)

        if str(message.guild.id) not in user:
            user[str(message.guild.id)] = {}

        if str(message.author.id) not in user[str(message.guild.id)]:
            user[str(message.guild.id)][str(message.author.id)] = {}
            user[str(message.guild.id)][str(message.author.id)]['level'] = 0
            user[str(message.guild.id)][str(message.author.id)]['exp'] = 0

            with open('points.json', 'w', encoding='utf8') as f:
                return json.dump(user, f,indent=5)

        user[str(message.guild.id)][str(message.author.id)]['exp'] += 1
        exp = user[str(message.guild.id)][str(message.author.id)]['exp']
        lvl = user[str(message.guild.id)][str(message.author.id)]['level']  + 1
        exps=[1]
        if lvl == 100000000000000000000000000000000:
                return

        while lvl > len(exps):
            exps.append(int(exps[-1] + exps[-1]/10))

            if lvl == len(exps):
              break

        lvl_end = exps[-1]
        with open('points.json', 'w', encoding='utf8') as f:
                    json.dump(user, f,indent=5)

        if lvl_end <= exp:
         user[str(message.guild.id)][str(message.author.id)]['exp'] = 1
         user[str(message.guild.id)][str(message.author.id)]['level'] +=1
         lvl = user[str(message.guild.id)][str(message.author.id)]['level']
         with open('points.json', 'w', encoding='utf8') as f:
              json.dump(user, f,indent=5)

        await message.channel.send(f'Congratulations,{message.author.mention} has got one <:coin:865205194454204436>')
        await message.channel.set_permissions(message.guild.default_role, send_messages=False)
        await message.channel.send("Channel <:lock:865209279665799178> for 120 Minutes")
        await asyncio.sleep(10)
        await message.channel.set_permissions(message.guild.default_role, send_messages=True)
        await message.channel.send('Channel <:unlock:865209752313135125>')
    
def setup(client):
    client.add_cog(Points(client))