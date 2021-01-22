from save_to_db import save_pc_stat
from save_to_db import save_weather
from save_to_db import save_currency

import schedule
import time

def job():
    print("I'm working...")

def save_5_sec():
    save_pc_stat()

def save_24_hour():
    print('Here some scripts!..')
    save_weather()
    save_currency()


schedule.every(5).seconds.do(save_5_sec)
schedule.every().day.at('11:40').do(save_24_hour)

while 1:
    schedule.run_pending()
    time.sleep(1)

