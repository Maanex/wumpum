import os


settings = {
    'track_individual_users': os.environ['WUMPUM_TRACK_INDIVIDUAL'] == 'true'
}

bot = {
    'token': os.environ['WUMPUM_DBOT_TOKEN']
}

server = {
    'port': 80
}