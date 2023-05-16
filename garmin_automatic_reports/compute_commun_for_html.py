# -*- coding: utf-8 -*-
"""
Last updated on 05/05/2023

@author: aterman
"""
import copy
import numpy as np
import pandas as pd 
from collections import deque
from garmin_automatic_reports.config import ACTIVITY_THREASHOLD
from datetime import datetime

# ------------------------ The main function ---------------------------------
# ----------------------------------------------------------------------------
def get_commun_indicators(cst_data:dict, garmin_data:dict) :
    # Compute the combination of Garmin and cst data 
    commun_data = combine_data(cst_data, garmin_data)

    # Initialize the dictionary where the new data will be saved
    commun_indicators = initialize_dictionary_with_template()

    # ========================== Cardio dict ===============================
    # Add rate high
    value = round(max(commun_data["cardio"]["rate"]["values"].dropna()))
    commun_indicators["cardio"]["rate_high"] = value
    
    # Add rate resting 
    df_values = commun_data['cardio']['rate']["values"].dropna()
    mean_values = sliding_window(df_values, minutes = 30)
    value = round(min(mean_values))
    commun_indicators["cardio"]["rate_resting"] = value

    # Add rate variability
    df_aux = commun_data['cardio']['rate_var']
    values = df_aux.loc[df_aux["activity_values"] <= ACTIVITY_THREASHOLD, 
                        "values"].dropna().reset_index(drop=True)
    value = round(np.mean(values))
    commun_indicators["cardio"]["rate_var_resting"] = value

    # ========================== Breath dict =================================
    # Add rate high
    value = round(max(commun_data["breath"]["rate"]["values"].dropna()))
    commun_indicators["breath"]["rate_high"] = value

    # Add rate resting
    values_df = commun_data['breath']['rate']['values'].dropna()
    mean_values = sliding_window(values_df, minutes = 30)
    value = round(min(mean_values))
    commun_indicators["breath"]["rate_resting"] = value

    # Add rate variability
    df_aux = commun_data['breath']['rate_var']
    values = df_aux.loc[df_aux["activity_values"] <= ACTIVITY_THREASHOLD, 
                        "values"].dropna().reset_index(drop=True)
    value = round(np.mean(values))
    commun_indicators["breath"]["rate_var_resting"] = value

    # Add inhale/exhale ratio TO CHANGE !!!!!
    value = 500
    commun_indicators["breath"]["ratio_in_exhale"] = value

    # ========================== Activity dict ===============================
    # dictionary with data used to plot steps graph 
    steps_dict_for_plot = {
        "total_steps" : None,
        "goal" : None
    }
    # Steps
    value = round(sum(commun_data["activity"]["steps"]["values"].dropna()))
    commun_indicators["activity"]["steps"] = value
    steps_dict_for_plot["total_steps"] = value

    # Goal
    value = garmin_data["activity"]["goal"]
    commun_indicators["activity"]["goal"] = value
    steps_dict_for_plot["goal"] = value

    # Distance
    value = round(sum(commun_data["activity"]["distance"]["values"].dropna()))
    commun_indicators["activity"]["distance"] = value

    return commun_data, commun_indicators, steps_dict_for_plot

# ----------------------- Internal functions ---------------------------------
# ----------------------------------------------------------------------------
def  combine_data(cst_data, garmin_data):
    
    cardio_dict = {
        "rate" : None,
        "rate_var" : None
        }
    breath_dict = {
        "rate" : None,
        }
    activity_dict = {
        "steps" : None,
        "distance" : None,
        }
    
    commun_data = {  
        "cardio" : cardio_dict,
        "breath" : breath_dict,
        "activity" : activity_dict,
        }
    
    # --- Cardio ---
    # Rate 
    garmin_df = garmin_data["cardio"]["rate"]
    cst_df = cst_data["cardio"]["rate"][["times", "values"]]

    commun_data["cardio"]["rate"] = merge_cst_and_garmin_data(cst_df, garmin_df)
    
    # Rate variability
    cst_df = cst_data["cardio"]["rate_var"]
    commun_data["cardio"]["rate_var"] = cst_df
    
    # --- Breath ---
    # Rate 
    garmin_df = garmin_data["breath"]["rate"]
    cst_df    = cst_data["breath"]["rate"][["times", "values"]]
    commun_data["breath"]["rate"] = merge_cst_and_garmin_data(cst_df, garmin_df)

    # Rate variability
    cst_df = cst_data["breath"]["rate_var"]
    commun_data["breath"]["rate_var"] = cst_df
    
    # --- Activity ---
    # Steps 
    garmin_df = garmin_data["activity"]["intensity"][["times", "steps"]]
    garmin_df = garmin_df.rename(columns={"steps": "values"})
    cst_df    = cst_data["activity"]["steps"]
    commun_data["activity"]["steps"] = merge_cst_and_garmin_data(garmin_df, cst_df)

    # Distance 
    garmin_df = garmin_data["activity"]["intensity"][["times", "distance"]]
    garmin_df.rename(columns = {'distance':'values'}, inplace = True)
    cst_df    = cst_data["activity"]["distance"]
    commun_data["activity"]["distance"] = merge_cst_and_garmin_data(garmin_df, cst_df)
    
    return copy.deepcopy(commun_data)

def initialize_dictionary_with_template() -> dict :
    cardio_dict = {
        "rate_high"        : None,
        "rate_resting"     : None,
        "rate_var_resting" : None,
    } 
    breath_dict = {
        "rate_high"        : None,
        "rate_resting"     : None,
        "rate_var_resting" : None,
        "ratio_in_exhale"  : None,
    } 
    activity_dict = {
        "steps"            : None,
        "distance"         : None,
        "goal"             : None,
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