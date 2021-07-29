from cogs.core import core
from discord.ext import commands
import discord
import os, requests, random
from dotenv import load_dotenv
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")


class guess_number(core):
	
	@commands.Cog.listener()
	async def on_raw_message_edit(self, payload):
		if payload.channel_id == 869899274605981697:
			message = await self.client.get_channel(867007112332705792).fetch_message(payload.message_id)
			await message.delete()

	@commands.command()
	async def 查看guess_number分數(self, ctx):
		data = requests.get(html).json()
		id = str(ctx.author.id)
		if id in data["guess_number"]["points"]:
			await ctx.send(f"<@{ctx.author.id}> 的分數為 : {data['guess_number']['points'][id]}")
		else:
			await ctx.send(f"<@{ctx.author.id}> 的分數為 : 0")
		await ctx.message.delete()

	@commands.command(pass_context=True)
	async def 查看guess_number排行榜(self, ctx):
		data = requests.get(html).json()
		dictset = sorted(data["guess_number"]["points"].items(), key = lambda d: d[1], reverse=True)
		text, count = "", 0
		for x in range(5):
			text = text + f"第`{count+1}`名：<@!{dictset[count][0]}>  分數：`{dictset[count][1]}`\n"
			count += 1
		await ctx.send(embed=discord.Embed(title="**GUESS-NUMBER**排行榜", description=text, color=random.randint(0, 0xffffff)))
		await ctx.message.delete()

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.channel.id == 869899274605981697 and not message.author.bot:
			data = requests.get(html).json()
			num = data["guess_number"]["number"]
			try:
				int(message.content)
				msgs = await message.channel.history(limit=2).flatten()
				if int(message.content) == num:
					await message.channel.purge(limit=None)
					await message.channel.send(embed=discord.Embed(description=f"<@!{message.author.id}>猜對了\n數字=`{num}`", color=random.randint(0, 0xffffff)))
					if str(message.author.id) in data["guess_number"]["points"]:
						data["guess_number"]["points"][str(message.author.id)] += 1
					else:
						data["guess_number"]["points"][str(message.author.id)] = 1
					data["guess_number"]["number"] = random.randint(0, 100)
					requests.put(html1, params={"id": html2}, json=data)
				elif int(message.content) > num:
					await message.reply(embed=discord.Embed(title="數字太大", description=f"數字<`{message.content}`", color=random.randint(0, 0xffffff)))
				elif int(message.content) < num:
					await message.reply(embed=discord.Embed(title="數字太小", description=f"數字>`{message.content}`", color=random.randint(0, 0xffffff)))
			except ValueError:
				await message.delete()

def setup(client):
	client.add_cog(guess_number(client))
