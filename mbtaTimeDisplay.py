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
        time_1, color_1 = time_handler(m1, s1, True)
        if times.__len__() > 1:
            m2, s2 = secs_to_mins(times[1])
            time_2, color_2 = time_handler(m2, s2, True)
            
    return time_1, color_1, time_2, color_2

# Convert seconds into minutes and seconds
def secs_to_mins(seconds):
    m, s = divmod(seconds, 60)
    return m, s


# Format the arrival times
def time_handler(m, s, panel=False):
    if panel:
        if m <= 5:
            return "%02d : %02d" % (m, s), "red"
        elif m <= 7:
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
