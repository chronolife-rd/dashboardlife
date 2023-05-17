# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 17:29:37 2023

@author: aterman
"""
import numpy as np
from garmin_automatic_reports.config import DELTA_TIME

# ---------- Functions for computing durations of wearing the device ----------

def find_time_intervals(times_series):
    """
    This function separates the time intervals
    Exemple:
    input            [1,2,3,10,11,12,13,32,33,34,35]
    a                [1,2,3, 10,11,12,13,32,33,34]
    b                [2,3,10,11,12,13,32,33,34,35]
    time_differences [1,1,7, 1, 1, 1, 19, 1, 1, 1]
    indexes          [2, 6]
    output [[1,2,3], [10,11,12,13],[32,33,34,35]]

    """
    times_series = times_series.reset_index(drop=True)
    a = times_series[:-1]
    b = times_series[1:]
    b = b.reset_index(drop=True)

    # Compute time_differences 
    time_differences = b-a

    # Get the index where the time difference is bigger than acceptable delta
    indexes = np.where(time_differences > DELTA_TIME)[0]

    # Get the time intervals as a list of lists 
    intervals = []
    first_index = 0
    for index in indexes:
        interval = times_series[first_index:index+1]
        interval = interval.reset_index(drop=True)
        intervals.append(interval)
        first_index = index+1

    # Add the last interval
    interval = times_series[first_index:]
    interval = interval.reset_index(drop=True)
    intervals.append(interval)

    return intervals

def sum_time_intervals(time_intervals):

    total_time = 0
    
    for i in range(len(time_intervals)):
        if (len(time_intervals[i]) > 2):
            delta_time = time_intervals[i].tail(1).item() - time_intervals[i][0]
            delta_time = delta_time.seconds  
            total_time += delta_time
    
    return total_time

def sum_time_intervals_garmin(time_intervals):
    total_time = 0
    for i in range(len(time_intervals)):
        if (len(time_intervals[i]) > 2):
            delta_time = time_intervals[i].tail(1).item() - time_intervals[i][0]
            delta_time = delta_time.seconds  
            total_time += delta_time
    
    return timedelta_formatter(total_time)

def timedelta_formatter(time_delta, convert = False):    # defining the function
    if convert == True:                                  # if time_delta is a timedelta type
        time_delta = time_delta.seconds                  # getting the seconds field of the timedelta
    hour_count, rem = divmod(time_delta, 3600)           # calculating the total hours
    minute_count, second_count = divmod(rem, 60)         # distributing the remainders
    msg = "{}h, {}min".format(hour_count,minute_count)
    return msg 

def unwrap(values):
    """ Unwrap values from list

     Parameter
    ----------
    values:     Values to unwrap

    Returns
    ----------
    new_values: unwrapped values

    """
    if not is_list_of_list(values):
        return values

    new_values = []
    for value in values:     
        if value is not None and type(value)==float:            
            new_values.append(value)
        else:
             if value is not None:
                 new_values.extend(value) 

    return np.array(new_values)

def is_list_of_list(values):
    """ Define if input signal is a matrix """
    is_list_list = False

    if isinstance(values, int) or  isinstance(0, float):
        return is_list_list

    if len(values) > 0:
        sig = np.array(values)
        for i in range(len(sig)):
            if type(sig[i]) is np.ndarray or type(sig[i]) is list:
                is_list_list = True
                break

    return is_list_list