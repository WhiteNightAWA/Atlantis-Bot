from cogs.core import core
from discord.ext import commands
from discord_slash.utils.manage_components import create_button, create_actionrow, ComponentContext, wait_for_component
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext
import discord, requests, json, ast, os, datetime, asyncio, random, matplotlib, base64, ast
from progressbar import *
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import numpy as np
html = os.environ["html"]
html1 = os.environ["html1"]
html2 = os.environ["html2"]

async def get_data(user_id: int):
	response = requests.get(f"https://osu.ppy.sh/users/{user_id}")
	soup = BeautifulSoup(response.text, "html.parser")
	data = json.loads(str(soup.find("script", id="json-user"))[60:][:-18])
	return data

async def exp(osu):
	lv, exp = osu['statistics']['level']['current'], osu['statistics']['level']['progress']
	text = f"```Lv.{lv}| "
	exp2 = round(exp/5)
	for _ in range(20):
		if exp2 > 0:
			text = text + "█"
			exp2 -= 1
		else:
			text = text + " "
			exp2 -= 1
	text = text + f" |{exp}%```"
	return text

async def num(num_int):
	text = ""
	awa = list(str(num_int))
	for x in awa:
		if x == "1":
			text = text + ":one:"
		elif x == "2":
			text = text + ":two:"
		elif x == "3":
			text = text + ":three:"
		elif x == "4":
			text = text + ":four:"
		elif x == "5":
			text = text + ":five:"
		elif x == "6":
			text = text + ":six:"
		elif x == "7":
			text = text + ":seven:"
		elif x == "8":
			text = text + ":eight:"
		elif x == "9":
			text = text + ":nine:"
		elif x == "0":
			text = text + ":zero:"
	return text

async def get_ranks(user_id):
	v = await get_data(user_id)
	v, x = v['rank_history']['data'], []
	for r in v:
		if r == 0: 
			pass
		else:
			x.append(int(r))
	y = []
	count = 1
	for z in x:
		if z != x[-1]:
			t = datetime.date.today() - datetime.timedelta(days=int(len(x)-count))
			d = t.strftime("%d/%m")
			y.append(d)
			count += 1
		else:
			y.append("Now")
	fig = plt.figure()
	ax = plt.gca()
	plt.plot(y,x)
	plt.title("osu! Ranks")
	plt.xlabel("Time")
	plt.ylabel("Ranks")
	plt.gca().invert_yaxis()
	fig.set_size_inches(10,5)
	fig.set_facecolor("white")
	plt.savefig(f'foo{user_id}.png')
	with open(f'foo{user_id}.png', "rb") as file:
		url = "https://api.imgbb.com/1/upload"
		key = '33bf975438e54bf5bb36d94ac087c206'
		payload = {
			"key": key,
			"image": base64.b64encode(file.read()),
		}
		res = requests.post(url, payload).json()
	os.remove(f'foo{user_id}.png')
	plt.close('all')
	plt.clf()
	s = res["data"]["display_url"]
	return s


