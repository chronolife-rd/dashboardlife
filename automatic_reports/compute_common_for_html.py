# -*- coding: utf-8 -*-
"""
Last updated on 01/06/2023

@author: aterman
"""
import copy
import numpy as np
import pandas as pd 
from collections import deque
from automatic_reports.config import ACTIVITY_THREASHOLD
from datetime import datetime

# ------------------------ The main function ---------------------------------
# ----------------------------------------------------------------------------
def get_common_indicators(cst_data:dict, garmin_data:dict) :
    # Compute the combination of Garmin and cst data 
    common_data = combine_data(cst_data, garmin_data)

    # Initialize the dictionary where the new data will be saved
    common_indicators = initialize_dictionary_with_template()

    # ========================== Cardio dict ===============================
    # ----------------------------- rate -------------------------------------
    
    if len(common_data["cardio"]["rate"]) >0:
    # Add rate high and max
        values_df = common_data["cardio"]["rate"]["values"].dropna()
        value = round(max(values_df))
        common_indicators["cardio"]["rate_high"] = value
        common_indicators["cardio"]["rate_max"] = value

        # Add rate min
        value = round(min(values_df))
        common_indicators["cardio"]["rate_min"] = value

        # Add rate mean
        value = round(np.mean(values_df))
        common_indicators["cardio"]["rate_mean"] = value
        
        # Add rate resting 
        mean_values = sliding_window(values_df, minutes = 30)
        value = round(min(mean_values))
        common_indicators["cardio"]["rate_resting"] = value

    # --------------------------- rate var -----------------------------------
    if len(common_data["cardio"]["rate_var"]) >0:
    # Add rate variability max and high
        values_df = common_data["cardio"]["rate_var"]["values"].dropna()
        value = round(max(values_df))
        common_indicators["cardio"]["rate_var_high"] = value
        common_indicators["cardio"]["rate_var_max"] = value

        # Add rate variability min
        value = round(min(values_df))
        common_indicators["cardio"]["rate_var_min"] = value

        # Add rate variability mean
        value = round(np.mean(values_df))
        common_indicators["cardio"]["rate_var_mean"] = value

        # Add rate variability resting
        df_aux = common_data['cardio']['rate_var']
        values = df_aux.loc[df_aux["activity_values"] <= ACTIVITY_THREASHOLD, 
                            "values"].dropna().reset_index(drop=True)
        value = round(np.mean(values))
        common_indicators["cardio"]["rate_var_resting"] = value

    # ========================== Breath dict =================================
    # ----------------------------- rate -------------------------------------
    if len(common_data["breath"]["rate"]) >0:
        # Add rate high and max
        values_df = common_data["breath"]["rate"]["values"].dropna()
        value = round(max(values_df))
        common_indicators["breath"]["rate_high"] = value
        common_indicators["breath"]["rate_max"] = value

        # Add rate min
        value = round(min(values_df))
        common_indicators["breath"]["rate_min"] = value

        # Add rate mean
        value = round(np.mean(values_df))
        common_indicators["breath"]["rate_mean"] = value

        # Add rate resting
        mean_values = sliding_window(values_df, minutes = 30)
        value = round(min(mean_values))
        common_indicators["breath"]["rate_resting"] = value

    # --------------------------- rate var -----------------------------------
    if len(common_data["breath"]["rate_var"]) >0:
        # Add rate variability high and max
        values_df = common_data["breath"]["rate_var"]["values"].dropna()
        common_indicators["breath"]["rate_var_max"] = round(max(values_df))
        common_indicators["breath"]["rate_var_high"] = round(max(values_df))

        # Add rate variability min
        common_indicators["breath"]["rate_var_min"] = round(min(values_df))

        # Add rate variability mean
        common_indicators["breath"]["rate_var_mean"] = round(np.mean(values_df))

        # Add rate variability resting
        df_aux = common_data['breath']['rate_var']
        values = df_aux.loc[df_aux["activity_values"] <= ACTIVITY_THREASHOLD, 
                            "values"].dropna().reset_index(drop=True)
        value = round(np.mean(values))
        common_indicators["breath"]["rate_var_resting"] = value

    # ------------------------- inspi expi -----------------------------------
    if len(common_data["breath"]["inspi_expi"]) >0:
        values_df = common_data["breath"]["inspi_expi"]["values"].dropna()

        # Add rate variability high and max
        common_indicators["breath"]["inspi_expi_max"] =  round(max(values_df))
        
        # Add rate variability min
        common_indicators["breath"]["inspi_expi_min"] = round(min(values_df))

        # Add rate variability mean
        common_indicators["breath"]["inspi_expi_mean"] = round(np.mean(values_df))

    # ========================== Activity dict ===============================
    # dictionary with data used to plot steps graph 
    steps_dict_for_plot = {
        "total_steps" : "",
        "goal" : ""
    }

    if len(common_data["activity"]["steps"]) >0:
        # Steps
        value = round(sum(common_data["activity"]["steps"]["values"].dropna()))
        common_indicators["activity"]["steps"] = value
        steps_dict_for_plot["total_steps"] = value

        # Goal        
        if garmin_data["activity"]["goal"] == "":
            value = 3000
        else :
            value = garmin_data["activity"]["goal"]

        common_indicators["activity"]["goal"] = value
        steps_dict_for_plot["goal"] = value

        # Distance
        value = round(sum(common_data["activity"]["distance"]["values"].dropna()))
        common_indicators["activity"]["distance"] = value

    return common_data, common_indicators, steps_dict_for_plot

