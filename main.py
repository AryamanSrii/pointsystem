import discord
from discord.ext import commands, tasks
from discord.ext.commands import (CommandOnCooldown)
from discord.ext.commands import cooldown, BucketType
import asyncio
from itertools import cycle
import os
import json
import random

intents = discord.Intents.all()
client = commands.Bot(command_prefix='.', intents = intents)


@client.event
async def on_ready():
    print('Bot is ready')


for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'Cogs.{filename[:-3]}')


class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour = discord.Colour.red(), title = ":bookmark_tabs: | Help Menu")
            emby.set_thumbnail(url = "https://cdn.discordapp.com/avatars/566193564502196235/b624ea7737776938c070f6693c91abc9?size=2048")
            emby.set_footer(text = "Check Bot Status at https://RKS.aryamansri.repl.co ")
            await destination.send(embed=emby)

client.help_command = NewHelpName()

@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'Cogs.{extension}')
    await ctx.send('Succesfully loaded module')


@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'Cogs.{extension}')
    await ctx.send('Succesfully unloaded module')


@client.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f'Cogs.{extension}')
    await ctx.send('Succesfully reloaded module')


class CogName(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(CogName(bot))

@client.command(aliases=['lvl', 'rank'])
@cooldown(1, 5, BucketType.member)
async def level(ctx, member: discord.Member = None):
	if member == None:
		member = ctx.author
	with open('points.json', 'r', encoding='utf8') as f:
		user = json.load(f)
	guild = user[str(ctx.guild.id)]
	level = user[str(ctx.guild.id)][str(member.id)]['level']
	ranks = []
	rank = 1
	lvl = user[str(ctx.guild.id)][str(member.id)]['level']  + 1
	exps=[1]
	if lvl == 696969696969696969696970:
		return
	while lvl > len(exps):
		exps.append(int(exps[-1] + exps[-1]/10))
		if lvl == len(exps):
			break
	lvl_end = exps[-1]
	for i in guild:
		if i.isdigit():
			if i == "774136203548557333":
				pass
			else:
				l = guild[str(i)]['level']
				ranks.append(l)
	ranks = sorted(ranks, reverse=True)
	for q in ranks:
		if q == level:
			break
		rank += 1

	if str(member.id) in guild:
		lvl = user[str(ctx.guild.id)][str(member.id)]['level']
		exp = user[str(ctx.guild.id)][str(member.id)]['exp']
	else:
		lvl = 0
		exp = 0
		lvl_end = 0
	if lvl == 0:
		rank = 0
		
	avatar = member.avatar_url_as(size=128)
	Level = lvl
	exp = exp
	exp_limit = lvl_end
	rank = rank
	name = member

	await ctx.send(f"You have {lvl} <:coin:865205194454204436> ")



@client.command(aliases = ["lb"])
async def leaderboard(ctx, x=5):
  with open('points.json', 'r') as f:
    
    users = json.load(f)
    guild = ctx.guild
    
  leaderboard = {}
  total=[]
  
  for user in list(users[str(ctx.guild.id)]):
    name = int(user)
    total_amt = users[str(ctx.guild.id)][str(user)]['level']
    leaderboard[total_amt] = name
    total.append(total_amt)
    

  total = sorted(total,reverse=True)
  

  em = discord.Embed(
    title = f'Top {x} members with most <:coin:865205194454204436> in {ctx.guild.name}',
    description = f'Top {x} in {ctx.guild.name} '
  )
  
  index = 1
  for amt in total:
    id_ = leaderboard[amt]
    member = guild.get_member(id_)
    
    
    em.add_field(name = f'{index}: {member}', value = f'{amt}', inline=False)
    
    
    if index == x:
      break
    else:
      index += 1
      
  await ctx.send(embed = em)


client.run(os.getenv('token'))
