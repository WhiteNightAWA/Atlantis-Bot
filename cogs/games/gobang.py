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
        text_cb = text_cb + "X"
    elif y == 2:
        text_cb = text_cb + "O"
    if c == 15:
        text_cb = text_cb + "\n"
    else:
        text_cb = text_cb + "═══"
    return text_cb


async def get_text(cb):
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


async def check_winner(cb):
    winner = None
    for y in cb:
        for x in range(11):
            if y[x] == y[x + 1] == y[x + 2] == y[x + 3] == y[x + 4] and y[x] != 0:
                winner = y[x]
    for x in range(11):
        for y in range(11):
            if cb[x][y] == cb[x + 1][y] == cb[x + 2][y] == cb[x + 3][y] == cb[x + 4][y] and cb[x][y] != 0:
                winner = cb[x][y]
    for x in range(11):
        for y in range(11):
            if cb[x][y] == cb[x + 1][y + 1] == cb[x + 2][y + 2] == cb[x + 3][y + 3] == cb[x + 4][y + 4] and cb[x][
                y] != 0:
                winner = cb[x][y]
            elif cb[x][y + 4] == cb[x + 1][y + 3] == cb[x + 2][y + 2] == cb[x + 3][y + 1] == cb[x + 4][y] and cb[x][
                y] != 0:
                winner = cb[x][y]
    d = None
    for x in cb:
        for y in x:
            if y == 0:
                d = 1
    if d is None:
        winner = "draw"
    return winner


class gobang(core):

    @commands.command()
    async def gobang(self, ctx, p2: discord.Member):
        if p2.bot:
            pass
        else:
            msg = await ctx.send(content=f"<@!{p2.id}>",
                                 embed=discord.Embed(title=f"`{ctx.author}`邀請你玩五子棋", color=random.randint(0, 0xffffff)))
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
                    cb = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
                    await msg.edit(embed=discord.Embed(title=f"`{ctx.author}`的回合", color=random.randint(0, 0xffffff),
                                                       description=f"P1 (X): <@!{ctx.author.id}>\nP2 (O): <@!{p2.id}>\n**棋盤:**\n{await get_text(cb)}"))
                    winner, now = None, ctx.author.id
                    while True:
                        def check(m):
                            if str(m.content) == "退出" and m.author.id in [ctx.author.id, p2.id]:
                                return True
                            if str(m.content[0]).upper() in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L",
                                                             "M", "N", "O"] and m.author.id == now:
                                try:
                                    if int(m.content[1:]) in range(1, 16):
                                        return True
                                except ValueError:
                                    pass
                            return False

                        inp = await self.client.wait_for("message", check=check)
                        if str(inp.content) != "退出":
                            y = int(inp.content[1:]) - 1
                            x = int(ord(str(inp.content[0].upper())) - 65)
                            if cb[y][x] == 0:
                                await inp.delete()
                                await ctx.send(f"{y}{x}")
                                if now == ctx.author.id:
                                    cb[y][x] = 1
                                    now, next, last = p2.id, p2, ctx.author
                                elif now == p2.id:
                                    cb[y][x] = 2
                                    now, next, last = ctx.author.id, ctx.author, p2
                                winner = await check_winner(cb)
                                if winner in [1, 2]:
                                    await msg.edit(
                                        embed=discord.Embed(title=f"`{last}`勝利", color=random.randint(0, 0xffffff),
                                                            description=f"P1 (X): <@!{ctx.author.id}>\nP2 (O): <@!{p2.id}>\n**棋盤:**\n{await get_text(cb)}"))
                                    data = requests.get(html).json()
                                    if str(last.id) in data["gobang"]:
                                        data["gobang"][str(last.id)] += 1
                                    else:
                                        data["gobang"][str(last.id)] = 1
                                    requests.put(html1, params={"id": html2}, json=data)
                                    return
                                elif winner == "draw":
                                    await msg.edit(embed=discord.Embed(title=f"平局", color=random.randint(0, 0xffffff),
                                                                       description=f"P1 (X): <@!{ctx.author.id}>\nP2 (O): <@!{p2.id}>\n**棋盤:**\n{await get_text(cb)}"))
                                    return
                                elif winner is None:
                                    await msg.edit(
                                        embed=discord.Embed(title=f"`{next}`的回合", color=random.randint(0, 0xffffff),
                                                            description=f"P1 (X): <@!{ctx.author.id}>\nP2 (O): <@!{p2.id}>\n**棋盤:**\n{await get_text(cb)}"))
                            else:
                                if cb[y][x] == 1:
                                    w = "X"
                                else:
                                    w = "O"
                                await inp.reply(embed=discord.Embed(title=f"這個位置已經有棋{w}了", color=discord.Colour.red()))
                        else:
                            if inp.author.id == ctx.author.id:
                                others = p2
                            else:
                                others = ctx.author
                            message = await ctx.send(embed=discord.Embed(
                                title=f"{inp.author}想退出, 如30秒後對方沒有回應, 將會自動退出...",
                                description=f"<@!{others.id}若不想退出, 輸入`no`>"))

                            def check2(m):
                                return m.author.id == others.id and str(m.content).lower() == "no"

                            try:
                                msg = await self.client.wait_for("message", check=check2, timeout=30)
                            except asyncio.TimeoutError:
                                await msg.delete()
                                await message.delete()
                                await inp.delete()
                                await msg.edit(
                                    embed=discord.Embed(title=f"`{inp.author}`退出了", color=random.randint(0, 0xffffff),
                                                        description=f"P1 (X): <@!{ctx.author.id}>\nP2 (O): <@!{p2.id}>\n**棋盤:**\n{await get_text(cb)}"))
                                return
                            await msg.delete()
                            await message.delete()
                            await inp.delete()
                            await ctx.send(embed=discord.Embed(title=f"`退出失敗`", color=discord.Colour.red()))
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                await msg.edit(content="", embed=discord.Embed(title="邀請超時", color=discord.Colour.red()))


def setup(client):
    client.add_cog(gobang(client))
