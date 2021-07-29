import discord
import requests, random
from discord.ext import commands
from discord_slash.utils.manage_components import create_button, create_actionrow, ComponentContext, wait_for_component
from discord_slash.model import ButtonStyle
from cogs.core import core
import os
from dotenv import load_dotenv
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")


class sign_in(core):


	@commands.command()
	async def here(self, ctx):
		pass


	@commands.Cog.listener()
	async def on_component(self, ctx: ComponentContext):
		if ctx.custom_id == "0311c913-ec34-4233-a84b-f88db5475f1a":
			await ctx.edit_origin(embed=discord.Embed(description="<@&858535636385267712>", color=random.randint(0,0xffffff)))
			role = ctx.guild.get_role(858535636385267712)
			await ctx.author.add_roles(role)

	@commands.command()
	async def 申請加入(self, ctx):
		def check(m):
			return m.channel == ctx.channel and m.author == ctx.author

		awa = {"請問你的Minecraft id是:": "userName", "請問你目前真實學程是:": "user學程", "請問你的科技進度是:": "user科技進",
			"請問你想加入的原因是:": "user原因", "請問你專長的是:": "user專長", "請問你興趣的是:": "user興趣", "請問你有無其他社區:": "user社區"}
		for x in awa:
			if x == "請問你目前真實學程是:":
				embed = discord.Embed(title=x, description=f"(真實學程就是 幼稚園/國小/國中/高中/大學)\n<@{ctx.author.id}>",
									color=discord.Colour.green())
			else:
				embed = discord.Embed(title=x, description=f"<@{ctx.author.id}>", color=discord.Colour.green())
			msg2 = await ctx.send(embed=embed)
			msg = await self.client.wait_for('message', check=check)
			awa[x] = msg.content
			await msg.delete()
			await msg2.delete()
		embed = discord.Embed(title=f"{ctx.author}申請加入!", description=f"<@{ctx.author.id}>", color=0x03e3fc)
		embed.add_field(name="遊戲ID", value=awa["請問你的Minecraft id是:"], inline=True)
		embed.add_field(name="真實學程", value=awa["請問你目前真實學程是:"], inline=True)
		embed.add_field(name="科技進度", value=awa["請問你的科技進度是:"], inline=True)
		embed.add_field(name="加入的原因", value=awa["請問你想加入的原因是:"], inline=True)
		embed.add_field(name="專長", value=awa["請問你專長的是:"], inline=True)
		embed.add_field(name="興趣", value=awa["請問你興趣的是:"], inline=True)
		embed.add_field(name="其他社區", value=awa["請問你有無其他社區:"], inline=True)
		embed.set_image(url=ctx.author.avatar_url)
		msg = await ctx.guild.get_channel(865819228870279169).send(embed=embed)
		data = requests.get(html).json()
		data["add"][str(msg.id)] = ctx.author.id
		requests.put(html1, params={"id": html2},json=data)
		await msg.add_reaction("✅")
		await msg.add_reaction("❌")
		await ctx.send(
			embed=discord.Embed(title="✅ 申請成功", description=f"<@{ctx.author.id}>", color=discord.Colour.green()))

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if not payload.member.bot:
			data = requests.get(html).json()
			if str(payload.message_id) in data["add"]:
				guild = self.client.get_guild(payload.guild_id)
				member_id = int(data["add"][str(payload.message_id)])
				member = await guild.fetch_member(member_id)
				role = guild.get_role(856388764468379658)
				message = await self.client.get_channel(payload.channel_id).fetch_message(int(payload.message_id))
				if payload.emoji.name == "✅":
					await member.add_roles(role)
					embed = discord.Embed(title=f"已通過{member}的申請",
										description=f"申請人: <@{member.id}>\n處理人: <@{payload.member.id}>",
										color=discord.Colour.green())
					newEmbed = message.embeds[0]
					newEmbed.title = f"已通過{member}的申請"
					newEmbed.description = f"申請人: <@{member.id}>\n處理人: <@{payload.member.id}>"
					newEmbed.set_image(url="")
					newEmbed.set_thumbnail(url=member.avatar_url)
					await message.clear_reactions()
					await message.edit(embed=newEmbed)
					try:
						await member.send(embed=embed)
					except:
						pass
				if payload.emoji.name == "❌":
					embed = discord.Embed(title=f"已拒絕{member}的申請",
										description=f"申請人: <@{member.id}>\n處理人: <@{payload.member.id}>",
										color=discord.Colour.red())
					await message.clear_reactions()
					try:
						await member.send(embed=embed)
					except:
						pass
					await message.edit(embed=embed)


def setup(client):
	client.add_cog(sign_in(client))
