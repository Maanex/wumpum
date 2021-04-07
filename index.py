import bot
import promserver
import threading
import schedule
import time

def main():
    discord_thread = threading.Thread(target=bot.run)
    discord_thread.start()
    promserver_thread = threading.Thread(target=promserver.run)
    promserver_thread.start()
    
    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