class osu(core):
	
	@commands.command(name="me")
	async def me(self, ctx):
		data = requests.get(html).json()
		if str(ctx.author.id) in data["osu"]:
			user_id = data["osu"][str(ctx.author.id)]
			osu = await get_data(user_id)
			embed=discord.Embed(title=f":flag_{osu['country_code'].lower()}:`{osu['username']}`", url=f"https://osu.ppy.sh/users/{user_id}", color=random.randint(0, 0xffffff))
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			embed.set_thumbnail(url=osu["avatar_url"])
			embed.add_field(name="等级", value=await exp(osu), inline=False)
			embed.add_field(name="排名", value=f"全球`#{osu['statistics']['global_rank']}`\n國家`#{osu['statistics']['country_rank']}`", inline=True)
			embed.add_field(name="Ranks", value=f"<:rankA:868795017458753606>`{osu['statistics']['grade_counts']['a']}`|<:rankS:868795016804438098>`{osu['statistics']['grade_counts']['s']}`|<:rankSH:868795017098035230>`{osu['statistics']['grade_counts']['sh']}`\n<:rankSS:868795017190342676>`{osu['statistics']['grade_counts']['ss']}`|<:rankSSH:868795016670240800>`{osu['statistics']['grade_counts']['ssh']}`", inline=True)
			embed.add_field(name="總遊玩時間", value=f"`{str(datetime.timedelta(seconds=osu['statistics']['play_time']))}`", inline=True)
			embed.add_field(name="總分", value=f"`{int(osu['statistics']['total_score'])}`", inline=True)
			embed.add_field(name="進榜圖譜總分", value=f"`{int(osu['statistics']['ranked_score'])}`", inline=True)
			embed.add_field(name="遊玩次數", value=f"`{int(osu['statistics']['play_count'])}`", inline=True)
			embed.add_field(name="PP",value=f"`{int(str(round(osu['statistics']['pp'])))}`", inline=True)
			embed.add_field(name="準確率", value=f"`{int(round(osu['statistics']['hit_accuracy']))}`", inline=True)
			embed.add_field(name="成就", value=f"`{int(str(len(osu['user_achievements'])))}`", inline=True)
			embed.add_field(name="總命中次數", value=f"`{int(osu['statistics']['total_hits'])}`", inline=True)
			embed.add_field(name="最大連擊", value=f"`{int(osu['statistics']['maximum_combo'])}`", inline=True)
			x = ""
			if osu['playstyle'] != None:
				for y in osu['playstyle']:
					if y == "mouse":
						x = x + ":mouse_three_button: "
					elif y == "keyboard":
						x = x + ":keyboard: "
					elif y == "tablet":
						x = x + ":white_square_button: "
					elif y == "touch":
						x = x + ":mobile_phone: "
				embed.add_field(name="慣用", value=x, inline=True)
			else:
				embed.add_field(name="慣用", value="未設定", inline=True)
			if osu['is_online']:
				embed.add_field(name="狀態", value=":green_circle: Online", inline=True)
			else:
				embed.add_field(name="狀態", value=":red_circle: Offline", inline=True)
			embed.add_field(name="最後上線", value=f"`{datetime.datetime.fromisoformat(str(osu['last_visit'])[:-6])+datetime.timedelta(hours=8)}`", inline=True)
			embed.add_field(name="註冊時間", value=f"`{datetime.datetime.fromisoformat(str(osu['join_date'])[:-6])+datetime.timedelta(hours=8)}`", inline=True)
			embed.add_field(name="論壇", value=f"發表了`{int(osu['post_count'])}`篇貼文\n發表了`{int(osu['comments_count'])}`則留言", inline=True)
			embed.add_field(name="粉絲", value=f"`{int(osu['follower_count'])}`", inline=True)
			embed.add_field(name="作圖追蹤者", value=f"`{int(osu['graveyard_beatmapset_count'])}`", inline=True)
			embed.add_field(name="Discord", value=f"`{osu['discord']}`", inline=True)
			embed.add_field(name="Twitter", value=f"`{osu['twitter']}`", inline=True)
			embed.add_field(name="個人網站", value=f"`{osu['website']}`", inline=True)
			embed.set_image(url=await get_ranks(user_id))
			await ctx.send(embed=embed)
		else:
			pass
	
	@commands.command(name="register")
	async def register(self, ctx, user_id:int):
		osu = await get_data(user_id)
		if str(ctx.author) == str(osu['discord']):
			data = requests.get(html).json()
			data["osu"][str(ctx.author.id)] = user_id
			requests.put(html1, params={"id": html2},json=data)
			await ctx.send(embed=discord.Embed(title="Done", color=discord.Colour.green()))
		else:
			embed=discord.Embed(title=f"`{osu['username']}`不是你的osu帳號或你在那個帳號並沒有填上你的discord帳號", color=discord.Colour.red()).set_image(url="https://i.ibb.co/GtFF722/Screen-Shot-2021-07-25-at-7-30-30-PM.png")
			embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
			await ctx.send(embed=embed)

	@commands.command(name="add_osu")
	async def add_osu(self, ctx, user_id:int):
		data = requests.get(html).json()
		data["osu"]["user_list"].append(user_id)
		requests.put(html1, params={"id": html2},json=data)
		
	@commands.command()
	async def register_id(self, ctx, user_id, discord_id):
			data = requests.get(html).json()
			data["osu"][str(discord_id)] = user_id
			requests.put(html1, params={"id": html2},json=data)
			await ctx.send(embed=discord.Embed(title="Done", color=discord.Colour.green()))


	@commands.command()
	async def rank(self, ctx):
		pass


	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		print(payload.emoji)

def setup(client):
	client.add_cog(osu(client))