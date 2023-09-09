import math
import os
import time
from Easy_F import hrb, hrt
from pyrogram.errors import FloodWait
from pyrogram.types import Message

class Timer:
    def __init__(self, time_between=5):
        self.start_time = time.time()
        self.time_between = time_between

    def can_send(self):
        if time.time() > (self.start_time + self.time_between):
            self.start_time = time.time()
            return True
        return False

async def progress_bar(current, total, reply: Message, start):
    timer = Timer()
    retry_count = 0
    max_retries = 5  # Maximum number of retries

    while retry_count <= max_retries:
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
                    await reply.edit_text(
                        f'┌ <b>Progress</b> 📈 -【 {perc} 】\n├ <b>Speed</b> 🧲 -【 {sp} 】\n├ <b>Size</b> 📂 -【 {cur} / {tot} 】\n└ <b>ETA</b> ⏳ -【 {eta} 】'
                    )
                    return  # Exit the loop if editing is successful

                except FloodWait as e:
                    time.sleep(e.x)
                    retry_count += 1

    # If we reach here, it means we exceeded the maximum number of retries
    print("Maximum retry count reached. Exiting.")

# Example usage:
# current = 100
# total = 1000
# reply_message = await some_function_to_send_message()
# start_time = time.time()
# await progress_bar(current, total, reply_message, start_time)
