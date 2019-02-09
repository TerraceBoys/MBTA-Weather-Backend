import datetime
import dateutil

def panel_train(times, station='Lechmere'):
    time_1 = ""
    time_2 = ""
    color_1 = ""
    color_2 = ""

    times.sort()
    times = filter(lambda x: x > 240, times)
    if times:
        m1, s1 = secs_to_mins(times[0])
        time_1, color_1 = time_handler(m1, s1, 4, 6, True)
        if times.__len__() > 1:
            m2, s2 = secs_to_mins(times[1])
            time_2, color_2 = time_handler(m2, s2, 4, 6, True)
            
    return time_1, color_1, time_2, color_2

def panel_bus(times, station='Lechmere'):
    time_1 = ""
    time_2 = ""
    color_1 = ""
    color_2 = ""

    times.sort()
    times = filter(lambda x: x > 240, times)
    if times:
	m1, s1 = secs_to_mins(times[0])
        time_1, color_1 = time_handler(m1, s1, 3, 5, True)
        if len(times) > 1:
            m2, s2 = secs_to_mins(times[1])
            time_2, color_2 = time_handler(m2, s2, 3, 5, True)

    return time_1, color_1, time_2, color_2

# Convert seconds into minutes and seconds
def secs_to_mins(seconds):
    m, s = divmod(seconds, 60)
    return m, s


# Format the arrival times
def time_handler(m, s, red=4, yellow=6, panel=False):
    if panel:
        if m <= red:
            return "%02d : %02d" % (m, s), "red"
        elif m <= yellow:
            return "%02d : %02d" % (m, s), "orange"
        else:
            return "%02d : %02d" % (m, s), "green"
    else:
        if m < 1:
            return "%02d : %02d [BRD]" % (m, s)
        elif m == 1:
            return "%02d : %02d [ARR]" % (m, s)
        else:
            return "%02d : %02d" % (m, s)
