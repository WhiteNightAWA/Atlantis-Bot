from cogs.core import core
from discord.ext import commands
import discord
import random


class member_join(core):

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id != 856155057561272331:
            return
        channel = self.client.get_channel(858534917784076299)
        await channel.send(embed=discord.Embed(description=f"歡迎`<{member}`來到了殘破不堪的小卯村<:awa3:866963596785221662> <:awa3:866963596785221662> <:awa3:866963596785221662> <:awa3:866963596785221662> <:MuMao_1:865847027715014677>", color=random.randint(0, 0xffffff)))


def setup(client):
    client.add_cog(member_join(client))
