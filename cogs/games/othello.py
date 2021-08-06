import random
import discord
import asyncio
from cogs.core import core
from discord.ext import commands


def changes(num):
    c = 1
    for t in [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:"]:
        if c == num:
            return t
        c += 1


def isOnBoard(x, y):
    return x >= 0 and x <= 7 and y >= 0 and y <= 7


def isValidMove(board, tile, xstart, ystart):
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != 0:
        return False
    board[xstart][ystart] = tile
    if tile == 1:
        otherTile = 2
    else:
        otherTile = 1
    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToFlip.append([x, y])
    board[xstart][ystart] = 0
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


def isGameOver(board):
    for x in board:
        for y in x:
            if y == 0:
                return False
    return True


def getValidMoves(board, tile):
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
    return validMoves


def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 1:
                xscore += 1
            if board[x][y] == 2:
                oscore += 1
    return {"1": xscore, "2": oscore}


def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)
    if tilesToFlip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return board


async def get_text(cb):
    bc = str(random.choice(
        [":yellow_square:", ":red_square:", ":purple_square:", ":orange_square:", ":green_square:", ":brown_square:",
         ":blue_square:"]))
    t = ":black_large_square::regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:\n"
    count = 1
    for x in cb:
        t += str(changes(int(count)))
        count += 1
        for y in x:
            if y == 0:
                t += bc
            elif y == 1:
                t += ":black_circle:"
            elif y == 2:
                t += ":white_circle:"
        t += "\n"
    t = t[:-1]
    return t


