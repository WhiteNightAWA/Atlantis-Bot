from cogs.core import core
from discord.ext import commands
import discord, random, requests
import os
from dotenv import load_dotenv
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")

class count_down(core):
	
  @commands.Cog.listener()
  async def on_raw_message_edit(self, payload):
    if payload.channel_id == 867771687202062336:
      message = await self.client.get_channel(867771687202062336).fetch_message(payload.message_id)
      await message.delete()
  
  @commands.command()
  async def set_countdown_number(self, ctx, 數字: int):
    await ctx.send(數字)

  @commands.command()
  async def 查看countdown分數(self, ctx):
    data = requests.get(html).json()
    id = str(ctx.author.id)
    if id in data["countdown"]:
      await ctx.send(f"<@{ctx.author.id}> 的分數為 : {data['countdown'][id]}")
    else:
      await ctx.send(f"<@{ctx.author.id}> 的分數為 : 0")
    await ctx.message.delete()

  @commands.command()
  async def 查看countdown排行榜(self, ctx):
    data = requests.get(html).json()
    dictset = sorted(data["countdown"].items(), key = lambda d: d[1], reverse=True)
    text, count = "", 0
    for x in dictset:
    	text = text + f"第`{count+1}`名：<@{dictset[count][0]}>  分數：`{dictset[count][1]}`\n"
    	count += 1
    await ctx.send(embed=discord.Embed(title="**COUNTDOWN**排行榜", description=text, color=random.randint(0, 0xffffff)))
    #await ctx.send(embed=discord.Embed(title="countdown排行榜", description=f"第一名：<@{dictset[0][0]}>  分數：`{dictset[0][1]}`\n第二名：<@{dictset[1][0]}>  分數：`{dictset[1][1]}`\n第三名：<@{dictset[2][0]}>  分數：`{dictset[2][1]}`\n第四名：<@{dictset[3][0]}>  分數：`{dictset[3][1]}`\n第五名：<@{dictset[4][0]}>  分數：`{dictset[4][1]}`", color=random.randint(0, 0xffffff)))
    await ctx.message.delete()

  @commands.Cog.listener()
  async def on_message(self, message):
    if message.channel.id == 867771687202062336 and not message.author.bot: #檢查訊息是否在該頻道及是否機器人
      #if message.author.id == 841678712767512597 or message.author.bot:
      #  return
      msgs = await message.channel.history(limit=2).flatten() #取得該頻道最近兩條訊息
      if msgs[0].author.id == msgs[1].author.id and message.author.id != 841678712767512597: #檢查兩條訊息是否由同一個人發送 
        await message.delete() #如果是就刪除
      else:
        if message.author.id != 841678712767512597: #如果發送者不是小卯機器人
          try:
            int(message.content) #嘗試把訊息轉成數字
          except:
            await message.delete()
            return  #如果失敗就刪除訊息及退出程式
        m1, m2 = int(message.content), int(msgs[1].content) #將m1, m2設定成最近兩條訊息
        if m1 != m2-1 and m1 != m2-2: #如果m1不等於m2+1
          await message.delete() #就刪除訊息
        if m1 <= 0: #如果m1等於0
          await message.delete() #就刪除訊息
        else:
          data = requests.get(html).json() #取得資料
          if m1 == 1: #如果m1等於答案
            await message.channel.purge(limit=None) #清空
            if str(message.author.id) in data["countdown"]:
              data["countdown"][str(message.author.id)] += 1
            else:
              data["countdown"][str(message.author.id)] = 1
            await message.channel.send(embed=discord.Embed(title=f"新局開始!", description=f"上局得分者為： <@{message.author.id}>", color=random.randint(0, 0xffffff)))#發訊息
            await message.channel.send("100")
          requests.put(html1, params={"id": html2}, json=data) #上載

def setup(client):
  client.add_cog(count_down(client))
