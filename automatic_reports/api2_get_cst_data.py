
# Imports
import json
import copy
import math
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from automatic_reports.useful_functions import find_time_intervals, sum_time_intervals, timedelta_formatter, unwrap
from automatic_reports.config import CST_SIGNAL_TYPES
from automatic_reports.config import RED_ALERT, GREEN_ALERT, ALERT_SIZE, ACTIVITY_THREASHOLD
from automatic_reports.config import TACHYPNEA_TH, BRADYPNEA_TH, TACHYCARDIA_TH, BRADYCARDIA_TH,\
    QT_MAX_TH, QT_MIN_TH
    
# ------------------------ The main function ---------------------------------
# ----------------------------------------------------------------------------
# Request user's data from servers

def get_cst_data(user_id, date, api, url):

    # We have to request data from date-1 and date+1, because we don't know 
    # the offset (if there is no data in requested date (utc))
    date_after = change_date(date, sign = +1)
    date_before = change_date(date, sign = -1)
    
    datas = get_datas(user_id, date, CST_SIGNAL_TYPES, api, url)
    datas_before = get_datas(user_id, date_before, CST_SIGNAL_TYPES, api, url)
    datas_after = get_datas(user_id, date_after, CST_SIGNAL_TYPES, api, url)
    
    datas_3_days = datas + datas_before + datas_after

    # Save the results in a dictionary
    results_dict = initialize_dictionary_with_template()
    results_dict['user_id']  = user_id
    add_cardio(date, datas_3_days, results_dict['cardio'])
    add_breath(date, datas_3_days, results_dict['breath'])                  
    add_activity(date, datas_3_days, results_dict['activity'])
    add_durations(date, results_dict)
    
    # Add activity level to each indicator
    results_dict_2 = add_activity_to_indicators(copy.deepcopy(results_dict))

    # Add anomalie (alerts)
    add_anomalies(results_dict_2)
      
    return results_dict_2

# ----------------------- Internal functions ---------------------------------
# ----------------------------------------------------------------------------
def change_date(date:str, sign = -1) -> str:
    date_today = datetime.strptime(date, "%Y-%m-%d")
    new_date = date_today + sign*timedelta(days=1)
    new_date =  datetime.strftime(new_date, "%Y-%m-%d")
    return new_date

def get_datas(user_id, date, signal_types, api, url):
    params = {
        'user'    : user_id,  
        'types'   : signal_types,
        'date'    : date,
        }
    
    reply = request_data_from_servers(params, api, url)
    datas = error_management(date, reply)

    return datas

def request_data_from_servers(params, api_key, url):
    # Perform the POST request authenticated with YOUR API key (NOT the one of 
    # the sub-user!).
    reply = requests.get(url, headers={"X-API-Key": api_key}, params=params)
    
    return reply

def error_management(date, reply) :
    datas = []
    # Error management 
    if reply.status_code == 200:
      # Convert the reply content into a json object.
      json_list_of_records = json.loads(reply.text) 
      for record in json_list_of_records:
          datas.append(record)
    elif reply.status_code == 400:
        print('Part of the request could not be parsed or is incorrect.')
    elif reply.status_code == 401:
        print('Invalid authentication')
    elif reply.status_code == 403:
        print('Not authorized.')
    elif reply.status_code == 404:
        print('Invalid url')
    elif reply.status_code == 500:
        print('Invalid user ID')
    
    if len(datas) == 0:
        print('No data found for day:', date)
    
    return datas

def initialize_dictionary_with_template() -> dict :  
    activity_dict = {
        'steps' : None,
        'averaged_activity' : None,
        'distance' : None,
        }
    anomalies_dict = initialize_alerts_with_template()
    breath_dict = {
        'rate' : None, 
        'rate_var' : None,
        'inspi_expi' : None,
        }
    cardio_dict = {
        'rate' : None, 
        'rate_var' : None,
         }
    duration_dict = {
        'intervals' : None, 
        'collected' : None,
        'day' : None, 
        'night' : None,
        'rest' : None,
        'active' : None,
        }
    dict_template = {
                    'user_id' : None,
                    'activity': copy.deepcopy(activity_dict),
                    'anomalies': copy.deepcopy(anomalies_dict),
                    'breath': copy.deepcopy(breath_dict),
                    'cardio'  : copy.deepcopy(cardio_dict),
                    'duration': copy.deepcopy(duration_dict),
                    }
    return copy.deepcopy(dict_template)

