from prometheus_client import start_http_server, Counter, Gauge
import config

track_individual_users = config.settings['track_individual_users']

PROM_MESSAGE_COUNT = Counter('wumpum_message_count', 'The total amount of messages seen', ['userid', 'bot'] if track_individual_users else [])
PROM_ONLINE_COUNT = Gauge('wumpum_online_count', 'Users that are not offline. Includes afk and dnd.', ['guildid'] if track_individual_users else [])
PROM_PRESENCE_GAUGE = Gauge('wumpum_user_presence', 'Users online or offline.', ['userid'] if track_individual_users else [])
PROM_VOICE_GAUGE = Gauge('wumpum_user_voice_connections', 'Users in voice channels', ['userid'] if track_individual_users else [])

def run():
    start_http_server(config.server['port'])
    print('Server started with port {0}'.format(config.server['port']))
