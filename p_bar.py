import time
import math
import os
from Easy_F import hrb,hrt
from pyrogram.errors import FloodWait
from Easy_F import hrb, hrt
import asyncio


class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

timer = Timer()
async def progress_bar(current, total, reply, start):
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
                await reply.edit(f'┌ <b>Progress</b> 📈 -【 {perc} 】\n├ <b>Speed</b> 🧲 -【 {sp} 】\n├ <b>Size</b> 📂 -【 {cur} / {tot} 】\n└ <b>ETA</b> ⏳ -【 {eta} 】')
                await asyncio.sleep(1)  # Add a short sleep to keep the connection active
            except FloodWait as e:
                print(f"Caught FloodWait exception: {e}")
                await asyncio.sleep(e.x)  # Retry after waiting
