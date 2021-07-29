from discord.ext import commands
from cogs.core import core
import requests
import discord

Admin = [610381826284060692, 455259347107446794, 599966693338644482, 499233545693298698]
import os
html = os.environ["html"]
html1 = os.environ["html1"]
html2 = os.environ["html2"]


class control(core):

    @commands.command()
    async def add(self, ctx, 級: int, 會員: str):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            if 級 == 1:
                data["data"]["one"].append(會員)
            elif 級 == 2:
                data["data"]["two"].append(會員)
            elif 級 == 3:
                data["data"]["three"].append(會員)
            elif 級 == -1:
                data["data"]["one"].remove(會員)
            elif 級 == -2:
                data["data"]["two"].remove(會員)
            elif 級 == -3:
                data["data"]["three"].remove(會員)
            requests.put(html1, params={"id": html2}, json=data)
            await ctx.message.delete()

    @commands.command()
    async def money(self, ctx, aom: str, money: int):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            if aom == "+":
                data["data"]["money"] += money
                await ctx.message.delete()
            elif aom == "-":
                data["data"]["money"] -= money
                await ctx.message.delete()
            elif aom == "=":
                data["data"]["money"] = money
                await ctx.message.delete()
            requests.put(html1, params={"id": html2}, json=data)
            await ctx.message.delete()

    @commands.command()
    async def star(self, ctx, aom: str, star: int):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            if aom == "+":
                data["data"]["star"] += star
            elif aom == "-":
                data["data"]["star"] -= star
            elif aom == "=":
                data["data"]["star"] = star
            requests.put(html1, params={"id": html2}, json=data)
            await ctx.message.delete()

    @commands.command()
    async def reload_bgt(self, ctx):
        try:
            self.client.unload_extension("cogs.money.bgt")
            self.client.load_extension("cogs.money.bgt")
        except:
            pass


def setup(bot):
    bot.add_cog(control(bot))
