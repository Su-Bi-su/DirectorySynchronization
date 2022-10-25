"""
This file is necessary to run the unit tests in test_sync_directories.py file
Do not delete this file.

Author : Sushma Bhandari

"""

import re
import datetime


# get the date and time from logfile at line number - linenum
# eg. first line, linenum = 1, for last line linenum = -1
def get_logfile_datetime(logfile="synclog.log", linenum=-1):
    global last_line
    with open(logfile, "r") as file:
        last_line = file.readlines()[linenum]
    pattern = "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
    t_format = "%Y-%m-%d %H:%M:%S"
    match = re.compile(pattern)
    date_time = match.search(last_line).group(1)
    return datetime.datetime.strptime(date_time, t_format)


# get the current date and time
def get_current_datetime():
    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    t_format = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.strptime(time_now, t_format)
