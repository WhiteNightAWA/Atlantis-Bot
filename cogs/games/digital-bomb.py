from cogs.core import core
from discord.ext import commands
from dotenv import load_dotenv
import os
import requests
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")


class digital_bomb(core):

    @commands.Cog.listener()
    async def on_message(self, message):
        channel = self.client.get_channel(872783579564879922)
        if message.channel.id == channel.id:
            msgs = await message.channel.history(limit=3).flatten()
            if msgs[0].author.id == msgs[2].author.id:
                await message.delete()
            else:
                if message.content in range(1, 9):
                    data = requests.get(html).json()
                    await channel.send(f"現在的數字是：{data['num']}")
                else:
                    await message.delete()


def setup(client):
    client.add_cog(digital_bomb(client))