# ----------------------- Internal functions ---------------------------------
# ----------------------------------------------------------------------------
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

    return copy.deepcopy(common_data)

def initialize_dictionary_with_template() -> dict :
    cardio_dict = {
        "rate_high"        : "",
        "rate_resting"     : "",
        "rate_min"         : "",
        "rate_max"         : "",
        "rate_mean"        : "",

        "rate_var_resting" : "",
        "rate_var_high"    : "",
        "rate_var_min"     : "",
        "rate_var_max"     : "",
        "rate_var_mean"    : "",
    } 
    breath_dict = {
        "rate_high"        : "",
        "rate_max"         : "",
        "rate_min"         : "",
        "rate_mean"        : "",
        "rate_resting"     : "",

        "rate_var_high"    : "",
        "rate_var_max"     : "",
        "rate_var_min"     : "",
        "rate_var_mean"    : "",
        "rate_var_resting" : "",
        
        "inspi_expi_max"  : "",
        "inspi_expi_min"  : "",
        "inspi_expi_mean" : "",
    } 
    activity_dict = {
        "steps"            : "",
        "distance"         : "",
        "goal"             : "",
    }
    dict_template = {
                    'cardio'   : copy.deepcopy(cardio_dict),
                    'breath'   : copy.deepcopy(breath_dict),
                    'activity' : copy.deepcopy(activity_dict)
                    }
    return copy.deepcopy(dict_template)

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
    
# Sliding window to compute the average rate on 30 min sliding window
# TO CHANGE !! adapt to time intervals (when the session is interrupted)
def sliding_window(sequence, minutes):
    """Calcule une moyenne sur des fenêtres glissantes.
    k est la taille de la fenêtre glissante
 
    >>> fenetre_glissante([40, 30, 50, 46, 39, 44], 3)
    [40.0, 42.0, 45.0, 43.0]
    """
    # on initialise avec les k premiers élements
    d = deque(sequence[:minutes])  
    avg = []

    nan_count = d.count('Nan')
    if(nan_count < 10):
        s = sum(d)
        avg.append(s / minutes)  # la moyenne sur la fenêtre
    
    # Calcul de la moyenne sur le fenetre glissante 
    for element in sequence[minutes:]:
        d.append(element)
        s += element - d.popleft()  # on enlève la 1re valeur, on ajoute la nouvelle
        
        nan_count = d.count('Nan')
        if(nan_count < 10):
            s = sum(d)
            avg.append(s / minutes)  # la moyenne sur la fenêtre
 
    return avg