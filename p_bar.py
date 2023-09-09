import time
import math
import os
from Easy_F import hrb,hrt
from pyrogram.errors import FloodWait
from Easy_F import hrb, hrt
import logging
import threading
logging.basicConfig(filename='progress_log.txt', level=logging.INFO)





class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between
        self.lock = threading.Lock()  # Create a lock for thread safety

    def can_send(self):
        with self.lock:
            if time.time() > (self.start_time + self.time_between):
                self.start_time = time.time()
                return True
            return False

timer = Timer()

def update_progress(current, total, reply, start, retries=3):
    for _ in range(retries):
        if timer.can_send():
            now = time.time()
            diff = now - start
            if diff < 1:
                return
            else:
                perc = f"{current * 100 / total:.1f}%"
                elapsed_time = round(diff)
                speed = current / elapsed_time
                sp = str(hrb(speed)) + "ps"
                tot = hrb(total)
                cur = hrb(current)
                remaining = total - current
                eta_seconds = round(remaining / speed)
                eta = hrt(eta_seconds)
                try:
                    message = f'┌ <b>Progress</b> 📈 -【 {perc} 】\n├ <b>Speed</b> 🧲 -【 {sp} 】\n├ <b>Size</b> 📂 -【 {cur} / {tot} 】\n└ <b>ETA</b> ⏳ -【 {eta} 】'
                    reply.edit(message)
                    # Log progress
                    logging.info(f'Progress: {perc}, Speed: {sp}, Size: {cur}/{tot}, ETA: {eta}')
                    break  # Break the loop if update is successful
                except FloodWait as e:
                    time.sleep(e.x)
