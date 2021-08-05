import discord
import asyncio
from cogs.core import core
from discord.ext import commands
from dotenv import load_dotenv
import os
import random
import requests
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")


def fill(text_cb, no, y, c, count):
    if c == 1:
        if len(str(count)) == 1:
            text_cb = text_cb + f"0{count}"
        else:
            text_cb = text_cb + str(count)
    if y == 0:
        text_cb = text_cb + no
    elif y == 1:
        text_cb = text_cb + "●"
    elif y == 2:
        text_cb = text_cb + "○"
    if c == 15:
        text_cb = text_cb + "\n"
    else:
        text_cb = text_cb + "═══"
    return text_cb


def get_text(cb):
    count = 1
    text_cb = "```\n  A   B   C   D   E   F   G   H   I   J   K   L   M   N   O\n"
    for x in cb:
        c = 1
        if count == 1:
            for y in x:
                if c == 1:
                    no = "╔"
                elif c == 15:
                    no = "╗"
                else:
                    no = "╦"
                text_cb = fill(text_cb, no, y, c, count)
                c += 1
            text_cb = text_cb + "  ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║\n"
        elif count == 15:
            for y in x:
                if c == 1:
                    no = "╚"
                elif c == 15:
                    no = "╝"
                else:
                    no = "╩"
                text_cb = fill(text_cb, no, y, c, count)
                c += 1
        else:
            for y in x:
                if c == 1:
                    no = "╠"
                elif c == 15:
                    no = "╣"
                else:
                    no = "╬"
                text_cb = fill(text_cb, no, y, c, count)
                c += 1
            text_cb = text_cb + "  ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║   ║\n"
        count += 1
    text_cb = text_cb + "```"
    return text_cb


class gobang(core):

    @commands.command()
    async def gobang(self, ctx, p2: discord.Member):
        if p2.bot:
            pass
        else:
            msg = await ctx.send(content=f"<@!{p2.id}>",
                                 embed=discord.Embed(title=f"`{ctx.author}`邀請你玩井字棋", color=random.randint(0, 0xffffff)))
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            try:
                def check(payload):
                    return payload.member.id == p2.id and str(payload.emoji) in ["✅",
                                                                                 "❌"] and payload.message_id == msg.id

                payload = await self.client.wait_for("raw_reaction_add", timeout=30, check=check)
                await msg.clear_reactions()
                if str(payload.emoji) == "✅":
                    await msg.edit(content="", embed=discord.Embed(title="遊戲即將開始", color=discord.Colour.green()))
                    cb = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
                    data = requests.get(html).json()
                    data["tic_tac_toe"][str(msg.id)] = {"player": {str(ctx.author.id): 1, str(p2.id): 2},
                                                        "round": ctx.author.id, "cb": cb}
                    await msg.edit(embed=discord.Embed(title=f"`{ctx.author}`的回合", color=random.randint(0, 0xffffff),
                                                       description=f"P1 (:x:): <@!{ctx.author.id}>\nP2 (:o:): <@!{p2.id}>").add_field(
                        name="棋盤", value=await get_text(cb)))
                    # requests.put(html1, params={"id": html2}, json=data)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                await msg.edit(content="", embed=discord.Embed(title="邀請超時", color=discord.Colour.red()))


def setup(client):
    client.add_cog(gobang(client))