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


class song_control(core):

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, payload):
		if not payload.member.bot:
			if payload.emoji.name == "⏹️":
				data = requests.get(html).json()
				if payload.message_id == data["music"]:
					data["music"] = 0
					requests.put(html1, params={"id": html2}, json=data)


	@cog_ext.cog_subcommand(base="music",name="stop_repeat")
	async def _stop_repeat(self, ctx:SlashContext):
		data = requests.get(html).json()
		data["music"] = 0
		requests.put(html1, params={"id": html2}, json=data)

	@cog_ext.cog_subcommand(base="music",name="stop")
	async def _stop(self, ctx:SlashContext):
		vc = ""
		try:
			for x in self.client.voice_clients:
				if x.guild == ctx.guild:
					vc = x
			if vc.is_playing:
				vc.stop()
				await vc.disconnect()
		except:
			pass

	@cog_ext.cog_subcommand(base="music",name="pause")
	async def _pause(self, ctx:SlashContext):
		vc = ""
		try:
			for x in self.client.voice_clients:
				if x.guild == ctx.guild:
					vc = x
			if vc.is_playing:
				vc.pause()
		except:
			pass

	@cog_ext.cog_subcommand(base="music",name="resume")
	async def _resume(self, ctx:SlashContext):
		vc = ""
		for x in self.client.voice_clients:
			if x.guild == ctx.guild:
				vc = x
		if vc.is_paused:
			vc.resume()



	@commands.command(name="stop_repeat")
	async def stop_repeat(self, ctx):
		data = requests.get(html).json()
		data["music"] = 0
		requests.put(html1, params={"id": html2}, json=data)
	
	@commands.command(name="stop")
	async def stop(self, ctx):
		vc = ""
		try:
			for x in self.client.voice_clients:
				if x.guild == ctx.guild:
					vc = x
			if vc.is_playing:
				vc.stop()
				await vc.disconnect()
		except:
			pass

	@commands.command(name="pause")
	async def pause(self, ctx):
		vc = ""
		try:
			for x in self.client.voice_clients:
				if x.guild == ctx.guild:
					vc = x
			if vc.is_playing:
				vc.pause()
		except:
			pass

	@commands.command(name="resume")
	async def resume(self, ctx):
		vc = ""
		for x in self.client.voice_clients:
			if x.guild == ctx.guild:
				vc = x
		if vc.is_paused:
			vc.resume()

def setup(client):
	client.add_cog(song_control(client))
