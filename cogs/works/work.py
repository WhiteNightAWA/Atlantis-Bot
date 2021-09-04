from cogs.core import core
from discord.ext import commands
from dotenv import load_dotenv

import discord
import datetime
import os
import requests

load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")


class Work(core):

    @commands.command()
    async def 招聘勞工(self, ctx, num: int, money: int, info: str, minecraft_id: str):
        await ctx.message.delete()
        data = requests.get(html).json()
        no = int(max(data["work"])) + 1
        time_end = datetime.datetime.utcnow().replace(microsecond=0) + datetime.timedelta(days=3)
        int_time = time_end
        embed = discord.Embed(
            title=f"`{ctx.author.name}`勞工招募:",
            description=f"#{no}",
            color=discord.Color.green(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=ctx.author,
            icon_url=ctx.author.avatar_url
        ).add_field(
            name="工作內容",
            value=f"```{info}```",
            inline=False
        ).add_field(
            name="人數",
            value=f"```{num}```",
            inline=True
        ).add_field(
            name="薪水",
            value=f"```${money}```",
            inline=True
        ).add_field(
            name="招聘者",
            value=f"<@!{ctx.author.id}>\nMinecraft ID: `{minecraft_id}`",
            inline=True
        ).add_field(
            name="剩餘時間",
            value=f"<t:{int_time}:R>",
            inline=False
        )

        data["work"][str(no)] = {
            "info": info,
            "money": money,
            "minecraft_id": minecraft_id,
            "user_id": ctx.author.id,
            "num": num,
            "time": time_end.isoformat()
        }
        channel = self.client.get_channel(883391652687933440)
        requests.put(html1, params={"id": html2}, json=data)
        await channel.send(embed=embed)
        await ctx.send(embed=discord.Embed(title="Success!",
                                           description="Posted at <#883391652687933440>",
                                           color=discord.Color.green()))

    @commands.command()
    async def 接受工作(self, ctx, no: int, minecraft_id: str, times: str):
        await ctx.message.delete()
        data = requests.get(html).json()
        if str(no) in data["work"]:
            d = data["work"][str(no)]

            embed = discord.Embed(title=f"`{ctx.author}`接受你的工作",
                                  description=f"<@!{ctx.author.id}>",
                                  timestamp=datetime.datetime.utcnow()).set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar_url
            ).add_field(
                name="玩家ID",
                value=minecraft_id
            ).add_field(
                name="方便聯絡時間",
                value=times
            )

            member = self.client.get_user(d["user_id"])
            await member.send(embed=embed)
            await ctx.send(embed=discord.Embed(title="Done!",
                                               description="請等待回复",
                                               color=discord.Color.red(),
                                               timestamp=datetime.datetime.utcnow()))

        else:
            await ctx.send(embed=discord.Embed(title="錯誤的編號",
                                               color=discord.Color.red(),
                                               timestamp=datetime.datetime.utcnow()
                                               ).set_author(
                name=ctx.author,
                icon_url=ctx.author.avatar_url
            ))


def setup(client):
    client.add_cog(Work(client))