def initialize_alerts_with_template() -> dict :
    pdf_info = {
        "path" : GREEN_ALERT,
        "x" : None,
        "y" : None,
        "w" : ALERT_SIZE,
        "h" : ALERT_SIZE,
        "exists" : False,
        "min" : "",
        "max" : "",
        "high" : "",
        "resting" : "",
        "percentage" : "",
        "duration" : "",
        "values" : []
        }

    dict_template = {
        "tachypnea"   : copy.deepcopy(pdf_info), 
        "bradypnea"   : copy.deepcopy(pdf_info),
        "tachycardia" : copy.deepcopy(pdf_info), 
        "bradycardia" : copy.deepcopy(pdf_info),
        "qt"          : copy.deepcopy(pdf_info),
    }
    return copy.deepcopy(dict_template)

def add_cardio(date, datas, cardio_dict):
    rate = get_cst_result_info(date, datas, result_type='heartbeat')
    rate_var = get_cst_result_info(date, datas, result_type='HRV')
    qt = get_cst_result_info_segment(date, datas, result_type='qt_c_framingham_per_seg')

    cardio_dict['rate'] = rate
    cardio_dict['rate_var'] = rate_var
    cardio_dict['qt'] = qt

def add_breath(date, datas, breath_dict):
    rate = get_cst_result_info(date, datas, result_type='breath_2_brpm')
    rate_var = get_cst_result_info(date, datas, result_type='breath_2_brv')
    inspi_expi = get_cst_result_info_segment(date, datas, result_type='breath_2_inspi_over_expi') # TO CHANGE!!!

    breath_dict['rate'] = rate
    breath_dict['rate_var'] = rate_var
    breath_dict['inspi_expi'] = inspi_expi

def add_activity(date, datas, activity_dict) : 
    averaged_activity = get_cst_result_info(date, datas, result_type='averaged_activity')
    steps_number = get_cst_result_info(date, datas, result_type='steps_number')

    # Compose the distance dataframe  
    times = steps_number["times"]
    values = steps_number["values"]*0.76
    distance = pd.DataFrame({'times' : times, 'values' : values})
    
    activity_dict['steps'] = steps_number
    activity_dict['averaged_activity' ] = averaged_activity
    activity_dict['distance'] = distance

def add_activity_to_indicators(results_dict) -> dict:
    averaged_activity_df = results_dict["activity"]["averaged_activity"]
    averaged_activity_df.rename(columns={"values": "activity_values"}, inplace=True)
    
    # ECG indicators
    sig_indicators = results_dict["cardio"]
    sig_indicators["rate"] = merge_on_times(sig_indicators["rate"], averaged_activity_df)
    sig_indicators["rate_var"] = merge_on_times(sig_indicators["rate_var"], averaged_activity_df)
    sig_indicators["qt"] = merge_on_times(sig_indicators["qt"], averaged_activity_df)
    
    # Breath 
    sig_indicators = results_dict["breath"]
    sig_indicators["rate"] = merge_on_times(sig_indicators["rate"], averaged_activity_df)
    sig_indicators["rate_var"] = merge_on_times(sig_indicators["rate_var"], averaged_activity_df)
    sig_indicators["inspi_expi"] = merge_on_times(sig_indicators["inspi_expi"], averaged_activity_df)

    return copy.deepcopy(results_dict)

