from random import randint

from static_data.jokes import JOKES


channels_joke_schedule = {}


def joke_generator():
    idx = randint(0, len(JOKES) - 1)
    return "```" + JOKES[idx] + "```"


def add_joke_schedule(channel_id, cron_expression):
    channels_joke_schedule[channel_id] = cron_expression


def delete_joke_schedule(channel_id):
    del channels_joke_schedule[channel_id]


def does_channel_has_schedule(channel_id) -> bool:
    return channel_id in channels_joke_schedule
