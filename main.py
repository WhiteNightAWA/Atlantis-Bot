import asyncio
import os
import discord
from discord.ext import commands
from discord_slash import SlashCommand
from discord.ext.commands import errors

client = commands.Bot(command_prefix="~", activity=discord.Game(name="木貓"), description="由某白夜和綠鷹精心為木貓打造的機器人~awa", guild_subscriptions=True)
slash = SlashCommand(client, sync_commands=True, sync_on_cog_reload=True)

from dotenv import load_dotenv
load_dotenv()

@client.command(name="reload")
async def reload(ctx):
	await ctx.message.delete()
	for file in os.listdir("./cogs"):
		if not file.endswith(".py"):
			for fileName in os.listdir(f"./cogs/{file}"):
				if fileName.endswith(".py"):
					if fileName not in ["osu.py"]:
						try:
							client.unload_extension(f"cogs.{file}.{fileName[:-3]}")
						except:
							pass
						client.load_extension(f"cogs.{file}.{fileName[:-3]}")
	await ctx.send("成功!! (ﾉ◕ヮ◕)ﾉ*.✧")

for file in os.listdir("./cogs"):
	if not file.endswith(".py"):
		for fileName in os.listdir(f"./cogs/{file}"):
			if fileName.endswith(".py"):
				client.load_extension(f"cogs.{file}.{fileName[:-3]}")

if __name__ == "__main__":
	client.run(os.getenv("token"))
