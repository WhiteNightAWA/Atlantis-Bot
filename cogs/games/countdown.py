from cogs.core import core
from discord.ext import commands
from discord_slash.utils.manage_components import create_button, create_actionrow, ComponentContext, wait_for_component
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext
import ast
import discord, random, requests

html = "https://jsonstorage.net/api/items/203f7ffb-fbba-491d-b4c0-2f9b87468a17"
html1 = "https://jsonstorage.net/api/items/"
html2 = "203f7ffb-fbba-491d-b4c0-2f9b87468a17"

class count_down(core):
	pass

def setup(client):
  client.add_cog(count_down(client))
