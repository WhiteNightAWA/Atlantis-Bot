from cogs.core import core
from discord.ext import commands
import discord, random, requests

import os

from dotenv import load_dotenv
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")




class book(core):
	
	@commands.command()
	async def 訂購機器(self, ctx, 機器種類:str, 數量:int, 理想價錢:int):
		channel = ctx.guild.get_channel(866623568967499796)

		msg2 = await ctx.send(embed=discord.Embed(title="請問你是否有會員?", description=f"請回答`是`或`否`\n<@{ctx.author.id}>", color=discord.Colour.green()))

		def check(msg):
			return msg.author.id == ctx.author.id and msg.content in ["是", "否"]

		msg = await self.client.wait_for("message", check=check, timeout=30)
		await msg.delete()
		await msg2.delete()
		embed=discord.Embed(title=f"`{ctx.author}`訂購機器!", description=f"<@{ctx.author.id}>", color=random.randint(0, 0xffffff))
		embed.set_thumbnail(url=ctx.author.avatar_url)
		embed.add_field(name="機器種類:", value=機器種類, inline=True).add_field(name="數量:", value=數量, inline=True).add_field(name="理想價錢:", value=理想價錢, inline=True)
		if msg.content == "是":
			是否會員 = "✅"
		else:
			是否會員 = "❌"
		embed.add_field(name="是否會員", value=是否會員, inline=True)
		是否村民 = "❌"
		for role in ctx.author.roles:
			if role.id == 856388764468379658:
				是否村民 = "✅"
		embed.add_field(name="是否村民", value=是否村民, inline=True)
		msg3 = await channel.send(embed=embed)
		await msg3.add_reaction("✅")
		await ctx.message.delete()
		data = requests.get(html).json()
		data["book"][str(msg3.id)] = ctx.author.id
		requests.put(html1, params={"id": html2},json=data)
		await ctx.send(embed=discord.Embed(title="✅ 訂購申請發送成功, 請靜待管理員審核", description=f"<@!{ctx.author.id}>", color=discord.Colour.green()))
	

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		data = requests.get(html).json()
		if str(payload.message_id) in data["book"]:
			guild = self.client.get_guild(payload.guild_id)
			member = await guild.fetch_member(data["book"][str(payload.message_id)])
			channel = guild.get_channel(payload.channel_id)
			message = await channel.fetch_message(payload.message_id)
			embed = message.embeds[0].add_field(name="已完成-處理人:", value=f"<@{payload.user_id}>")
			await message.edit(embed=embed)
			await member.send(embed=discord.Embed(title="您的貨品已準備好了\n請到小卯捷運麥當勞旁邊取貨\n歡迎下次訂購",
			description=f"處理人: <@{payload.user_id}>" ,color=discord.Colour.green()))
			data = requests.get(html).json()
			data["book"].pop(str(payload.message_id), None)
			requests.put(html1, params={"id": html2},json=data)

def setup(client):
	client.add_cog(book(client))