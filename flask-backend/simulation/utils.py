import math

import sys
FLOAT_MAX = sys.float_info.max


def secToTimeStr(race_time :float) -> str:
    if race_time == FLOAT_MAX:
        return "No Time"
    elif race_time < FLOAT_MAX and race_time > FLOAT_MAX / 2:
        return "---"
    temp_time = round(race_time, 3)
    hours = 0
    minutes = 0
    seconds = 0
    milliseconds = 0
    time_str = ""

    if temp_time > 3600:
        hours = int(temp_time // 3600)
        temp_time = temp_time - (hours * 3600)
    
    if temp_time > 60:
        minutes = int(temp_time // 60)
        temp_time = temp_time - (minutes * 60)

    if temp_time > 0:
        seconds = int(math.floor(temp_time))
        temp_time = temp_time - seconds

    if temp_time > 0:
        milliseconds = int(temp_time * 1000)

    if hours > 0:
        time_str = "{hours}:{minutes:02}:{seconds:02}.{milliseconds:03}".format(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)
    elif minutes > 0:
        time_str = "{minutes}:{seconds:02}.{milliseconds:03}".format(minutes=minutes, seconds=seconds, milliseconds=milliseconds)
    elif seconds >= 0:
        time_str = "{seconds}.{milliseconds:03}".format(seconds=seconds, milliseconds=milliseconds)


    return time_str