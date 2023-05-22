import streamlit as st
import template.constant as constant
import requests
import json
from pylife.api_functions import map_data
from pylife.api_functions import map_data_filt
from pylife.api_functions import get_sig_info
   

st.session_state.url_data = "https://preprod.chronolife.net/api/2/data"
st.session_state.api_key = '3-1krbPQoufnmNVN6semRA'
st.session_state.end_user = "4vk5VJ"
st.session_state.date = "2023-05-17"
st.session_state.start_time = "14:00"
st.session_state.end_time = "14:05"

def get_raw_data():
    
    raw_data    = []
    url         = "https://preprod.chronolife.net/api/2/data"
    api_key     = '3-1krbPQoufnmNVN6semRA'
    user        = "4vk5VJ"
    types       = constant.TYPE()["SIGNALS"]
    date        = "2023-05-17"
    time_gte    = "14:00:00"
    time_lt     = "14:05:00"
    
    params = {
           'user':      user, # sub-user username
           'types':     types, 
           'date':      date,
           'time_gte':  time_gte, # UTC
           'time_lt':   time_lt,  # UTC
         }
    
    # Perform the POST request authenticated with YOUR API key (NOT the one of the sub-user!).
    reply = get_reply(params, url, api_key)
    message, status_code = api_status(reply)

    raw_data = request_datas(reply, status_code)

    # Declare as global variable
    return raw_data

def api_status(reply, user_text='Username'):
    
    status_code = reply.status_code
        
    if status_code == 200:
        message = "api_auth_200" #'Connected'
    elif status_code == 400:
        message = "api_auth_400" #'Part of the request could not be parsed or is incorrect'
    elif status_code == 401:
        message = "api_auth_401" #'Incorrect API key'
    elif status_code == 403:
        message = "api_auth_403" #'Not authorized'
    elif status_code == 404:
        message = "api_auth_404" #'Incorrect url'
    elif status_code == 500:
        message = "api_auth_500"
    elif status_code == 0:
        message = "api_auth_0" #"You are disconnect"
        
    return message, status_code

def get_reply(params, url, api_key):
    reply = requests.get(url, headers={"X-API-Key": api_key}, params=params)
    return reply

def request_datas(reply, status_code):
    datas = []

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
    
    return raw_data

def map_raw_data(datas, raw_data):
    types_raw    = constant.TYPE()["RAW_SIGNALS"].split(',')
    datas_mapped = map_data(datas, types_raw)
    
    for key_type in types_raw:
        raw_data[key_type] = {}
        for val_type in ["times", "sig"]:
            tmp = get_sig_info(datas_mapped, key_type, verbose=0)
            raw_data[key_type][val_type] = tmp[val_type]
    
def map_filtered_data(datas, raw_data):
    types_filtered  = constant.TYPE()["FILTERED_SIGNALS"].split(',')
    datas_filtered_mapped = map_data_filt(datas, types_filtered)
    for key_type in types_filtered:
        raw_data[key_type] = {}
        for val_type in ["times", "sig"]:
            tmp = get_sig_info(datas_filtered_mapped, key_type, verbose=0)
            raw_data[key_type][val_type] = tmp[val_type]

# -- test get_raw_data -- 


raw_data = get_raw_data()






