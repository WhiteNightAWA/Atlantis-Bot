from cogs.core import core
from discord.ext import commands
import asyncio, requests, os

from dotenv import load_dotenv
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")

class ready(core):

	@commands.Cog.listener()
	async def on_ready(self):
		print(">>>Bot Ready<<<")
	
	@commands.Cog.listener()
	async def on_message(self, message):
		if message.channel.id == 866672030454382662:
			if not str(message.content).startswith("~"):
				if not str(message.content).startswith("!"):
					if not str(message.content).startswith("|"):
						if not message.author.bot:
							await asyncio.sleep(1)
							await message.delete()

def setup(client):
	client.add_cog(ready(client))
