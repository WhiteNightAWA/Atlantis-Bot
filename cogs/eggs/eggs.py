from cogs.core import core
from discord.ext import commands
import discord, random, asyncio, requests
import os
html = os.environ["html"]
html1 = os.environ["html1"]
html2 = os.environ["html2"]

class eggs(core):
  
  @commands.Cog.listener()
  async def on_message(self, message):
    guild = message.guild
    if "木貓女裝" in message.content:
      role = guild.get_role(866685565071654973)
      await message.author.add_roles(role)
      await message.author.send(embed=discord.Embed(title="恭喜你找到`彩蛋#1`：所以說木貓你什麼時候女裝啦！", color=random.randint(0, 0xffffff)))
    if "地圖繪" in message.content:
      msg = await message.reply("discord.gg/JhzQTGAgUH")
      await asyncio.sleep(5)
      await msg.delete()
    if message.channel.id == 866672030454382662:
      if not str(message.content).startswith("~"):
        if not str(message.content).startswith("!"):
          if not message.author.bot:
            data = requests.get(html).json()
            try:
              data["eggs"]["3"][str(message.author.id)] += 1
            except:
              data["eggs"]["3"][str(message.author.id)] = 1
            if int(data["eggs"]["3"][str(message.author.id)]) == 50:
              role = guild.get_role(866693496689262652)
              await message.author.add_roles(role)
              await message.author.send(embed=discord.Embed(title="恭喜你找到`彩蛋#3`：所以說這是指令使用區啦！", color=random.randint(0, 0xffffff)))
            requests.put(html1, params={"id": html2}, json=data)
    if "小卯" in message.content:
      role = guild.get_role(866696175117402122)
      await message.author.add_roles(role)
      await message.author.send(embed=discord.Embed(title="恭喜你找到`彩蛋#4`：叫我嗎awa", color=random.randint(0, 0xffffff)))
      
    

  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    guild = self.client.get_guild(payload.guild_id)
    member = payload.member
    channel = self.client.get_channel(858582338347073536)
    message = await channel.fetch_message(867004190617763881)
    emoji = self.client.get_emoji(865847027715014677)
    if payload.message_id == 867004190617763881 and payload.emoji.id == 865847027715014677:
      await message.remove_reaction(emoji, member)
      role = guild.get_role(866689738852663366)
      await member.add_roles(role)
      await member.send(embed=discord.Embed(title="恭喜你找到`彩蛋#2`：所以你為啥:MuMao_1:啦！", color=random.randint(0, 0xffffff)))


def setup(client):
  client.add_cog(eggs(client))