class othello(core):

    @commands.command()
    async def othello(self, ctx, p2: discord.Member):
        if p2.bot:
            await ctx.send(embed=discord.Embed(title=f"暫未支持與機器人對戰awa...", color=discord.Colour.red()))
        elif p2.id == ctx.author.id:
            await ctx.send(embed=discord.Embed(title=f"你不能與自己對戰awa...", color=discord.Colour.red()))
        else:
            msg = await ctx.send(content=f"<@!{p2.id}>",
                                 embed=discord.Embed(title=f"`{ctx.author}`邀請你玩黑白棋", color=random.randint(0, 0xffffff)))
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
                    cb = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 2, 1, 0, 0, 0], [0, 0, 0, 1, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]
                    await msg.edit(embed=discord.Embed(title=f"`{ctx.author}`的回合", color=random.randint(0, 0xffffff),
                                                       description=f"P1 (:black_circle:): <@!{ctx.author.id}>\nP2 (:white_circle:): <@!{p2.id}>\n**棋盤:**\n{await get_text(cb)}").set_footer(
                        text="請不要同時進行兩局遊戲, 若等待對方時間過長, 你可`輸入`退出退出遊戲(需等待一段時間後對方無回應"))
                    winner, next_p = None, ctx.author
                    while True:
                        def check(m):
                            if str(m.content) == "退出" and m.author.id in [ctx.author.id, p2.id]:
                                return True
                            try:
                                sn = str(m.content[0]).upper()
                            except:
                                sn = "Z"
                            if sn in ["A", "B", "C", "D", "E", "F", "G", "H"] and next_p.id == m.author.id:
                                try:
                                    if int(m.content[1:]) in range(1, 9):
                                        return True
                                except ValueError:
                                    pass
                            return False

                        inp = await self.client.wait_for("message", check=check)

                        if isGameOver(cb):
                            mark = getScoreOfBoard(cb)
                            ma, mb = mark["1"], mark["2"]
                            winner = max(ma, mb)
                            if winner == ma:
                                winner = ctx.author
                            else:
                                winner = p2
                            await msg.edit(embed=discord.Embed(title=f"`{winner}`勝利", color=random.randint(0, 0xffffff),
                                                               description=f"P1 (:black_circle:): <@!{ctx.author.id}> : `{mark['1']}`\nP2 (:white_circle:): <@!{p2.id}> : `{mark['2']}`\n**棋盤:**\n{await get_text(cb)}"))

                        if str(inp.content) != "退出":
                            if inp.author.id == ctx.author.id:
                                tile = 1
                                next = 2
                                next_p = p2
                            else:
                                tile = 2
                                next = 1
                                next_p = ctx.author
                            x = int(inp.content[1:]) - 1
                            y = int(ord(str(inp.content[0].upper())) - 65)
                            vmove = getValidMoves(cb, tile)
                            print(x, y)

                            if [x, y] in vmove:
                                await inp.delete()
                                cb = makeMove(cb, tile, x, y)
                                if isGameOver(cb):
                                    mark = getScoreOfBoard(cb)
                                    ma, mb = mark["1"], mark["2"]
                                    winner = max(ma, mb)
                                    if winner == ma:
                                        winner = ctx.author
                                    else:
                                        winner = p2
                                    await msg.edit(
                                        embed=discord.Embed(title=f"`{winner}`勝利", color=random.randint(0, 0xffffff),
                                                            description=f"P1 (:black_circle:): <@!{ctx.author.id}> : `{mark['1']}`\nP2 (:white_circle:): <@!{p2.id}> : `{mark['2']}`\n**棋盤:**\n{await get_text(cb)}"))
                                mark = getScoreOfBoard(cb)
                                await msg.edit(
                                    embed=discord.Embed(title=f"`{next_p}`的回合", color=random.randint(0, 0xffffff),
                                                        description=f"P1 (:black_circle:): <@!{ctx.author.id}> : `{mark['1']}`\nP2 (:white_circle:): <@!{p2.id}> : `{mark['2']}`\n**棋盤:**\n{await get_text(cb)}").set_footer(
                                        text="請不要同時進行兩局遊戲, 若等待對方時間過長, 你可`輸入`退出退出遊戲(需等待一段時間後對方無回應)"))

                                if getValidMoves(cb, next) == []:
                                    await ctx.send(content=f"<@!{inp.author.id}> 沒有可以出的棋, 直接跳過這一輪!")
                                    if inp.author.id == ctx.author.id:
                                        tile = 2
                                        next = 1
                                        next_p = ctx.author
                                    else:
                                        tile = 1
                                        next = 2
                                        next_p = p2
                                    await msg.edit(
                                        embed=discord.Embed(title=f"`{next_p}`的回合", color=random.randint(0, 0xffffff),
                                                            description=f"P1 (:black_circle:): <@!{ctx.author.id}> : `{mark['1']}`\nP2 (:white_circle:): <@!{p2.id}> : `{mark['2']}`\n**棋盤:**\n{await get_text(cb)}").set_footer(
                                            text="請不要同時進行兩局遊戲, 若等待對方時間過長, 你可`輸入`退出退出遊戲(需等待一段時間後對方無回應)"))
                            else:
                                await inp.delete()
                                await ctx.send(content=f"<@!{inp.author.id}>:warning: 這步棋`{inp.content}`不符合黑白棋規則!")
                                if inp.author.id == ctx.author.id:
                                    tile = 2
                                    next = 1
                                    next_p = ctx.author
                                else:
                                    tile = 1
                                    next = 2
                                    next_p = p2
                        else:
                            if inp.author.id == ctx.author.id:
                                others = p2
                            else:
                                others = ctx.author
                            message = await ctx.send(embed=discord.Embed(
                                title=f"{inp.author}想退出, 如30秒後對方沒有回應, 將會自動退出...",
                                description=f"<@!{others.id}>若不想退出, 輸入`no`"))

                            def check2(m):
                                return m.author.id == others.id and str(m.content).lower() == "no"

                            try:
                                msg2 = await self.client.wait_for("message", check=check2, timeout=30)
                            except asyncio.TimeoutError:
                                await message.delete()
                                await inp.delete()
                                await msg.edit(
                                    embed=discord.Embed(title=f"`{inp.author}`退出了", color=random.randint(0, 0xffffff),
                                                        description=f"P1 (X): <@!{ctx.author.id}>\nP2 (O): <@!{p2.id}>\n**棋盤:**\n{await get_text(cb)}"))
                                return
                            await msg2.delete()
                            await message.delete()
                            await inp.delete()
                            await ctx.send(embed=discord.Embed(title=f"`退出失敗`", color=discord.Colour.red()))
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                await msg.edit(content="", embed=discord.Embed(title="邀請超時", color=discord.Colour.red()))


def setup(client):
    client.add_cog(othello(client))