def add_durations(date, results_dict):
    # Times constants
    YEAR = int(date[:4])
    M = int(date[5:7])
    D = int(date[8:10])
    NIGHT_LIMIT = datetime(YEAR, M, D, 6, 0, 0)

    ref_df = results_dict['activity']['averaged_activity']

    day_times    = ref_df.loc[ref_df["times"] > NIGHT_LIMIT,
                               "times"].reset_index(drop=True)
    night_times  = ref_df.loc[ref_df["times"] < NIGHT_LIMIT, 
                                    "times"].reset_index(drop=True)
    
    rest_times   = ref_df.loc[ref_df["values"] <= ACTIVITY_THREASHOLD,
                            "times"].reset_index(drop=True)   
    
    time_intervals = find_time_intervals(ref_df['times'])
    day_time_intervals = find_time_intervals(day_times)
    night_time_intervals = find_time_intervals(night_times)
    rest_time_intervals = find_time_intervals(rest_times)
    
    collected_in_s = sum_time_intervals(time_intervals)
    day_in_s = sum_time_intervals(day_time_intervals)
    night_in_s = sum_time_intervals(night_time_intervals)
    rest_in_s = sum_time_intervals(rest_time_intervals)
    active_in_s = collected_in_s - rest_in_s
    
    duration_dict = results_dict["duration"]
    duration_dict["intervals"] = time_intervals
    duration_dict["collected"] = timedelta_formatter(collected_in_s)
    duration_dict["day"] = timedelta_formatter(day_in_s)
    duration_dict["night"] = timedelta_formatter(night_in_s)
    duration_dict["rest"] = timedelta_formatter(rest_in_s)
    duration_dict["active"] = timedelta_formatter(active_in_s)
    
def add_anomalies(results_dict):
    alerts_dict = results_dict['anomalies']
    # --- Set alerts image positions ---
    # Tachypnea
    alerts_dict["tachypnea"]["x"]  = 4.56
    alerts_dict["tachypnea"]["y"]  = 7.01 + ALERT_SIZE
    # Bradypnea
    alerts_dict["bradypnea"]["x"]  = 4.56
    alerts_dict["bradypnea"]["y"]  = 7.23 + ALERT_SIZE
    # Tachycardia
    alerts_dict["tachycardia"]["x"]  = 1.95
    alerts_dict["tachycardia"]["y"]  = 7.01 + ALERT_SIZE
    # Bradycardia
    alerts_dict["bradycardia"]["x"]  = 1.95
    alerts_dict["bradycardia"]["y"]  = 7.23 + ALERT_SIZE
    # QT
    alerts_dict["qt"]["x"]  = 1.95
    alerts_dict["qt"]["y"]  = 7.45 + ALERT_SIZE

    # ------------------- detect anomaly ----------------------
    # Cardio Tachy/Brady
    df_aux = results_dict['breath']['rate']
    values = df_aux.loc[df_aux["activity_values"] <= ACTIVITY_THREASHOLD, "values"].dropna().reset_index(drop=True)
    value = round(max(values))
    
    if(value > TACHYPNEA_TH):
        alerts_dict["tachypnea"]["path"]  = RED_ALERT
        alerts_dict["tachypnea"]["exists"] = True
        alerts_dict["tachypnea"]["values"] = values
    elif(value < BRADYPNEA_TH):
        alerts_dict["bradypnea"]["path"]  = RED_ALERT
        alerts_dict["bradypnea"]["exists"] = True
        alerts_dict["bradypnea"]["values"] = values

    # Cardio Tachy/Brady
    df_aux = results_dict['cardio']['rate']
    values = df_aux.loc[df_aux["activity_values"] <= ACTIVITY_THREASHOLD, "values"].dropna().reset_index(drop=True)
    value = round(max(values))

    if(value > TACHYCARDIA_TH):
        alerts_dict["tachycardia"]["path"] = RED_ALERT
        alerts_dict["tachycardia"]["exists"] = True
        alerts_dict["tachycardia"]["values"] = values
        alerts_dict["tachycardia"]["mean"] = round(np.mean(values))
        alerts_dict["tachycardia"]["duration"] = -1
        alerts_dict["tachycardia"]["percentage"] = -1

    elif(value < BRADYCARDIA_TH):
        alerts_dict["bradycardia"]["path"]  = RED_ALERT
        alerts_dict["bradycardia"]["exists"] = True
        alerts_dict["bradycardia"]["values"] = values
        alerts_dict["bradycardia"]["mean"] = round(np.mean(values))
        alerts_dict["bradycardia"]["duration"] = -1
        alerts_dict["bradycardia"]["percentage"] = -1
    
    # Cardio QTc length TO CHANGE TO CHANGE when indicator is updateted !!!
    df_aux = results_dict['cardio']['qt']
    values = df_aux.loc[df_aux["activity_values"] <= ACTIVITY_THREASHOLD, "values"].dropna().reset_index(drop=True)
    value_max = round(max(values))
    value_min = round(min(values))
    if(value_max > QT_MAX_TH or value_min < QT_MIN_TH):
        alerts_dict["qt"]["path"]  = RED_ALERT
        alerts_dict["qt"]["exists"] = True
        alerts_dict["qt"]["values"] = values
        alerts_dict["qt"]["min"] = round(min(values))
        alerts_dict["qt"]["max"] = round(max(values))
        alerts_dict["qt"]["mean"] = round(np.mean(values))
        alerts_dict["qt"]["duration"] = -1
        alerts_dict["qt"]["percentage"] = -1

