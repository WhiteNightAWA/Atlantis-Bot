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

class song(core):

	@cog_ext.cog_subcommand(base="music",name="play_url")
	async def _play_url(self, ctx:SlashContext, *, url: str):
		vc = ctx.author.voice
		ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s', "--default-search": "ytsearch"})
		with ydl:
			result = ydl.extract_info(url, download=False)
		embed = discord.Embed(title=result["title"], url=result["webpage_url"], description=f"description```{result['description']}```")
		embed.set_author(name=f"Uploader: {result['uploader']}", url=result["uploader_url"])
		embed.set_image(url=result["thumbnail"])
		embed.set_footer(text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url)
		embed.add_field(name="音樂長短", value=str(datetime.timedelta(seconds=result["duration"])), inline=True)
		embed.add_field(name="觀看次數", value=result["view_count"], inline=True)
		embed.add_field(name="平均評分", value=result["average_rating"], inline=True)
		embed.add_field(name="喜歡", value=result["like_count"], inline=True)
		embed.add_field(name="不喜歡", value=result["dislike_count"], inline=True)
		msg = await ctx.send(embed=embed)
		await msg.add_reaction("✅")
		await msg.add_reaction("❌")

		def check(reaction, user):
			return user == ctx.message.author and str(reaction.emoji) in ["✅", "❌"] and msg.id == reaction.message.id 

		try:
			reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check)
		except asyncio.TimeoutError:
			await msg.clear_reactions()
			await msg.edit(embed=discord.Embed(title="點歌已取消", color=discord.Colour.red()).set_footer(
				text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url))
		else:
			if str(reaction) == "✅":
				try:
					vc = await vc.channel.connect()
				except :
					for x in self.client.voice_clients:
						if x.guild == ctx.guild:
							vc = x
					await vc.disconnect()
					vc = await vc.channel.connect()
				with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
					info = ydl.extract_info(url, download=False)
					URL = info['formats'][0]['url']
				ffm = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
						'options': '-vn'}
				vc.play(discord.FFmpegPCMAudio(URL, **ffm))
				await msg.clear_reactions()
				embed = discord.Embed(title=result["title"], url=result["webpage_url"], color=discord.Colour.green())
				embed.set_author(name=f"Uploader: {result['uploader']}", url=result["uploader_url"])
				embed.set_image(url=result["thumbnail"])
				embed.set_footer(text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url)
				embed.add_field(name="音樂長短", value=str(datetime.timedelta(seconds=result["duration"])), inline=True)
				embed.add_field(name="觀看次數", value=result["view_count"], inline=True)
				embed.add_field(name="平均評分", value=result["average_rating"], inline=True)
				embed.add_field(name="喜歡", value=result["like_count"], inline=True)
				embed.add_field(name="不喜歡", value=result["dislike_count"], inline=True)
				await msg.edit(embed=embed)
			else:
				await msg.clear_reactions()
				await msg.edit(embed=discord.Embed(title="點歌已取消", color=discord.Colour.red()).set_footer(
					text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url))

	@cog_ext.cog_subcommand(base="music",name="repeat")
	async def _repeat(self, ctx:SlashContext, url: str):
		vc = ctx.author.voice
		ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
		with ydl:
			result = ydl.extract_info(url, download=False)
		embed = discord.Embed(title=result["title"], url=result["webpage_url"], description=f"description```{result['description']}```")
		embed.set_author(name=f"Uploader: {result['uploader']}", url=result["uploader_url"])
		embed.set_image(url=result["thumbnail"])
		embed.set_footer(text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url)
		embed.add_field(name="音樂長短", value=str(datetime.timedelta(seconds=result["duration"])), inline=True)
		embed.add_field(name="觀看次數", value=result["view_count"], inline=True)
		embed.add_field(name="平均評分", value=result["average_rating"], inline=True)
		embed.add_field(name="喜歡", value=result["like_count"], inline=True)
		embed.add_field(name="不喜歡", value=result["dislike_count"], inline=True)
		msg = await ctx.send(embed=embed)
		await msg.add_reaction("✅")
		await msg.add_reaction("❌")

		def check(reaction, user):
			return user == ctx.message.author and str(reaction.emoji) in ["✅", "❌"] and msg.id == reaction.message.id 

		try:
			reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check)
		except asyncio.TimeoutError:
			await msg.clear_reactions()
			await msg.edit(embed=discord.Embed(title="點歌已取消", color=discord.Colour.red()).set_footer(
				text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url))
		else:
			if str(reaction) == "✅":
				try:
					vc = await vc.channel.connect()
				except :
					for x in self.client.voice_clients:
						if x.guild == ctx.guild:
							vc = x
					await vc.disconnect()
					vc = await vc.channel.connect()
				with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
					info = ydl.extract_info(url, download=False)
					URL = info['formats'][0]['url']
				ffm = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
						'options': '-vn'}
				count, timecount = 0, 0
				await msg.clear_reactions()
				await msg.add_reaction("⏹️")
				data = requests.get(html).json()
				data["music"] = msg.id
				requests.put(html1, params={"id": html2}, json=data)
				while True:
						vc.play(discord.FFmpegPCMAudio(URL, **ffm))
						count += 1
						while vc.is_playing():
							timecount += 1
							embed = discord.Embed(title=result["title"], url=result["webpage_url"], description="可以用`~stop_repeat`停止循環", color=random.randint(0,0xffffff))
							embed.set_author(name=f"Uploader: {result['uploader']}", url=result["uploader_url"])
							embed.set_image(url=result["thumbnail"])
							embed.set_footer(text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url)
							embed.add_field(name="音樂長短", value=str(datetime.timedelta(seconds=result["duration"])), inline=True)
							embed.add_field(name="觀看次數", value=result["view_count"], inline=True)
							embed.add_field(name="平均評分", value=result["average_rating"], inline=True)
							embed.add_field(name="無限重複", value="✅", inline=True)
							embed.add_field(name="time", value=str(datetime.timedelta(seconds=timecount)), inline=True)
							embed.add_field(name="count", value=count, inline=True)
							await msg.edit(embed=embed)
							await asyncio.sleep(1)
							data = requests.get(html).json()
							if data["music"] != msg.id:
								vc.stop()
								await vc.disconnect()
								await msg.edit(embed=discord.Embed(title="音樂停止", color=discord.Colour.red()).set_footer(text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url))
								break
			else:
				await msg.clear_reactions()
				await msg.edit(embed=discord.Embed(title="點歌已取消", color=discord.Colour.red()).set_footer(
					text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url))




	@commands.command(name="play_url")
	async def play_url(self, ctx, *, url: str):
		await ctx.message.delete()
		vc = ctx.author.voice
		ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
		if "www.youtube.com/watch?v=" in url:
			with ydl:
				result = ydl.extract_info(url, download=False)
		else:
			with ydl:
				result = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
		embed = discord.Embed(title=result["title"], url=result["webpage_url"], description=f"description```{result['description']}```")
		embed.set_author(name=f"Uploader: {result['uploader']}", url=result["uploader_url"])
		embed.set_image(url=result["thumbnail"])
		embed.set_footer(text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url)
		embed.add_field(name="音樂長短", value=str(datetime.timedelta(seconds=result["duration"])), inline=True)
		embed.add_field(name="觀看次數", value=result["view_count"], inline=True)
		embed.add_field(name="平均評分", value=result["average_rating"], inline=True)
		embed.add_field(name="喜歡", value=result["like_count"], inline=True)
		embed.add_field(name="不喜歡", value=result["dislike_count"], inline=True)
		msg = await ctx.send(embed=embed)
		await msg.add_reaction("✅")
		await msg.add_reaction("❌")

		def check(reaction, user):
			return user == ctx.message.author and str(reaction.emoji) in ["✅", "❌"] and msg.id == reaction.message.id 

		try:
			reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check)
		except asyncio.TimeoutError:
			await msg.clear_reactions()
			await msg.edit(embed=discord.Embed(title="點歌已取消", color=discord.Colour.red()).set_footer(
				text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url))
		else:
			if str(reaction) == "✅":
				try:
					vc = await vc.channel.connect()
				except :
					for x in self.client.voice_clients:
						if x.guild == ctx.guild:
							vc = x
					await vc.disconnect()
					vc = await vc.channel.connect()
				if "www.youtube.com/watch?v=" in url:
					with youtube_dl.YoutubeDL({'format': 'worstaudio'}) as ydl:
						info = ydl.extract_info(url, download=False)
						URL = info['formats'][0]['url']
				else:
					with youtube_dl.YoutubeDL({'format': 'worstaudio'}) as ydl:
						info = ydl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
						URL = info['formats'][0]['url']
				ffm = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
						'options': '-vn'}
				vc.play(discord.FFmpegPCMAudio(URL, **ffm))
				await msg.clear_reactions()
				embed = discord.Embed(title=result["title"], url=result["webpage_url"], color=discord.Colour.green())
				embed.set_author(name=f"Uploader: {result['uploader']}", url=result["uploader_url"])
				embed.set_image(url=result["thumbnail"])
				embed.set_footer(text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url)
				embed.add_field(name="音樂長短", value=str(datetime.timedelta(seconds=result["duration"])), inline=True)
				embed.add_field(name="觀看次數", value=result["view_count"], inline=True)
				embed.add_field(name="平均評分", value=result["average_rating"], inline=True)
				embed.add_field(name="喜歡", value=result["like_count"], inline=True)
				embed.add_field(name="不喜歡", value=result["dislike_count"], inline=True)
				await msg.edit(embed=embed)
			else:
				await msg.clear_reactions()
				await msg.edit(embed=discord.Embed(title="點歌已取消", color=discord.Colour.red()).set_footer(
					text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url))

	@commands.command(name="repeat")
	async def repeat(self, ctx, url: str):
		await ctx.message.delete()
		vc = ctx.author.voice
		ydl = youtube_dl.YoutubeDL({'outtmpl': '%(id)s.%(ext)s'})
		with ydl:
			result = ydl.extract_info(url, download=False)
		embed = discord.Embed(title=result["title"], url=result["webpage_url"], description=f"description```{result['description']}```")
		embed.set_author(name=f"Uploader: {result['uploader']}", url=result["uploader_url"])
		embed.set_image(url=result["thumbnail"])
		embed.set_footer(text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url)
		embed.add_field(name="音樂長短", value=str(datetime.timedelta(seconds=result["duration"])), inline=True)
		embed.add_field(name="觀看次數", value=result["view_count"], inline=True)
		embed.add_field(name="平均評分", value=result["average_rating"], inline=True)
		embed.add_field(name="喜歡", value=result["like_count"], inline=True)
		embed.add_field(name="不喜歡", value=result["dislike_count"], inline=True)
		msg = await ctx.send(embed=embed)
		await msg.add_reaction("✅")
		await msg.add_reaction("❌")

		def check(reaction, user):
			return user == ctx.message.author and str(reaction.emoji) in ["✅", "❌"] and msg.id == reaction.message.id 

		try:
			reaction, user = await self.client.wait_for('reaction_add', timeout=30, check=check)
		except asyncio.TimeoutError:
			await msg.clear_reactions()
			await msg.edit(embed=discord.Embed(title="點歌已取消", color=discord.Colour.red()).set_footer(
				text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url))
		else:
			if str(reaction) == "✅":
				try:
					vc = await vc.channel.connect()
				except :
					for x in self.client.voice_clients:
						if x.guild == ctx.guild:
							vc = x
					await vc.disconnect()
					vc = await vc.channel.connect()
				with youtube_dl.YoutubeDL({'format': 'bestaudio'}) as ydl:
					info = ydl.extract_info(url, download=False)
					URL = info['formats'][0]['url']
				ffm = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
						'options': '-vn'}
				vc.play(discord.FFmpegPCMAudio(URL, **ffm))
				count, timecount = 0, 0
				await msg.clear_reactions()
				await msg.add_reaction("⏹️")
				
				data = requests.get(html).json()
				data["music"] = msg.id
				requests.put(html1, params={"id": html2}, json=data)
				while True:
						count += 1
						while vc.is_playing():
							timecount += 1
							embed = discord.Embed(title=result["title"], url=result["webpage_url"], description="可以用`~stop_repeat`停止循環", color=random.randint(0,0xffffff))
							embed.set_author(name=f"Uploader: {result['uploader']}", url=result["uploader_url"])
							embed.set_image(url=result["thumbnail"])
							embed.set_footer(text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url)
							embed.add_field(name="音樂長短", value=str(datetime.timedelta(seconds=result["duration"])), inline=True)
							embed.add_field(name="觀看次數", value=result["view_count"], inline=True)
							embed.add_field(name="平均評分", value=result["average_rating"], inline=True)
							embed.add_field(name="無限重複", value="✅", inline=True)
							embed.add_field(name="time", value=str(datetime.timedelta(seconds=timecount)), inline=True)
							embed.add_field(name="count", value=count, inline=True)
							await msg.edit(embed=embed)
							await asyncio.sleep(1)
							data = requests.get(html).json()
							if data["music"] != msg.id:
								vc.stop()
								await vc.disconnect()
								await msg.edit(embed=discord.Embed(title="音樂停止", color=discord.Colour.red()).set_footer(text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url))
								break
						vc.play(discord.FFmpegPCMAudio(URL, **ffm))
			else:
				await msg.clear_reactions()
				await msg.edit(embed=discord.Embed(title="點歌已取消", color=discord.Colour.red()).set_footer(
					text=f"Add by: {ctx.author}", icon_url=ctx.author.avatar_url))

def setup(client):
	client.add_cog(song(client))
