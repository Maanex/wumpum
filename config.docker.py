import os


def readSecret(name):
    with open(name, 'r') as file:
        return file.read().replace('\n', '')


settings = {
    'track_individual_users': os.environ['WUMPUM_TRACK_INDIVIDUAL'] == 'true'
}

bot = {
    'token': readSecret('/run/secrets/WUMPUM_DBOT_TOKEN')
}

server = {
    'port': 80
}