from datetime import datetime, timedelta
import time

MAX_RETRIES = 5

def hrb_with_retry(value, digits=2, delim="", postfix=""):
    for _ in range(MAX_RETRIES):
        try:
            result = hrb(value, digits, delim, postfix)
            return result  # If successful, return the result
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)  # Wait for a short time before retrying
    else:
        raise Exception("Max retries reached. Unable to calculate hrb.")

def hrt_with_retry(seconds, precision=0):
    for _ in range(MAX_RETRIES):
        try:
            result = hrt(seconds, precision)
            return result  # If successful, return the result
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)  # Wait for a short time before retrying
    else:
        raise Exception("Max retries reached. Unable to calculate hrt.")

# Your original hrb and hrt functions (unchanged)
def hrb(value, digits=2, delim="", postfix=""):
    if value is None:
        return None
    chosen_unit = "B"
    for unit in ("KiB", "MiB", "GiB", "TiB"):
        if value > 1000:
            value /= 1024
            chosen_unit = unit
        else:
            break
    return f"{value:.{digits}f}" + delim + chosen_unit + postfix

def hrt(seconds, precision=0):
    pieces = []
    value = timedelta(seconds=seconds)

    if value.days:
        pieces.append(f"{value.days}d")

    seconds = value.seconds

    if seconds >= 3600:
        hours = int(seconds / 3600)
        pieces.append(f"{hours}h")
        seconds -= hours * 3600

    if seconds >= 60:
        minutes = int(seconds / 60)
        pieces.append(f"{minutes}m")
        seconds -= minutes * 60

    if seconds > 0 or not pieces:
        pieces.append(f"{seconds}s")

    if not precision:
        return "".join(pieces)

    return "".join(pieces[:precision])


