import streamlit as st
import template.constant as constant
import template.test as test
import requests
import json
from pylife.api_functions import map_data
from pylife.api_functions import map_data_filt
from pylife.api_functions import map_results
from pylife.api_functions import get_sig_info
from pylife.api_functions import get_result_info

import copy
import pandas as pd
from datetime import datetime, timedelta

from data.useful_functions import find_time_intervals, sum_time_intervals
from data.config import RED_ALERT, GREEN_ALERT, ALERT_SIZE, ACTIVITY_THREASHOLD

# def get_smart_textile_indicators():
    
#     # !!! TO BE REPLACED !!!
#     indicators  = []
#     url         = st.session_state.url_data
#     api_key     = st.session_state.api_key
#     user        = st.session_state.end_user
#     types       = constant.TYPE()["INDICATORS"]
#     date        = st.session_state.date
    
#     params = {
#             'user':      user, # sub-user username
#             'types':     types, 
#             'date':      date,
#           }
    
#     # Perform the POST request authenticated with YOUR API key (NOT the one of the sub-user!).
#     reply = requests.get(url, headers={"X-API-Key": api_key}, params=params)
#     message, status_code = test.api_status(reply)
#     datas = []
#     if status_code == 200:
                
#         json_list_of_records = json.loads(reply.text) 
#         for record in json_list_of_records:
#             datas.append(record)
        
#         if len(datas) == 0:
#             status_code = 600
            
#     if status_code == 200:
        
#         # --- Map raw data 
#         indicators = {}
#         types_indicators    = constant.TYPE()["INDICATORS"].split(',')
#         results_mapped      = map_results(datas, types_indicators)
        
#         for key_type in types_indicators:
#             indicators[key_type] = {}
#             for val_type in ["times", "values"]:
#                 tmp = get_result_info(datas=results_mapped, result_type=key_type)
#                 indicators[key_type][val_type] = tmp[val_type]
        
#     st.session_state.smart_textile_indicators = indicators


# Imports


# ------------------------ The main function ---------------------------------
# ----------------------------------------------------------------------------
# Request user's data from servers

def get_chronolife_indicators():

    user_id     = st.session_state.end_user
    date        = st.session_state.date
    prod        = st.session_state.prod
    types       = constant.TYPE()["CHRONOLIFE_INDICATORS"]
    
    # We have to request data from date-1 and date+1, because we don't know 
    # the offset (if there is no data in requested date (utc))
    date_after = change_date(date, sign = +1)
    date_before = change_date(date, sign = -1)
    
    datas = get_datas(user_id, date, types)
    datas_before = get_datas(user_id, date_before, types)
    datas_after = get_datas(user_id, date_after, types)
    
    datas_3_days = datas + datas_before + datas_after

    # Save the results in a dictionary
    results_dict = initialize_dictionary_with_template()
    results_dict['user_id']  = user_id
    add_cardio(date, datas_3_days, results_dict['cardio'])
    add_breath(date, datas_3_days, results_dict['breath_1'])
    add_breath(date, datas_3_days, results_dict['breath_2'])                              # TO CHNAGE WHEN breath_2 is ready
    add_activity(date, datas_3_days, results_dict['activity'])
    add_durations(date, results_dict)
    
    # Add activity level to each indicator
    results_dict_2 = add_activity_to_indicators(copy.deepcopy(results_dict))
    add_anomalies(results_dict_2)
      
    st.session_state.chronolife_indicators = results_dict_2
    
# ----------------------- Internal functions ---------------------------------
# ----------------------------------------------------------------------------
def change_date(date:str, sign = -1) -> str:
    date_today = datetime.strptime(date, "%Y-%m-%d")
    new_date = date_today + sign*timedelta(days=1)
    new_date =  datetime.strftime(new_date, "%Y-%m-%d")
    return new_date

def get_datas(user_id, date, signal_types):
    api_key = st.session_state.api_key
    url     = st.session_state.url_data
    params = {
        'user'    : user_id,  
        'types'   : signal_types,
        'date'    : date,
        }
    
    reply = request_data_from_servers(params, api_key, url)
    datas = error_management(date, reply)

    return datas

