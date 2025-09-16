''' This module includes functions used for calculations including time '''


# IMPORT MODULES

import time
import logging
from datetime import datetime as dt
from flask import request



# TIME RELATED FUNCTIONS

def current_time_hhmm():
    """ Returns local time in the HH:MM format
    :returns: current time
    """

    local_time = time.localtime()
    current_time = time.strftime("%H:%M", local_time)
    return current_time


def minutes_to_seconds(minutes):
    """ Converts minutes to seconds
    :param minutes: returns seconds
    """

    return int(minutes)*60


def hours_to_minutes(hours):
    """ Converts hours to minutes
    :param hours: returns minutes
    """

    return int(hours)*60


def hhmm_to_seconds(hhmm):
    """ Converts time in the HH:MM format to seconds
    :param hhmm: returns seconds
    """

    if len(hhmm.split(':')) != 2:
        print('Incorrect format. Argument must be formatted as HH:MM')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmm.split(':')[0])) + \
        minutes_to_seconds(hhmm.split(':')[1])


def hhmmss_to_seconds(hhmmss):
    """ Converts hh:mm:ss format into seconds
    :param hhmmss: returns seconds
    """

    if len(hhmmss.split(':')) != 3:
        logging.warning('Incorrect format. Argument must be formatted as HH:MM:SS')
        return None
    return minutes_to_seconds(hours_to_minutes(hhmmss.split(':')[0])) + \
        minutes_to_seconds(hhmmss.split(':')[1]) + int(hhmmss.split(':')[2])


def get_time_for_schedules():
    """ Get update time
    :returns time_till_update: update time in seconds
    """
    # gets update time
    time_of_update = request.args.get('update')
    # gets current time
    current_time = dt.now().strftime("%H:%M:%S")
    time_of_update = hhmm_to_seconds(time_of_update)
    current_time = hhmmss_to_seconds(current_time)
    # if update is in the future
    if time_of_update > current_time:
        time_till_update = time_of_update - current_time
    else:  # update time is in the 'past' (so is scheduled for tomorrow)
        time_till_update = (86400 - current_time) + time_of_update
    return time_till_update

