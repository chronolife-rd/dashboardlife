# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 17:29:37 2023

@author: aterman
"""
import numpy as np
import pandas as pd
import copy 
from datetime import datetime
from automatic_reports.config import DELTA_TIME

# ---------- Function to combine cst and garmin data -------------------------
def  combine_data(cst_data, garmin_data):
    
    cardio_dict = {
        "rate" : "",
        "rate_var" : "",
        }
    breath_dict = {
        "rate" : "",
        }
    activity_dict = {
        "steps" : "",
        "distance" : "",
        "goal" : "",
        }
    
    common_data = {  
        "cardio" : cardio_dict,
        "breath" : breath_dict,
        "activity" : activity_dict,
        }
    
    # --- Cardio ---
    # Rate 
    garmin_df = garmin_data["cardio"]["rate"]
    cst_df = cst_data["cardio"]["rate"]

    if len(garmin_df)>0 and len(cst_df)>0:
        common_data["cardio"]["rate"] = merge_cst_and_garmin_data(cst_df[["times", "values"]], garmin_df)
    elif len(garmin_df) == 0 and  len(cst_df)>0:
        common_data["cardio"]["rate"] = cst_df[["times", "values"]]
    elif len(garmin_df) > 0 and  len(cst_df) == 0:
        common_data["cardio"]["rate"] = garmin_df

    # Rate variability
    cst_df = cst_data["cardio"]["rate_var"]
    common_data["cardio"]["rate_var"] = cst_df
    
    # --- Breath ---
    # Rate 
    garmin_df = garmin_data["breath"]["rate"]
    cst_df    = cst_data["breath"]["rate"]
    
    if len(garmin_df)>0 and len(cst_df)>0:
        common_data["breath"]["rate"] = merge_cst_and_garmin_data(cst_df[["times", "values"]], garmin_df)
    elif len(garmin_df) == 0 and  len(cst_df)>0:
        common_data["breath"]["rate"] = cst_df[["times", "values"]]
    elif len(garmin_df) > 0 and  len(cst_df) == 0:
        common_data["breath"]["rate"] = garmin_df

    # Rate variability
    cst_df = cst_data["breath"]["rate_var"]
    common_data["breath"]["rate_var"] = cst_df

    # Ratio inspi/expi
    cst_df = cst_data["breath"]["inspi_expi"]
    common_data["breath"]["inspi_expi"] = cst_df
    
    # --- Activity ---
    # Steps 
    cst_df    = cst_data["activity"]["steps"]
    garmin_df = garmin_data["activity"]["intensity"]
    
    if len(garmin_df)>0 and len(cst_df)>0:
        garmin_df = garmin_df[["times", "steps"]]
        garmin_df = garmin_df.rename(columns={"steps": "values"})
        
        common_data["activity"]["steps"] = merge_cst_and_garmin_data(garmin_df, cst_df)
    
    elif len(garmin_df) == 0 and  len(cst_df)>0:
        common_data["activity"]["steps"] = cst_df

    elif len(garmin_df) > 0 and  len(cst_df) == 0:
        garmin_df = garmin_df[["times", "steps"]]
        garmin_df = garmin_df.rename(columns={"steps": "values"})
        common_data["activity"]["steps"] = garmin_df

    # Distance 
    cst_df    = cst_data["activity"]["distance"]
    garmin_df = garmin_data["activity"]["intensity"]
    
    if len(garmin_df)>0 and len(cst_df)>0:
        garmin_df = garmin_df[["times", "distance"]]
        garmin_df.rename(columns = {'distance':'values'}, inplace = True)

        common_data["activity"]["distance"] = merge_cst_and_garmin_data(garmin_df, cst_df)
    
    elif len(garmin_df) == 0 and  len(cst_df)>0:
        common_data["activity"]["distance"] = cst_df

    elif len(garmin_df) > 0 and  len(cst_df) == 0:
        garmin_df = garmin_df[["times", "distance"]]
        garmin_df = garmin_df.rename(columns={"distance": "values"})
        common_data["activity"]["distance"] = garmin_df

    # Goal
    goal = garmin_data["activity"]["goal"] 
    if isinstance(goal, str) == False:
        common_data["activity"]["goal"] = goal
    else :
        common_data["activity"]["goal"] = 3000
    
    return copy.deepcopy(common_data)

def merge_cst_and_garmin_data(df_1, df_2): 
    format_time = '%Y-%m-%d %H:%M'
    df_1["times"] = df_1["times"].apply(lambda x: datetime.strftime(x, format_time))
    df_2["times"] = df_2["times"].apply(lambda x: datetime.strftime(x, format_time))
        
    #  Find outer data of df_2
    df_2_outer = pd.merge(df_1, df_2, how='outer', on='times', 
                indicator=True).query('_merge=="right_only"').drop(columns='_merge')
    
    # Rename columns    
    df_2_outer = df_2_outer[["times", "values_y"]]
    df_2_outer = df_2_outer.rename(columns={"values_y": "values"})
    # Add outer data of df_2 to df_1
    df_result = pd.concat([df_1, df_2_outer]) 
    df_result = df_result.drop_duplicates(subset=['times'])
    # Change type : str -> datetime
    df_result["times"] = df_result["times"].apply(lambda x: datetime.strptime(x, format_time))
    # Sort and reset
    df_result = df_result.sort_values("times")
    df_result = df_result.reset_index(drop= True)
    
    return df_result

# ---------- Functions for computing durations of wearing the device ---------
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
    minute_count, _ = divmod(rem, 60)         # distributing the remainders
    msg = "{}h, {}min".format(hour_count,minute_count)
    return msg 

def unwrap_ratio_inspi_expi(values):
    """ Unwrap values from list

     Parameter
    ----------
    values:     Values to unwrap

    Returns
    ----------
    new_values: unwrapped values

    # """

    new_values = []
    for value in values:     
        if value is not None and type(value)==float:            
            new_values.append(value)
        else:
             if value is not None:
                 new_values.extend(value) 

    return np.array(new_values)

def unwrap(values):
    """ Unwrap values from list

     Parameter
    ----------
    values:     Values to unwrap

    Returns
    ----------
    new_values: unwrapped values

    # """
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