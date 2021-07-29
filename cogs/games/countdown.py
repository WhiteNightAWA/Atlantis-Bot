from cogs.core import core
from discord.ext import commands
from discord_slash.utils.manage_components import create_button, create_actionrow, ComponentContext, wait_for_component
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext
import ast, os
import discord, random, requests
from dotenv import load_dotenv
load_dotenv()
html = os.getenv("html")
html1 = os.getenv("html1")
html2 = os.getenv("html2")

class count_down(core):
	pass

def setup(client):
  client.add_cog(count_down(client))
