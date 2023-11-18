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

    ms_fmt = zero_pad(ms, 3) + "ms"

    if dd > 0:
        return f"{str(dd)}d:{zero_pad(hh)}h:{zero_pad(mm)}m:{zero_pad(ss)}s.{ms_fmt}"
    elif hh > 0:
        return f"{str(hh)}h:{zero_pad(mm)}m:{zero_pad(ss)}s.{ms_fmt}"
    elif mm > 0:
        return f"{str(mm)}m:{zero_pad(ss)}s.{ms_fmt}"
    else:
        return f"{str(ss)}s.{ms_fmt}"

def zero_pad(num, len_goal = 2):
    num = str(num)
    if len(num) == len_goal:
        return num
    else:
        return "0" * (len_goal - len(num)) + num

def pretty(num):
    return format(num, ",")

def format_date(date):
    return date.strftime("%m/%d/%Y")

def get_amount(total, target):
    if target == -1:
        return total
    else:
        return min(total, target)
