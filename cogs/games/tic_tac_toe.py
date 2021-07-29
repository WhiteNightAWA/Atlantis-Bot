from discord_slash.utils.manage_components import create_button, create_actionrow, ComponentContext, wait_for_component
from discord_slash.model import ButtonStyle
from cogs.core import core
from discord.ext import commands
import discord, os, ast, random, asyncio
html = os.environ["html"]
html1 = os.environ["html1"]
html2 = os.environ["html2"]

async def get_text(lister):
	pass

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
				def check(reaction, user):
					return user.id == p2.id and str(reaction.emoji) in ["✅", "❌"]
				reaction, user = await self.client.wait_for("reaction_add", timeout=30, check=check)
				if str(reaction.emoji) == "✅":
					await ctx.send("yes")
				elif str(reaction.emoji) == "❌":
					await ctx.send("no")
			except asyncio.TimeoutError:
				await ctx.send("timeout")
			
		

def setup(client):
	client.add_cog(tic_tac_toe(client))
