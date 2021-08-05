from cogs.core import core
from discord.ext import commands
import discord
import os
from dotenv import load_dotenv
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")


class count(core):
	
	@commands.Cog.listener()
	async def on_raw_message_edit(self, payload):
		if payload.channel_id == 867007112332705792:
			message = await self.client.get_channel(867007112332705792).fetch_message(payload.message_id)
			await message.delete()

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.channel.id == 867007112332705792:
			try:
				msg = int(message.content)
				msgs = await message.channel.history(limit=2).flatten()
				if msgs[0].author.id == msgs[1].author.id:
					await message.delete()
				else:
					try:
						int(msgs[1].content)
					except:
						await msgs[1].delete()
					if int(msgs[0].content) != int(msgs[1].content)+1:
						await message.delete()
					else:
						if int(msgs[0].content) == 5000:
							await message.author.send(embed=discord.Embed(title="恭喜你獲得:star:`5`, 請找`White_Night_awa` 領取獎勵"))
			except:
				await message.delete()

def setup(client):
	client.add_cog(count(client))
