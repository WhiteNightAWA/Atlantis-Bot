from discord import member
from discord_slash.utils.manage_components import create_button, create_actionrow, ComponentContext, wait_for_component
from discord_slash.model import ButtonStyle
from cogs.core import core
from discord.ext import commands
import discord, os, ast, random, asyncio, requests
from dotenv import load_dotenv
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")

def to_emoji(num):
	count = 1
	for x in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]:
		if count == num:
			return x
		count += 1

async def get_text(list_str, kind):
	msg, count, num = "", 1, 1
	for row in list_str:
		c = 1
		for item in row:
			if c < 3:
				if item == 0:
					if kind == 1:
						msg = msg + f"{to_emoji(num)} | "
					else:
						msg = msg + f":black_large_square: | "
				elif item == 1:
					msg = msg + ":x: | "
				elif item == 2:
					msg = msg + ":o: | "
			else:
				if count < 3:
					if item == 0:
						if kind == 1:
							msg = msg + f"{to_emoji(num)}\n----+----+----\n"
						else:
							msg = msg + f":black_large_square:\n----+----+----\n"
					elif item == 1:
						msg = msg + ":x:\n----+----+----\n"
					elif item == 2:
						msg = msg + ":o:\n----+----+----\n"
				else:
					if item == 0:
						if kind == 1:
							msg = msg + f"{to_emoji(num)}"
						else:
							msg = msg + f":black_large_square:"
					elif item == 1:
						msg = msg + ":x:"
					elif item == 2:
						msg = msg + ":o:"
			c += 1
			num += 1
		count += 1
	return msg

async def check_winer(line:list, can_do):
	winer = "no"
	if can_do != []:
		for x in line:
			if x[0] == x[1] == x[2]:
				if x[0] != 0:
					winer = x[0]
		for x in range(3):
			if line[0][x] == line[1][x] == line[2][x]:
				if line[x][0] != 0:
					winer = line[x][0]
		if line[0][0] == line[1][1] == line[2][2]:
			if line[0][0] != 0:
				winer = line[0][0]
		if line[0][2] == line[1][1] == line[2][0]:
			if line[0][2] != 0:
				winer = line[0][0]
	else:
		winer = "draw"
	return winer

