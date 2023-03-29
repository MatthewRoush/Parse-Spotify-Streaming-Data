def get_last_used_path(path):
    try:
        with open(path, "r", encoding="UTF-8") as f:
            path = f.read()
        last_used_path = path.strip()
    except FileNotFoundError:
        last_used_path = None

    return last_used_path

def save_path(save_path, data_path):
    with open(save_path, "w", encoding="UTF-8") as f:
        f.write(data_path)

def ms_to_readable(ms):
    """Format time in milliseconds as dd:hh:mm:ss.ms time."""
    ss, ms = divmod(ms, 1000)
    mm, ss = divmod(ss, 60)
    hh, mm = divmod(mm, 60)
    dd, hh = divmod(hh, 24)

    return f"{dd}d:{hh}h:{mm}m:{ss}s:{ms}ms"

def pretty(num):
    return format(num, ",")
