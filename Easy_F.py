from datetime import datetime,timedelta

def hrb(value: int, digits: int = 2, delim: str = "", postfix: str = "") -> str:
    """Return a human-readable file size."""
    if value is None:
        return None

    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    chosen_unit = "B"
    for unit in units:
        if value < 1024:
            break
        value /= 1024
        chosen_unit = unit

    return f"{value:.{digits}f}{delim}{chosen_unit}{postfix}"

def hrt(seconds: int, precision: int = 0) -> str:
    """Return a human-readable time delta as a string."""
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
        return "".join(pieces)
    else:
        return "".join(pieces[:precision])
