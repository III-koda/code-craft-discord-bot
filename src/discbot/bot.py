from datetime import datetime
from datetime import timedelta

import discord
from cron_converter import Cron
from cron_descriptor import get_description
from discord.ext import commands

import src.discbot.controllers.joke_controller as joke_ctl
from src.discbot.controllers.api_controller import api_handler
from src.discbot.controllers.run_code_controller import check_input
from src.discbot.controllers.run_code_controller import execute_code
from src.discbot.jobs import scheduled_joke

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=".", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord! Version {discord.__version__}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(e)

    scheduled_joke.start(bot)
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
    await ctx.send(joke_ctl.joke_generator())


@bot.hybrid_command(description="execute an API to JSON format")
async def api(ctx, method, *, url):
    result = api_handler(method, url)

    if result is None:
        result = "Sumthing went wrong!"
    await ctx.send(result)


@bot.hybrid_command(description="set automatic joke in cron format")
async def schedule_joke(ctx, period):
    channel_id = ctx.channel.id

    print(get_description(period))

    if joke_ctl.does_channel_has_schedule(channel_id):
        await ctx.send("Your channel already has a joke schedule set up")
        return
    joke_ctl.add_joke_schedule(channel_id, period)
    await ctx.send(f"Okay! All set")


@bot.hybrid_command(description="Remove joke schedule")
async def delete_joke_schedule(ctx):
    channel_id = ctx.channel.id
    if channel_id not in joke_ctl.channels_joke_schedule:
        await ctx.send(f"Your channel does not have any joke schedule set up")
        return
    joke_ctl.delete_joke_schedule(channel_id)
    await ctx.send(f"Joke's on you!")


@bot.hybrid_command(description="Explain cron format * * * * *")
async def cron_format(ctx, *, cron_expression):
    try:
        description = get_description(cron_expression)
    except:
        description = (
            f'Cron format is: "* * * * *"\n'
            + "Each star mean: Min(0-59) Hour(0-23) Day(1-31)  Mon(1-12)  Weekday(0=Sun ... 6=Sat)"
        )

    now = datetime.now()
    a_min_ago = now - timedelta(minutes=1)
    await ctx.send(
        "```"
        + description
        + "\n"
        + "Next at: "
        + Cron(cron_expression)
        .schedule(start_date=a_min_ago)
        .next()
        .strftime("%m/%d/%Y, %H:%M")
        + "```"
    )
