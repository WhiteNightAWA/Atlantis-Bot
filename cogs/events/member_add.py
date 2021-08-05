from cogs.core import core
from discord.ext import commands
import discord
import random


class member_add(core):

    @commands.Cog.listener()
    async def on_member_add(self, member):
        channel = self.client.get_channel(872704498244661269)
        await channel.send(embed=discord.Embed(description=f"歡迎<@!{member.id}>來到了殘破不堪的小卯村:awa3: :awa3: :awa3: :awa3: :MuMao_1:", color=random.randint(0, 0xffffff)))


def setup(client):
    client.add_cog(member_add(client))
