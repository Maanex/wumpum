from promserver import PROM_MESSAGE_COUNT, PROM_ONLINE_COUNT, PROM_PRESENCE_GAUGE, PROM_VOICE_GAUGE
import discord
import config
import threading
import schedule


intents = discord.Intents.all()
client = discord.Client(intents=intents)


presence_values = {
    'offline': 0,
    'invisible': 0,
    'idle': 1,
    'online': 2,
    'dnd': 3,
    'do_not_disturb': 3
}


@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))
    await update_trackers()

@client.event
async def on_message(message):
    if config.settings['track_individual_users']:
      PROM_MESSAGE_COUNT.labels(message.author.id, str(message.author.bot)).inc()
    else:
      PROM_MESSAGE_COUNT.inc()

    if message.author.bot:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')


@client.event
async def on_member_update(before, after):
    PROM_PRESENCE_GAUGE.labels(after.id).set(presence_values.get(str(after.status)))
    await update_tracker_guilds()


@client.event
async def on_voice_state_update(member, before, after):
    if after is not None:
        if after.channel is None:
            PROM_VOICE_GAUGE.labels(member.id).set(0)
        elif after.mute or after.self_mute:
            PROM_VOICE_GAUGE.labels(member.id).set(.5)
        else:
            PROM_VOICE_GAUGE.labels(member.id).set(1)
    else:
        PROM_VOICE_GAUGE.labels(member.id).set(0)


async def update_trackers():
    for member in client.get_all_members():
        PROM_PRESENCE_GAUGE.labels(member.id).set(presence_values.get(str(member.status)))
        if member.voice is not None:
            if member.voice.channel is None:
                PROM_VOICE_GAUGE.labels(member.id).set(0)
            elif member.voice.mute or member.voice.self_mute:
                PROM_VOICE_GAUGE.labels(member.id).set(.5)
            else:
                PROM_VOICE_GAUGE.labels(member.id).set(1)
        else:
            PROM_VOICE_GAUGE.labels(member.id).set(0)

        await update_tracker_guilds()

async def update_tracker_guilds():
    for guild in client.guilds:
        count = 0
        async for member in guild.fetch_members(limit=None):
            if not str(member.status) == 'offline':
                count = count + 1
        PROM_ONLINE_COUNT.labels(guild.id).set(count)


def run():
    client.run(config.bot['token'])
