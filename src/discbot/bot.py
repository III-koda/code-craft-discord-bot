import logging

import discord
from discord.ext import commands

from src.discbot.controllers.api_controller import api_handler
from src.discbot.controllers.joke_controller import joke_generator
from src.discbot.controllers.run_code_controller import check_input
from src.discbot.controllers.run_code_controller import execute_code


_LOGGER = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord! Version {discord.__version__}")

    await bot.tree.sync()


@bot.command()
async def run_code(ctx, language, *, code):
    check_input_result = check_input(language, code)
    if check_input_result != "":
        await ctx.send(check_input_result)
        return
    language = language.strip("```")
    code = code.strip("```")

    result = execute_code(language, code)
    if result is None:
        msg_str = "Something went wrong!"
    else:
        msg_str = result.to_discord_chat_response()
    await ctx.send(msg_str)


@bot.hybrid_command(description="Randon dev joke")
async def joke(ctx):
    await ctx.send(joke_generator())


@bot.hybrid_command(description="execute an API to JSON format")
async def api(ctx, method, *, url):
    result = api_handler(method, url)

    if result is None:
        result = "Sumthing went wrong!"
    await ctx.send(result)
