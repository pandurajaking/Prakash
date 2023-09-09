from datetime import datetime, timedelta
import time

MAX_RETRIES = 5
RETRY_DELAY_SECONDS = 1  # Adjust this as needed

def hrb(value: int, digits: int = 2, delim: str = "", postfix: str = "") -> str:
    """Return a human-readable file size in MB or GB with retry mechanism."""
    for retry_count in range(MAX_RETRIES):
        result = _hrb(value, digits, delim, postfix)
        if result is not None:
            return result
        # If the function returns None, wait for a moment before retrying
        time.sleep(RETRY_DELAY_SECONDS)
    # If all retries fail, return an error message or raise an exception
    return "Failed to retrieve file size"

def _hrb(value: int, digits: int = 2, delim: str = "", postfix: str = "") -> str:
    if value is None:
        return None

    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    chosen_unit = "B"
    for unit in units:
        if value < 1024:
            break
        value /= 1024
        chosen_unit = unit

    if chosen_unit == "B":
        return f"{value:.{digits}f}{delim}B{postfix}"
    elif chosen_unit == "KiB":
        return f"{value:.{digits}f}{delim}KiB{postfix}"
    elif chosen_unit == "MiB":
        return f"{value:.{digits}f}{delim}MB{postfix}"
    elif chosen_unit == "GiB":
        return f"{value:.{digits}f}{delim}GB{postfix}"
    else:
        return f"{value:.{digits}f}{delim}{chosen_unit}{postfix}"

def hrt(seconds: int, precision: int = 0, show_seconds: bool = True) -> str:
    """Return a human-readable time in seconds or minutes with retry mechanism."""
    for retry_count in range(MAX_RETRIES):
        result = _hrt(seconds, precision, show_seconds)
        if result is not None:
            return result
        # If the function returns None, wait for a moment before retrying
        time.sleep(RETRY_DELAY_SECONDS)
    # If all retries fail, return an error message or raise an exception
    return "Failed to retrieve time"

def _hrt(seconds: int, precision: int = 0, show_seconds: bool = True) -> str:
    pieces = []

    if seconds < 1 and precision > 0:
        return "0s"

    intervals = [("d", 86400), ("h", 3600), ("m", 60), ("s", 1)]
    for unit, interval in intervals:
        if seconds >= interval or unit == "s" or not pieces:
            value = seconds // interval
            seconds %= interval
            pieces.append(f"{int(value)}{unit}")

    if precision == 0:
        if show_seconds:
            return "".join(pieces)
        else:
            return f"{int(pieces[0][:-1])*60 + int(pieces[1][:-1])}m"
    else:
        if show_seconds:
            return "".join(pieces[:precision])
        else:
            return f"{int(pieces[0][:-1])*60 + int(pieces[1][:-1])}m"

