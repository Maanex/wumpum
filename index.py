import bot
import promserver
import threading
import time
import asyncio

def main():
    promserver_thread = threading.Thread(target=promserver.run)
    promserver_thread.start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.run())


if __name__ == '__main__':
    main()
