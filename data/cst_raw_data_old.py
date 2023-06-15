import streamlit as st
import template.constant as constant
import template.test as test
import requests
import json
from datetime import datetime, timedelta
from pylife.api_functions import map_data
from pylife.api_functions import map_data_filt
from pylife.api_functions import get_sig_info
from data.data import get_offset
   
def get_raw_data():
    offset_info = get_offset()
    
    url         = st.session_state.url_data
    api_key     = st.session_state.api_key
    user        = st.session_state.end_user
    types       = constant.TYPE()["SIGNALS"]
    date        = st.session_state.date
    start_time  = st.session_state.start_time + ":00" # str
    end_time    = st.session_state.end_time + ":00"   # str

    time_gte    = start_time 
    time_lt     = end_time

    if isinstance(offset_info["value"], str) == False:
        sign = offset_info["sign"] 
        format_datetime = "%H:%M:%S"
        # Str to datetime
        start_time = datetime.strptime(start_time, format_datetime) # datetime
        end_time   = datetime.strptime(end_time, format_datetime)   # datetime
        
        time_gte  = start_time + sign*timedelta(seconds = offset_info["value"])
        time_lt   = end_time + sign*timedelta(seconds = offset_info["value"])

        # Datetime to str 
        time_gte = datetime.strftime(time_gte, format_datetime)  # str
        time_lt  = datetime.strftime(time_lt, format_datetime)   # str
    
    params = {
           'user':      user, # sub-user username
           'types':     types, 
           'date':      date,
           'time_gte':  time_gte, # UTC
           'time_lt':   time_lt,  # UTC
         }
    
    # Perform the POST request authenticated with YOUR API key (NOT the one of the sub-user!).
    reply = get_reply(params, url, api_key)
    _, status_code = test.api_status(reply)

    raw_data = request_datas(reply, status_code)

    # Declare as global variable
    st.session_state.smart_textile_raw_data = raw_data

def get_reply(params, url, api_key):
    reply = requests.get(url, headers={"X-API-Key": api_key}, params=params)
    return reply

def request_datas(reply, status_code):
    datas = []
    raw_data    = []

    if status_code == 200:  
        json_list_of_records = json.loads(reply.text) 
        for record in json_list_of_records:
            datas.append(record)
        
        if len(datas) == 0:
            status_code = 600
    
    if status_code == 200:
        raw_data = {}

        # --- Map raw data 
        map_raw_data(datas, raw_data)
        
        # --- Map filtered data 
        map_filtered_data(datas, raw_data)
        print(raw_data)
    
    return raw_data

def map_raw_data(datas, raw_data):
    types_raw    = constant.TYPE()["RAW_SIGNALS"].split(',')
    datas_mapped = map_data(datas, types_raw)
    
    for key_type in types_raw:
        raw_data[key_type] = get_sig_info(datas_mapped, key_type, verbose=0)
    
def map_filtered_data(datas, raw_data):
    types_filtered  = constant.TYPE()["FILTERED_SIGNALS"].split(',')
    datas_filtered_mapped = map_data_filt(datas, types_filtered)
    for key_type in types_filtered:
        raw_data[key_type] = get_sig_info(datas_filtered_mapped, key_type, verbose=0)






