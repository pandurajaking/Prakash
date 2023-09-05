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

            # Calculate ETA
            remaining = total - current
            eta_seconds = round(remaining / speed)
            eta = hrt(eta_seconds)

            try:
                await reply.edit(f'┌ <b>Progress</b> 📈 -【 {perc} 】\n'
                                f'├ <b>Speed</b> 🧲 -【 {sp} 】\n'
                                f'├ <b>Size</b> 📂 -【 {cur} / {tot} 】\n'
                                f'└ <b>ETA</b> ⏳ -【 {eta} 】')
            except FloodWait as e:
                time.sleep(e.x)
