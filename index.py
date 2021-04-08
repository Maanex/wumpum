import bot
import promserver
import threading
import time

def main():
    discord_thread = threading.Thread(target=bot.run)
    discord_thread.start()
    promserver_thread = threading.Thread(target=promserver.run)
    promserver_thread.start()


if __name__ == '__main__':
    main()
