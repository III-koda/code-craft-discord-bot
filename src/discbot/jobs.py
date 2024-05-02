from datetime import datetime
from datetime import timedelta

from cron_converter import Cron
from discord.ext import tasks

from src.discbot.controllers.joke_controller import channels_joke_schedule
from src.discbot.controllers.joke_controller import joke_generator


@tasks.loop(minutes=1)
async def scheduled_joke(bot) -> None:
    now = datetime.now()
    a_min_ago = now - timedelta(minutes=1)

    for channel_id, cron_expression in channels_joke_schedule.items():
        if now.strftime("%m/%d/%Y, %H:%M") == Cron(cron_expression).schedule(
            start_date=a_min_ago
        ).next().strftime("%m/%d/%Y, %H:%M"):
            channel = bot.get_channel(channel_id)
            await channel.send(f"**{joke_generator()}**")
