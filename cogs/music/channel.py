from cogs.core import core
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import discord, requests, os, random, youtube_dl, datetime, asyncio
from discord.errors import *
from discord.ext.commands.errors import *
import os
from dotenv import load_dotenv
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")


class channel(core):


	@cog_ext.cog_slash(name="join")
	async def _join(self, ctx):
		vc = ctx.author.voice.channel
		try:
			await vc.connect()
			await ctx.send(embed=discord.Embed(title="成功連接到語音頻道。",
											description=f"連接到語音通道: <#{ctx.author.voice.channel.id}>",
											colour=discord.Colour.green()))
		except ClientException:
			for x in self.client.voice_clients:
				if x.guild == ctx.guild:
					vc = x
			await ctx.send(embed=discord.Embed(title="機器人已經連接到語音通道。",
											description=f"連接到語音通道: <#{vc.channel.id}>",
											colour=discord.Colour.red()))
		except AttributeError:
			await ctx.send(embed=discord.Embed(title="請你先加入一個語音頻道。", colour=discord.Colour.red()))

	@cog_ext.cog_subcommand(base="music",name="leave")
	async def _leave(self, ctx:SlashContext):
		vc = ""
		try:
			for x in self.client.voice_clients:
				if x.guild == ctx.guild:
					vc = x
			await vc.disconnect()
			await ctx.send(embed=discord.Embed(title="成功離開到語音頻道。",
											description=f"離開語音通道: <#{vc.channel.id}>",
											colour=discord.Colour.green()))
		except AttributeError:
			await ctx.send(embed=discord.Embed(title="機器人末加入到語音頻道。",
											description=f"使用`~join`讓機器人加入到語音頻道",
											colour=discord.Colour.red()))

	@commands.command(name="join")
	async def join(self, ctx):
		vc = ctx.author.voice.channel
		try:
			await vc.connect()
			await ctx.send(embed=discord.Embed(title="成功連接到語音頻道。",
											description=f"連接到語音通道: <#{ctx.author.voice.channel.id}>",
											colour=discord.Colour.green()))
		except ClientException:
			for x in self.client.voice_clients:
				if x.guild == ctx.guild:
					vc = x
			await ctx.send(embed=discord.Embed(title="機器人已經連接到語音通道。",
											description=f"連接到語音通道: <#{vc.channel.id}>",
											colour=discord.Colour.red()))
		except AttributeError:
			await ctx.send(embed=discord.Embed(title="請你先加入一個語音頻道。", colour=discord.Colour.red()))

	@commands.command(name="leave")
	async def leave(self, ctx):
		vc = ""
		try:
			for x in self.client.voice_clients:
				if x.guild == ctx.guild:
					vc = x
			await vc.disconnect()
			await ctx.send(embed=discord.Embed(title="成功離開到語音頻道。",
											description=f"離開語音通道: <#{vc.channel.id}>",
											colour=discord.Colour.green()))
		except AttributeError:
			await ctx.send(embed=discord.Embed(title="機器人末加入到語音頻道。",
											description=f"使用`~join`讓機器人加入到語音頻道",
											colour=discord.Colour.red()))


def setup(client):
	client.add_cog(channel(client))
