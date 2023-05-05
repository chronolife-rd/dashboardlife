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