class tic_tac_toe(core):

	@commands.command()
	async def 查看tic分數(self, ctx):
		data = requests.get(html).json()
		id = str(ctx.author.id)
		if id in data["tic_tac_toe"]["points"]:
			await ctx.send(f"<@{ctx.author.id}> 的分數為 : `{data['tic_tac_toe']['points'][id]}`")
		else:
			await ctx.send(f"<@{ctx.author.id}> 的分數為 : `0`")
		await ctx.message.delete()

	@commands.command(pass_context=True)
	async def 查看tic排行榜(self, ctx):
		data = requests.get(html).json()
		dictset = sorted(data["tic_tac_toe"]["points"].items(), key = lambda d: d[1], reverse=True)
		text, count = "", 0
		for x in dictset:
			text = text + f"第`{count+1}`名：<@{dictset[count][0]}>  分數：`{dictset[count][1]}`\n"
			count += 1
		await ctx.send(embed=discord.Embed(title="**tic_tac_toe**排行榜", description=text, color=random.randint(0, 0xffffff)))
		await ctx.message.delete()

	@commands.command()
	async def start_tic(self, ctx, p2:discord.Member):
		await ctx.message.delete()
		if p2.id == 841678712767512597:
			pass
		else:
			msg = await ctx.send(content=f"<@!{p2.id}>",embed=discord.Embed(title=f"`{ctx.author}`邀請你玩井字棋", color=random.randint(0, 0xffffff)))
			await msg.add_reaction("✅")
			await msg.add_reaction("❌")
			try:
				def check(payload):
					return payload.member.id == p2.id and str(payload.emoji) in ["✅", "❌"] and payload.message_id == msg.id
				payload = await self.client.wait_for("raw_reaction_add", timeout=30, check=check)
				await msg.clear_reactions()
				if str(payload.emoji) == "✅":
					await msg.edit(content="", embed=discord.Embed(title="遊戲即將開始", color=discord.Colour.green()))
					cb = [[0,0,0],[0,0,0],[0,0,0]]
					data = requests.get(html).json()
					data["tic_tac_toe"][str(msg.id)] = {"player": {str(ctx.author.id): 1,str(p2.id): 2}, "round": ctx.author.id, "cb": cb, "can_do":["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]}
					for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]:
						await msg.add_reaction(emoji)
					await msg.edit(embed=discord.Embed(title=f"`{ctx.author}`的回合", color=random.randint(0, 0xffffff), description=f"P1 (:x:): <@!{ctx.author.id}>\nP2 (:o:): <@!{p2.id}>").add_field(name="棋盤", value=await get_text(cb,1)))
					requests.put(html1, params={"id": html2}, json=data)
				elif str(payload.emoji) == "❌":
					await msg.edit(content="", embed=discord.Embed(title=f"`{p2}`拒絕了你的邀請", color=discord.Colour.red()))
			except asyncio.TimeoutError:
				await msg.clear_reactions()
				await msg.edit(content="", embed=discord.Embed(title="邀請超時", color=discord.Colour.red()))

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if not payload.member.bot:
			data = requests.get(html).json()
			msg = await self.client.get_channel(payload.channel_id).fetch_message(payload.message_id)
			if str(payload.message_id) in data["tic_tac_toe"]:
				if payload.member.id == data["tic_tac_toe"][str(payload.message_id)]["round"] and str(payload.emoji) in data["tic_tac_toe"][str(payload.message_id)]["can_do"]:
					player = []
					for p in data["tic_tac_toe"][str(payload.message_id)]["player"]:
						player.append(p)
					user = data["tic_tac_toe"][str(payload.message_id)]["round"]
					user_num = data["tic_tac_toe"][str(payload.message_id)]["player"][str(user)]
					x,y = 0,0
					for a in [["1️⃣", "2️⃣", "3️⃣"], ["4️⃣", "5️⃣", "6️⃣"], ["7️⃣", "8️⃣", "9️⃣"]]:
						x = 0
						for b in a:
							if str(payload.emoji) == b:
								data["tic_tac_toe"][str(payload.message_id)]["cb"][y][x] = user_num
							x += 1
						y += 1
					data["tic_tac_toe"][str(payload.message_id)]["can_do"].remove(str(payload.emoji))
					cb = data["tic_tac_toe"][str(payload.message_id)]["cb"]
					can_do = data["tic_tac_toe"][str(payload.message_id)]["can_do"]
					winer = await check_winer(cb, can_do)
					if winer == "no":
						await msg.remove_reaction(str(payload.emoji), payload.member)
						await msg.remove_reaction(str(payload.emoji), await self.client.get_guild(payload.guild_id).fetch_member(841678712767512597))
						if str(player[0]) == str(payload.member.id):
							next = await self.client.get_guild(payload.guild_id).fetch_member(int(player[1]))
						else:
							next = await self.client.get_guild(payload.guild_id).fetch_member(int(player[0]))
						data["tic_tac_toe"][str(payload.message_id)]["round"] = next.id
						await msg.edit(embed=discord.Embed(title=f"`{next}`的回合", color=random.randint(0, 0xffffff), description=f"P1 (:x:): <@!{player[0]}>\nP2 (:o:): <@!{player[1]}>").add_field(name="棋盤", value=await get_text(cb,1)))
						requests.put(html1, params={"id": html2}, json=data)
					elif winer == "draw":
						await msg.edit(embed=discord.Embed(title=f"遊戲結束：平局！", color=random.randint(0, 0xffffff), description=f"P1 (:x:): <@!{player[0]}>\nP2 (:o:): <@!{player[1]}>").add_field(name="棋盤", value=await get_text(cb,2)))
						await msg.clear_reactions()
						data["tic_tac_toe"].pop(str(payload.message_id), None)
						requests.put(html1, params={"id": html2}, json=data)
					else:
						await msg.edit(embed=discord.Embed(title=f"遊戲結束：`{payload.member}`勝利！", color=random.randint(0, 0xffffff), description=f"P1 (:x:): <@!{player[0]}>\nP2 (:o:): <@!{player[1]}>").add_field(name="棋盤", value=await get_text(cb,2)))
						await msg.clear_reactions()
						data["tic_tac_toe"].pop(str(payload.message_id), None)
						if str(payload.member.id) in data["tic_tac_toe"]["points"]:
							data["tic_tac_toe"]["points"][str(payload.member.id)] += 1
						else:
							data["tic_tac_toe"]["points"][str(payload.member.id)] = 1
						requests.put(html1, params={"id": html2}, json=data)
				else:
					await msg.remove_reaction(str(payload.emoji), payload.member)


def setup(client):
	client.add_cog(tic_tac_toe(client))
