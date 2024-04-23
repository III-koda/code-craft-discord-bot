import logging

import discord
from discord.ext import commands

from src.config import DISCORD_BOT_TOKEN
from src.discbot.controllers.joke_controller import joke_generator
from src.discbot.controllers.run_code_controller import check_input
from src.discbot.controllers.run_code_controller import execute_code


_LOGGER = logging.getLogger(__name__)

intents = discord.Intents.default()
bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    _LOGGER.info("Bot is ready")


@bot.command()
async def run_code(ctx, language, *, code):
    check_input_result = check_input(language, code)
    if check_input_result != "":
        await ctx.send(check_input_result)
        return
    language = language.strip("```")
    code = code.strip("```")
    _LOGGER.error(language)
    _LOGGER.error(code)

    result = execute_code(language, code)
    if result is None:
        msg_str = "Something went wrong!"
    else:
        msg_str = result.to_discord_chat_response()
    await ctx.send(msg_str)


@bot.command()
async def joke(ctx):
    await ctx.send(joke_generator())


bot.run(DISCORD_BOT_TOKEN)