def merge_on_times(df_1, df_2):
    df_result = pd.merge(df_1, df_2, how="outer", on="times")
    df_result.sort_values(by="times", inplace = True)
    df_result = df_result.reset_index(drop=True)
                   
    return copy.deepcopy(df_result)

def get_cst_result_info(date, datas, result_type):
    times = []
    values = []
    output = pd.DataFrame({
    'times' : times,
    'values' : values,
    })

    for data in datas:
        if result_type == data['type']:
            timestamp = get_timestamp(data['_id'])
            times.append(timestamp)
            values.append(data['values'])

    output['times'] = times
    output['values'] = values
    output.sort_values(by = 'times', inplace = True) 

    # Get output where times = date
    YEAR = int(date[:4])
    M = int(date[5:7])
    D = int(date[8:10])
    start_date = datetime(YEAR, M, D, 0, 0, 0)
    end_date = datetime(YEAR, M, D, 23, 59, 59)
    mask = (output['times'] > start_date) & (output['times'] <= end_date)
    output = output.loc[mask]
    output = output.reset_index(drop=True)

    # Round times to minutes
    output['times'] = output["times"].dt.round("min")
    # Format type from pandas._libs.tslibs.timestamps.Timestamp to datetime
    output['times'] = output["times"]

    return output

def get_cst_result_info_segment(date, datas, result_type):
    times = []
    values = []
    output = pd.DataFrame({
    'times' : times,
    'values' : values,
    })

    for data in datas:
        if result_type == data['type']:
            timestamp = get_timestamp(data['_id'])
            times.append(timestamp)
            segment_values = unwrap(data['values'])
            if np.size(segment_values) > 1:         # Nan values have size = 1       
                mean_value = round(np.mean(segment_values))
            else: mean_value = math.nan
            values.append(mean_value)

    output['times'] = times
    output['values'] = values
    output.sort_values(by = 'times', inplace = True) 

    # Get output where times = date
    YEAR = int(date[:4])
    M = int(date[5:7])
    D = int(date[8:10])
    start_date = datetime(YEAR, M, D, 0, 0, 0)
    end_date = datetime(YEAR, M, D, 23, 59, 59)
    mask = (output['times'] > start_date) & (output['times'] <= end_date)
    output = output.loc[mask]
    output = output.reset_index(drop=True)

    # Round times to minutes
    output['times'] = output["times"].dt.round("min")
    # Format type from pandas._libs.tslibs.timestamps.Timestamp to datetime
    output['times'] = output["times"]

    return output

def get_timestamp(id_:str):
    output = 0
    timestamp = id_[:id_.index(".")]
    timestamp_int = int(timestamp)
    output = datetime.fromtimestamp(timestamp_int)

    return output

# %% ------------- Test the main function-------------------------------------
# from config import API_KEY_PREPROD, API_KEY_PROD, URL_CST_PREPROD, URL_CST_PROD
# prod = False
# # -- Ludo
# user_id = "4vk5VJ"
# date = "2023-05-17"
# # -- Fernando
# user_id = "5Nwwut"
# date = "2023-05-17"
# # -- Michel
# # user_id = "5Nwwut" 
# # date = "2023-05-04" 
# # -- Adriana
# # user_id = "6o2Fzp"
# # date = "2023-05-10"

# if prod == True :
#     api = API_KEY_PROD
#     url = URL_CST_PROD
# else :
#     api = API_KEY_PREPROD
#     url = URL_CST_PREPROD

# results_dict = get_cst_data(user_id, date, api, url)
