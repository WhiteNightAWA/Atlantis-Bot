from cogs.core import core
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option, create_choice
import discord, datetime, requests, random

Admin = [455259347107446794, 721171337879748609, 610381826284060692, 499233545693298698, 404185635570581508,
         680360499803586569, 194425503963152384, 592658930879168512, 495209042818498562, 598121193924722689,
         328835900761047043, 560740155347042324, 609412150611673088, 652698396791930914, 587604693136572426,
         599966693338644482]
import os
html = os.environ["html"]
html1 = os.environ["html1"]
html2 = os.environ["html2"]


class point(core):

    @cog_ext.cog_slash(name="hello", description="打個招呼~")
    async def _hello(self, ctx: SlashContext):
        embed = discord.Embed(title=f"你好啊~{ctx.author.name}", color=0x00ff00, timestamp=datetime.datetime.utcnow())
        embed.add_field(name=f"我是在固體與液體之間的小卯owo\n歡迎來到小卯村 (人´∀｀)｡ﾟ+\n在這裡就好好玩吧\n有問題再/指令問我喔:hearts:", value="Owo",
                        inline=False)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="ping", description="查看機器人延遲")
    async def _ping(self, ctx: SlashContext):
        embed = discord.Embed(color=0x04ff00, timestamp=datetime.datetime.utcnow())
        embed.add_field(name="當前機器人延遲:", value=f"~{round(self.client.latency * 1000)}ms", inline=True)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="新増會員", description="/新増會員 [@成員]")
    async def _新増會員(self, ctx: SlashContext, 成員: discord.Member):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            id = 成員.id
            if id not in data:
                data["point"][id] = 0
                requests.put(html1, params={"id": html2}, json=data)
                await ctx.send(f"成功新増{成員}為會員")
            else:
                await ctx.send(f"{成員}已經是會員")
        else:
            await ctx.send("你不是管理員")

    @cog_ext.cog_slash(name="查看會員點數", description="/查看會員點數")
    async def _查看會員點數(self, ctx:SlashContext):
        data = requests.get(html).json()
        if str(ctx.author.id) in data:
            await ctx.send(f"你的會員點數為 : {data[str(ctx.author.id)]}")
        else:
            await ctx.send("你不是會員")

    @cog_ext.cog_slash(name="查看", description="/查看 [@會員]")
    async def _查看(self, ctx:SlashContext, 會員: discord.Member):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            id = 會員.id
            if id in data:
                await ctx.send(f"{會員}的會員點數為 : {data[str(id)]}")
            else:
                await ctx.send(f"{會員}不是會員")
        else:
            await ctx.send("你不是管理員")

    @cog_ext.cog_slash(name="增加會員點數", description="/增加會員點數 [@會員] 點數")
    async def _增加會員點數(self, ctx:SlashContext, 會員: discord.Member, 點數: int):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            id = 會員.id
            if id in data:
                add_point = 點數
                point = data["point"][id]
                new_point = point + add_point
                data["point"][id] = new_point
                requests.put(html1,
                             params={"id": html2}, json=data)
                await ctx.send(f"成功為{會員}增加{點數}點會員點數")
            else:
                await ctx.send(f"{會員}不是會員")
        else:
            await ctx.send("你不是管理員")

    @cog_ext.cog_slash(name="扣除會員點數", description="/扣除會員點數 [@會員] 點數")
    async def _扣除會員點數(self, ctx:SlashContext, 會員: discord.Member, 點數: int):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            id = 會員.id
            if id in data:
                add_point = 點數
                point = data["point"][id]
                new_point = point - add_point
                data["point"][id] = new_point
                requests.put(html1,
                             params={"id": html2}, json=data)
                await ctx.send(f"成功扣除{會員}{點數}點會員點數")
            else:
                await ctx.send(f"{會員}不是會員")
        else:
            await ctx.send("你不是管理員")

    @cog_ext.cog_slash(name="開始抽獎活動",
                 description="/開始抽獎活動 [最少數字] [最大數字] [同一個數字是否可以被選擇兩次或以上] [同一個人是否可以中獎兩次或以上] [是否只能抽中被人選擇的數字]",
                options=[
            create_option(name="最少數字", description="www", option_type=4, required=True),
            create_option(name="最大數字", description="www", option_type=4, required=True),
            create_option(name="同一個數字是否可以被選擇兩次或以上", description="www", option_type=5, required=True),
            create_option(name="同一個人是否可以中獎兩次或以上", description="www", option_type=5, required=True),
            create_option(name="是否只能抽中被人選擇的數字", description="www", option_type=5, required=True)
        ])
    async def _開始抽獎活動(self, ctx:SlashContext, 最少數字: int, 最大數字: int, 同一個數字是否可以被選擇兩次或以上: bool, 同一個人是否可以中獎兩次或以上: bool, 是否只能抽中被人選擇的數字: bool):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            if data["lucky"]["start"]:
                await ctx.send("抽獎活動已經開始")
            else:
                data["lucky"] = {}
                data["lucky"]["start"] = True
                data["lucky"]["smallest"] = 最少數字
                data["lucky"]["biggest"] = 最大數字
                data["lucky"]["same"] = 同一個數字是否可以被選擇兩次或以上
                data["lucky"]["dowle"] = 同一個人是否可以中獎兩次或以上
                data["lucky"]["num"] = []
                data["lucky"]["user"] = {}
                data["lucky"]["get"] = False
                data["lucky"]["ok"] = []
                data["lucky"]["select"] = 是否只能抽中被人選擇的數字
                data["lucky"]["n"] = 0
                data["lucky"]["output"] = ""
                requests.put(html1, params={"id": html2}, json=data)
                await ctx.send(
                    f"@everyone！抽獎活動開始，最少可選擇數字：{最少數字}，最大可選擇數字：{最大數字}，同一個數字是否可以被選擇兩次或以上：{同一個數字是否可以被選擇兩次或以上}，同一個人是否可以中獎兩次或以上：{同一個人是否可以中獎兩次或以上}，是否只能抽中被人選擇的數字：{是否只能抽中被人選擇的數字}。")
        else:
            await ctx.send("你不是管理員")

    @cog_ext.cog_slash(name="設定我的幸運數字", description="/設定我的幸運數字 [數字]")
    async def _設定我的幸運數字(self, ctx:SlashContext, 數字: int):
        data = requests.get(html).json()
        print("ok")
        if data["lucky"]["get"]:
            if data["lucky"]["start"]:
                if str(ctx.author.id) not in data["lucky"]["ok"]:
                    biggest = data["lucky"]["biggest"]
                    smallest = data["lucky"]["smallest"]
                    if data["lucky"]["same"]:
                        if 數字 > biggest or 數字 < smallest:
                            await ctx.send(f"數字必須在`{smallest}`與`{biggest}`之間")
                        else:
                            data["lucky"]["user"][數字] = ctx.author.id
                            data["lucky"]["num"].append(數字)
                            data["lucky"]["ok"].append(str(ctx.author.id))
                            requests.put(html1, params={"id": html2}, json=data)
                            await ctx.send(f"成功選取數字`{數字}`")
                    else:
                        if 數字 > biggest or 數字 < smallest:
                            await ctx.send(f"數字必須在`{smallest}`與`{biggest}`之間")
                        else:
                            if 數字 in data["lucky"]["num"]:
                                await ctx.send(f"數字`{數字}`已被人選取")
                            else:
                                data["lucky"]["user"][數字] = ctx.author.id
                                data["lucky"]["num"].append(數字)
                                data["lucky"]["ok"].append(str(ctx.author.id))
                                requests.put(html1, params={"id": html2}, json=data)
                                await ctx.send(f"成功選取數字`{數字}`")
                else:
                    await ctx.send("你已經選取過幸運數字了")
            else:
                await ctx.send("抽獎活動尚未開始或已經結束")
        else:
            await ctx.send("現在不可以選擇幸運數字")

    @cog_ext.cog_slash(name="結束抽獎活動", description="/結束抽獎活動")
    async def _結束抽獎活動(self, ctx:SlashContext):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            if data["lucky"]["start"]:
                data["lucky"]["start"] = False
                requests.put(html1, params={"id": html2}, json=data)
                await ctx.send("成功結束抽獎活動")
            else:
                await ctx.send("抽獎活動尚未開始或已經結束")
        else:
            await ctx.send("你不是管理員")

    @cog_ext.cog_slash(name="開始選擇幸運數字", description="/開始選擇幸運數字")
    async def _開始選擇幸運數字(self, ctx:SlashContext):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            if data["lucky"]["start"]:
                data["lucky"]["get"] = True
                requests.put(html1, params={"id": html2}, json=data)
                await ctx.send("現在可以開始選擇幸運數字")
            else:
                await ctx.send("抽獎活動尚未開始或已經結束")
        else:
            await ctx.send("你不是管理員")

    @cog_ext.cog_slash(name="結束選擇幸運數字", description="/結束選擇幸運數字")
    async def _結束選擇幸運數字(self, ctx:SlashContext):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            if data["lucky"]["start"]:
                data["lucky"]["get"] = False
                requests.put(html1, params={"id": html2}, json=data)
                await ctx.send("現在開始不可以選擇幸運數字")
            else:
                await ctx.send("抽獎活動尚未開始或已經結束")
        else:
            await ctx.send("你不是管理員")

    @cog_ext.cog_slash(name="抽獎", description="抽獎")
    async def _抽獎(self, ctx:SlashContext, 獎品: str):
        data = requests.get(html).json()
        if ctx.author.id in Admin:
            if data["lucky"]["start"]:
                if data["lucky"]["get"]:
                    await ctx.send("為避免錯誤，請先結束選擇幸運數字(/結束選擇幸運數字)")
                else:
                    n = data["lucky"]["n"]
                    n = n + 1
                    biggest = data["lucky"]["biggest"]
                    smallest = data["lucky"]["smallest"]
                    list = data["lucky"]["num"]
                    dict = data["lucky"]["user"]
                    if data["lucky"]["dowle"]:
                        if data["lucky"]["select"]:
                            ans_num = str(random.choice(list))
                            ans = dict[ans_num]
                            await ctx.send(f"#{n} 數字：{ans_num}，恭喜<@{ans}>獲得{獎品}！")
                            data["lucky"]["n"] = n
                            data["lucky"]["output"] = data["lucky"]["output"] + f"#{n} 數字：{ans_num}，<@{ans}> => {獎品}！\n"
                            requests.put(html1, params={"id": html2}, json=data)
                        else:
                            ans_num = str(random.randint(smallest, biggest))
                            try:
                                ans = dict[ans_num]
                                await ctx.send(f"#{n} 數字：{ans_num}，恭喜<@{ans}>獲得{獎品}！")
                                data["lucky"]["n"] = n
                                data["lucky"]["output"] = data["lucky"][
                                                              "output"] + f"#{n} 數字：{ans_num}，<@{ans}> => {獎品}！\n"
                                requests.put(html1, params={"id": html2}, json=data)
                            except:
                                await ctx.send(f"數字：{ans_num}，沒有人選擇這個數字。")
                    else:
                        if data["lucky"]["select"]:
                            ans_num = str(random.choice(list))
                            ans = dict[ans_num]
                            data["lucky"]["num"].remove(int(ans_num))
                            requests.put(html1, params={"id": html2}, json=data)
                            await ctx.send(f"#{n} 數字：{ans_num}，恭喜<@{ans}>獲得{獎品}！")
                            data["lucky"]["n"] = n
                            data["lucky"]["output"] = data["lucky"]["output"] + f"#{n} 數字：{ans_num}，<@{ans}> => {獎品}！\n"
                            requests.put(html1, params={"id": html2}, json=data)
                        else:
                            ans_num = str(random.randint(smallest, biggest))
                            try:
                                ans = dict[ans_num]
                                await ctx.send(f"#{n} 數字：{ans_num}，恭喜<@{ans}>獲得{獎品}！")
                                data["lucky"]["n"] = n
                                data["lucky"]["output"] = data["lucky"][
                                                              "output"] + f"#{n} 數字：{ans_num}，<@{ans}> => {獎品}！\n"
                                requests.put(html1, params={"id": html2}, json=data)
                            except:
                                await ctx.send(f"數字：{ans_num}，沒有人選擇這個數字。")
            else:
                await ctx.send("抽獎活動尚未開始或已經結束")
        else:
            await ctx.send("你不是管理員")

    @cog_ext.cog_slash(name="公共傳點", description="/公共傳點")
    async def _公共傳點(self, ctx:SlashContext):
        await ctx.send("\/to !ARTC!")

    @cog_ext.cog_slash(name="output", description="output")
    async def output(self, ctx:SlashContext):
        if ctx.author.id in Admin:
            data = requests.get(html).json()
            await ctx.send(data["lucky"]["output"])
        else:
            await ctx.send("你不是管理員")



def setup(client):
    client.add_cog(point(client))