def request_data_from_servers(params, api_key, url):
    # Perform the POST request authenticated with YOUR API key (NOT the one of the sub-user!).
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
    anomalies_dict = initialize_alerts_with_template()

    cardio_dict = {
        'rate' : None, 
        'rate_var' : None,
        }
    breath_dict = {
        'rate' : None, 
        'rate_var' : None,
        }
    activity_dict = {
        'steps' : None,
        'averaged_activity' : None,
        'distance' : None,
        }
    duration_dict = {
        'intervals' : None, 
        'collected' : None,
        'day' : None, 
        'noght' : None,
        'rest' : None,
        'active' : None,
        }
    
    dict_template = {
                    'user_id' : None,
                    'anomalies': copy.deepcopy(anomalies_dict),
                    'cardio'  : copy.deepcopy(cardio_dict),
                    'breath_1': copy.deepcopy(breath_dict),
                    'breath_2': copy.deepcopy(breath_dict),
                    'activity': copy.deepcopy(activity_dict),
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

    cardio_dict['rate'] = rate
    cardio_dict['rate_var'] = rate_var

def add_breath(date, datas, breath_dict):
    rate = get_cst_result_info(date, datas, result_type='respiratory_rate')

    breath_dict['rate'] = rate

def add_activity(date, datas, activity_dict) : 
    averaged_activity = get_cst_result_info(date, datas, result_type='averaged_activity')
    steps_number = get_cst_result_info(date, datas, result_type='steps_number')

    # Compose the distance dataframe # TO CHANGE !!! 
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
    
    # Breath_1 indicators TO CHANGE !!
    sig_indicators = results_dict["breath_1"]
    sig_indicators["rate"] = merge_on_times(sig_indicators["rate"], averaged_activity_df)
    
    # Breath 2 does not have indicators yet TO CHANGE !!
    sig_indicators = results_dict["breath_2"]
    sig_indicators["rate"] = merge_on_times(sig_indicators["rate"], averaged_activity_df)
  
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
    
    rest_times   = ref_df.loc[ref_df["values"] <= 15, "times"].reset_index(drop=True)
    active_times = ref_df.loc[ref_df["values"] > 15, "times"].reset_index(drop=True)
   
    
    time_intervals = find_time_intervals(ref_df['times'])
    day_time_intervals = find_time_intervals(day_times)
    night_time_intervals = find_time_intervals(night_times)
    rest_time_intervals = find_time_intervals(rest_times)
    activity_time_intervals = find_time_intervals(active_times)
    
    duration_dict = results_dict["duration"]
    duration_dict["collected"] = sum_time_intervals(time_intervals)
    duration_dict["day"] = sum_time_intervals(day_time_intervals)
    duration_dict["night"] = sum_time_intervals(night_time_intervals)
    duration_dict["rest"] = sum_time_intervals(rest_time_intervals)
    duration_dict["active"] = sum_time_intervals(activity_time_intervals)

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
    df_aux = results_dict['breath_1']['rate']
    values = df_aux.loc[df_aux["activity_values"] <= ACTIVITY_THREASHOLD, "values"].dropna().reset_index(drop=True)
    value = round(max(values))
    
    if(value > 20):
        alerts_dict["tachypnea"]["path"]  = RED_ALERT
    elif(value < 6):
        alerts_dict["bradypnea"]["path"]  = RED_ALERT

    # Cardio Tachy/Brady
    df_aux = results_dict['cardio']['rate']
    values = df_aux.loc[df_aux["activity_values"] <= ACTIVITY_THREASHOLD, "values"].dropna().reset_index(drop=True)
    value = round(max(values))

    if(value > 100):
        alerts_dict["tachycardia"]["path"] = RED_ALERT
    elif(value < 60):
        alerts_dict["bradycardia"]["path"]  = RED_ALERT
    
    # Cardio QTc length TO CHANGE TO CHANGE when indicator is updateted !!!
    alerts_dict["qt"]["path"]  = RED_ALERT

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

def get_timestamp(id_:str):
    output = 0
    timestamp = id_[:id_.index(".")]
    timestamp_int = int(timestamp)
    output = datetime.fromtimestamp(timestamp_int)

    return output

# %% ------------- Test the main function--------------------------------------
# results_dict = get_cst_data(user_id, date)


    
def get_smart_textile_raw_data():
    
    raw_data    = []
    url         = st.session_state.url_data
    api_key     = st.session_state.api_key
    user        = st.session_state.end_user
    types       = constant.TYPE()["SIGNALS"]
    date        = st.session_state.date
    time_gte    = st.session_state.start_time + ":00"
    time_lt     = st.session_state.end_time + ":00"
    
    params = {
           'user':      user, # sub-user username
           'types':     types, 
           'date':      date,
           'time_gte':  time_gte, # UTC
           'time_lt':   time_lt,  # UTC
         }
    
    # Perform the POST request authenticated with YOUR API key (NOT the one of the sub-user!).
    reply = requests.get(url, headers={"X-API-Key": api_key}, params=params)
    message, status_code = test.api_status(reply)
    datas = []
    if status_code == 200:
                
        json_list_of_records = json.loads(reply.text) 
        for record in json_list_of_records:
            datas.append(record)
        
        if len(datas) == 0:
            status_code = 600
    
    if status_code == 200:
        # --- Map raw data 
        raw_data = {}
        types_raw       = constant.TYPE()["RAW_SIGNALS"].split(',')
        datas_mapped = map_data(datas, types_raw)
        
        for key_type in types_raw:
            raw_data[key_type] = {}
            for val_type in ["times", "sig"]:
                tmp = get_sig_info(datas_mapped, key_type, verbose=0)
                raw_data[key_type][val_type] = tmp[val_type]
        
        # --- Map filtered data 
        types_filtered  = constant.TYPE()["FILTERED_SIGNALS"].split(',')
        datas_filtered_mapped = map_data_filt(datas, types_filtered)
        for key_type in types_filtered:
            raw_data[key_type] = {}
            for val_type in ["times", "sig"]:
                tmp = get_sig_info(datas_filtered_mapped, key_type, verbose=0)
                raw_data[key_type][val_type] = tmp[val_type]
                
    st.session_state.smart_textile_raw_data = raw_data