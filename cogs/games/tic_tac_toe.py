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

async def get_text(list_str):
	msg, count = "", 1
	for row in list_str:
		c = 1
		for item in row:
			if c < 3:
				if item == 0:
					msg = msg + ":black_medium_square: | "
				elif item == 1:
					msg = msg + ":x: | "
				elif item == 2:
					msg = msg + ":o: | "
			else:
				if count < 3:
					if item == 0:
						msg = msg + ":black_medium_square:\n--- + --- + ---\n"
					elif item == 1:
						msg = msg + ":x:\n--- + --- + ---\n"
					elif item == 2:
						msg = msg + ":o:\n--- + --- + ---\n"
				else:
					if item == 0:
						msg = msg + ":black_medium_square:"
					elif item == 1:
						msg = msg + ":x:"
					elif item == 2:
						msg = msg + ":o:"
			c += 1
		count += 1
	return msg


class tic_tac_toe(core):

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
					data["tic_tac_toe"][str(msg.id)] = {"player": {"p1": ctx.author.id, "p2": p2.id}, "cb": cb}
					requests.put(html1, params={"id": html2}, json=data)
					for emoji in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]:
						await msg.add_reaction(emoji)
					await msg.edit(embed=discord.Embed(title=f"`{ctx.author}`的回合", color=random.randint(0, 0xffffff), description=f"P1 (:x:): <@!{ctx.author.id}>\nP2 (:o:): <@!{p2.id}>").add_field(name="棋盤", value=await get_text(cb)))
				elif str(payload.emoji) == "❌":
					await msg.edit(content="", embed=discord.Embed(title=f"`{p2}`拒絕了你的邀請", color=discord.Colour.red()))
			except asyncio.TimeoutError:
				await msg.clear_reactions()
				await msg.edit(content="", embed=discord.Embed(title="邀請超時", color=discord.Colour.red()))


def setup(client):
	client.add_cog(tic_tac_toe(client))
