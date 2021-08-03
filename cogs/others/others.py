from cogs.core import core
from discord.ext import commands
from discord_slash.utils.manage_components import create_button, create_actionrow, ComponentContext, wait_for_component
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext
import ast
import base64
from bs4 import BeautifulSoup
import discord
import os, requests, json, datetime
from dotenv import load_dotenv
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")

async def get_data(user_id: int):
	response = requests.get(f"https://osu.ppy.sh/users/{user_id}")
	soup = BeautifulSoup(response.text, "html.parser")
	data = json.loads(str(soup.find("script", id="json-user"))[60:][:-18])
	return data

class others(core):

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		print(payload.emoji.url)

	@commands.command()
	async def here2(self, ctx):
		member = await ctx.guild.fetch_member(455259347107446794)
		embed=discord.Embed(title="=========**GUESS-NUMBER**=========", description="<#869899274605981697>", color=discord.Colour.green()).add_field(name="規則",value="```md\n- 一開始隨機生成數字(1~100)\n- 猜得太高或太低小卯會提示你\n- 最先猜中的人加一分，並開啟新的一局\n```",inline=False).add_field(name="指令",value="`~查看guess_number分數` 可查看自己的分數\n`~查看guess_number排行榜` 可查看所有人的排名和分數",inline=True).set_author(name=member, icon_url=member.avatar_url)
		await ctx.send(embed=embed)

	@commands.command()
	@commands.has_permissions(administrator=True)
	async def clear(self, ctx):
		deleted = await ctx.channel.purge(limit=None)
		await ctx.send(embed=discord.Embed(title=f"🗑️成功刪除{len(deleted)}則訊息", description=f"<@{ctx.author.id}>", color=discord.Colour.green()))
	
	@commands.command()
	async def run(self, ctx, *, cmd):

		def insert_returns(body):
			if isinstance(body[-1], ast.Expr):
				body[-1] = ast.Return(body[-1].value)
				ast.fix_missing_locations(body[-1])

			if isinstance(body[-1], ast.If):
				insert_returns(body[-1].body)
				insert_returns(body[-1].orelse)

			if isinstance(body[-1], ast.With):
				insert_returns(body[-1].body)

		fn_name = "_eval_expr"

		cmd = cmd.strip("` ")

		cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

		body = f"async def {fn_name}():\n{cmd}"

		parsed = ast.parse(body)
		body = parsed.body[0].body

		insert_returns(body)

		env = {
			'bot': ctx.bot,
			'discord': discord,
			'commands': commands,
			'ctx': ctx,
			'__import__': __import__
		}
		exec(compile(parsed, filename="<ast>", mode="exec"), env)

		result = (await eval(f"{fn_name}()", env))
		await ctx.send(result)

def setup(client):
	client.add_cog(others(client))
