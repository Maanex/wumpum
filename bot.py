from promserver import PROM_MESSAGE_COUNT, PROM_ONLINE_COUNT, PROM_PRESENCE_GAUGE, PROM_VOICE_GAUGE
import asyncio
import discord
import config
import threading
import schedule


intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Bot logged in as {0.user}'.format(client))
    # schedule.every().minute.do(update_trackers_sync)
    schedule.every(5).seconds.do(update_trackers_sync)

def update_trackers_sync():
    loop = asyncio.get_event_loop()
    loop.ensure_future(update_trackers)
    
@client.event
async def on_message(message):
    if config.settings['track_individual_users']:
      PROM_MESSAGE_COUNT.labels(message.author.id).inc()
    else:
      PROM_MESSAGE_COUNT.inc()

    if message.author.bot:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

async def update_trackers():
    presence_values = {
        'offline': 0,
        'invisible': 0,
        'idle': 1,
        'online': 2,
        'dnd': 3,
        'do_not_disturb': 3
    }

    for member in client.get_all_members():
        print(member, member.status, presence_values.get(str(member.status)))
        PROM_PRESENCE_GAUGE.labels(member.id).set(presence_values.get(str(member.status)))
        if member.voice is not None:
            if member.voice.mute or member.voice.self_mute:
                PROM_VOICE_GAUGE.labels(member.id).set(.5)
            else:
                PROM_VOICE_GAUGE.labels(member.id).set(1)
        else:
            PROM_VOICE_GAUGE.labels(member.id).set(0)

    for guild in client.guilds:
        count = 0
        async for member in guild.fetch_members(limit=None):
            if not str(member.status) == 'offline':
                count = count + 1
        PROM_ONLINE_COUNT.labels(guild.id).set(count)


def run():
    client.run(config.bot['token'])
