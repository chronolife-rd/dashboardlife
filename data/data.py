import streamlit as st
import pandas as pd
from io import BytesIO
import numpy as np
import template.test as test
import requests
import json
from pylife.api_functions import map_results
from pylife.api_functions import get_result_info
from pylife.useful import unwrap
import time

# Imports for requesting data and genereting reports
from garmin_automatic_reports.api2_get_cst_data import get_cst_data
from garmin_automatic_reports.api2_get_garmin_data import get_garmin_data
from garmin_automatic_reports.compute_commun_for_html import get_commun_indicators
from garmin_automatic_reports.plot_images import plot_images


def get_health_indicators():
    
    end_user    = st.session_state.end_user
    date        = st.session_state.date
    api         = st.session_state.api_key 
    url_cst     = st.session_state.url_data 
    url_garmin  = st.session_state.url_garmin
    
    garmin_data = []
    cst_data    = []
    commun_data = []

    # Get CST (Chronolife Smart Textile) data
    cst_data = get_cst_data(
        user_id = end_user, 
        date = date,
        api = api,
        url = url_cst,
        )
    
    # Get Garmin data
    garmin_data = get_garmin_data(
        user_id = end_user, 
        date = date,
        api = api,
        url = url_garmin
        )
    
    # Compute commun data
    commun_data, commun_indicators,\
    steps_dict = get_commun_indicators(cst_data, garmin_data) 

    st.session_state.garmin_indicators      = garmin_data
    st.session_state.chronolife_indicators  = cst_data
    st.session_state.commun_data            = commun_data       # New
    st.session_state.commun_indicators      = commun_indicators # New
    st.session_state.steps_dict             = steps_dict        # New

def get_bodybattery():
    datas = st.session_state.garmin_indicators

    output = {}
    output['values'] = ""
    output["high"]   = ""
    output["low"]    = ""
    
    if len(datas) > 0 and datas["body_battery"]["highest"] is not None:
        output["values"] = datas["body_battery"]["all_values"]
        output["high"]   = datas["body_battery"]["highest"]
        output["low"]    = datas["body_battery"]["lowest"]
    
    return output

def get_calories():
    datas = st.session_state.garmin_indicators
    
    output = {}
    output["total"]    = ""
    output["rest"]  = ""
    output["active"]   = ""
    
    if len(datas) > 0 and datas["calories"]["total"] is not None:
        output["total"]    = datas["calories"]["total"]
        output["rest"]  = datas["calories"]["resting"]
        output["active"]   = datas["calories"]["active"]

    return output


def get_intensity():
    datas = st.session_state.garmin_indicators
    
    output = {}
    output["total"]     = ""
    output["moderate"]  = ""
    output["vigurous"]  = ""
    
    if len(datas) > 0 and datas["intensity_min"]["total"] is not None:
            output["total"]    = td_to_hhmm_str(datas["intensity_min"]["total"])
            output["moderate"] = td_to_hhmm_str(datas["intensity_min"]["moderate"])
            output["vigurous"] = td_to_hhmm_str(datas["intensity_min"]["vigurous"])
    
    return output

def get_sleep():
    datas = st.session_state.garmin_indicators
    
    output = {}
    output["values"]            = ""
    output["score"]             = ""
    output["quality"]           = ""
    output["duration"]          = ""
    output["duration_deep"]     = ""
    output["duration_light"]    = ""
    output["duration_rem"]      = ""
    output["duration_awake"]    = ""
    output["percentage_deep"]   = ""
    output["percentage_light"]  = ""
    output["percentage_rem"]    = ""
    output["percentage_awake"]  = ""
    
    if len(datas) > 0 and datas["sleep"]["score"] is not None:
        output["values"]            = datas["sleep"]["sleep_map"]
        output["score"]             = datas["sleep"]["score"]
        output["quality"]           = datas["sleep"]["quality"]
        output["duration"]          = datas["sleep"]["recorded_time"]
        output["duration_deep"]     = td_to_hhmm_str(datas["sleep"]["deep"])
        output["duration_light"]    = td_to_hhmm_str(datas["sleep"]["light"])
        output["duration_rem"]      = td_to_hhmm_str(datas["sleep"]["rem"])
        output["duration_awake"]    = td_to_hhmm_str(datas["sleep"]["awake"])

        output["percentage_deep"]   = int(round(datas["sleep"]["deep"]/datas["sleep"]["recorded_time"]*100))
        output["percentage_light"]  = int(round(datas["sleep"]["light"]/datas["sleep"]["recorded_time"]*100))
        output["percentage_rem"]    = int(round(datas["sleep"]["rem"]/datas["sleep"]["recorded_time"]*100))
        output["percentage_awake"]  = int(round(datas["sleep"]["awake"]/datas["sleep"]["recorded_time"]*100))

    return output

def get_spo2():
    datas = st.session_state.garmin_indicators
    
    output = {}
    output["mean"]    = ""
    output["min"]     = ""
    output["values"]  = ""
    
    if len(datas) > 0 and datas["spo2"]["averege"] is not None:
            output["mean"]    = datas["spo2"]["averege"]
            output["min"]     = datas["spo2"]["lowest"]
            output["values"]  = datas["spo2"]["all_values"]
    
    return output

def get_stress():
    datas = st.session_state.garmin_indicators
    
    output = {}
    output["values"]            = ""
    output["score"]             = ""
    output["duration"]          = ""
    output["duration_rest"]     = ""
    output["duration_low"]      = ""
    output["duration_medium"]   = ""
    output["duration_high"]     = ""
    output["percentage_rest"]   = ""
    output["percentage_low"]    = ""
    output["percentage_medium"] = ""
    output["percentage_high"]   = ""
    
    if len(datas) > 0 and datas["stress"]["recorded_time"] is not None:
        output["values"]            = datas["stress"]["all_values"]
        output["score"]             = datas["stress"]["score"]
        output["duration"]          = datas["stress"]["recorded_time"]
        
        output["duration_rest"]     = td_to_hhmm_str(datas["stress"]["rest"])
        output["duration_low"]      = td_to_hhmm_str(datas["stress"]["low"])
        output["duration_medium"]   = td_to_hhmm_str(datas["stress"]["medium"])
        output["duration_high"]     = td_to_hhmm_str(datas["stress"]["high"])
        
        output["percentage_rest"]   = int(round(datas["stress"]["rest"]/datas["stress"]["recorded_time"]*100))
        output["percentage_low"]    = int(round(datas["stress"]["low"]/datas["stress"]["recorded_time"]*100))
        output["percentage_medium"] = int(round(datas["stress"]["medium"]/datas["stress"]["recorded_time"]*100))
        output["percentage_high"]   = int(round(datas["stress"]["high"]/datas["stress"]["recorded_time"]*100))
    
    return output

def get_duration_chronolife():
    datas = st.session_state.chronolife_indicators

    output = {}    
    output["duration"]          = ""
    output["duration_day"]      = ""
    output["duration_night"]    = ""
    output["duration_rest"]     = "" 
    output["duration_activity"] = ""
    
    if len(datas) > 0 and datas["duration"]["collected"] is not None:
        output["duration"]          = datas["duration"]["collected"] 
        output["duration_day"]      = datas["duration"]["day"]
        output["duration_night"]    = datas["duration"]["night"] 
        output["duration_rest"]     = datas["duration"]["rest"] 
        output["duration_activity"] = datas["duration"]["active"] 
    
    return output

def get_duration_garmin():
    datas = st.session_state.garmin_indicators

    output = {}    
    output["duration"]          = ""
    output["duration_day"]      = ""
    output["duration_night"]    = ""
    output["duration_rest"]     = "" 
    output["duration_activity"] = ""
    
    if len(datas) > 0 and datas["duration"]["collected"] is not None:
        output["duration"]          = datas["duration"]["collected"] 
        output["duration_day"]      = datas["duration"]["day"]
        output["duration_night"]    = datas["duration"]["night"] 
        output["duration_rest"]     = datas["duration"]["rest"] 
        output["duration_activity"] = datas["duration"]["active"] 
    
    return output    

def get_steps():
    datas = st.session_state.commun_indicators
  
    output = {}
    output["number"]    = ""
    output["goal"]      = ""
    output["score"]     = ""
    output["distance"]  = ""

    if len(datas) > 0 and datas["activity"]["distance"] is not None:
        output["number"]    = datas["activity"]["steps"] 
        output["goal"]      = datas["activity"]["goal"] 
        output["distance"]  = datas["activity"]["distance"] 
        output["score"]     = int(output["number"]/output["goal"]*100)
    
    return output

def get_temperature():
    
    # !!! TO BE UPDATED !!!
    output = {}
    #/ output["mean"]  = ""
    # output["min"]   = ""
    # output["max"]   = ""
    
    output["mean"]  = 35.4
    output["min"]   = 33.4
    output["max"]   = 37.1
    
    return output

def get_bpm():
    datas = st.session_state.commun_indicators

    # !!! TO BE UPDATED !!!
    output = {}
    output["mean"]  = ""
    output["min"]   = ""
    output["max"]   = ""
    output["rest"]  = ""
    output["high"]  = ""
    
    if len(datas) > 0 and datas["cardio"]["rate_high"] is not None:
        output["mean"]  = 500
        output["min"]   = 500
        output["max"]   = 500
        output["rest"]  = datas["cardio"]["rate_resting"] 
        output["high"]  = datas["cardio"]["rate_high"] 
    
    return output

def get_hrv():
    datas = st.session_state.commun_indicators

    # !!! TO BE UPDATED !!!
    output = {}
    output["mean"]  = ""
    output["min"]   = ""
    output["max"]   = ""
    output["rest"]  = ""
    output["high"]  = ""

    if len(datas) > 0 and datas["cardio"]["rate_var_resting"] is not None:
        output["mean"]  = 500
        output["min"]   = 500
        output["max"]   = 500
        output["rest"]  = datas["cardio"]["rate_var_resting"] 
        output["high"]  = 500
    
    return output

def get_qt():
    datas = st.session_state.chronolife_indicators
    
    # !!! TO BE UPDATED !!!
    output = {}
    output["exists"]    = False
    output["mean"]      = ""
    output["min"]       = ""
    output["max"]       = ""
    output["rest"]      = ""
    output["high"]      = ""
    output["threshold"] = ""
    
    if len(datas["anomalies"]["qt"]["values"]) > 0:
        values = datas["anomalies"]["qt"]["values"]
        output["exists"]    = datas["anomalies"]["qt"]["exists"]
        output["mean"]      = round(np.mean(values))
        output["min"]       = round(min(values))
        output["max"]       = round(max(values))
        output["rest"]      = 500
        output["high"]      = 500
        output["threshold"] = 550
    
    if output["exists"]:
        qt_alert_icon = st.session_state.alert
    else:
        qt_alert_icon = st.session_state.alert_no
    st.session_state.qt_alert_icon          = qt_alert_icon
    
    return output

def get_bradycardia():
    datas = st.session_state.chronolife_indicators

    # !!! TO BE UPDATED !!!
    output = {}
    output["exists"]      = ""
    output["mean"]        = ""
    output["duration"]    = ""
    output["percentage"]  = ""
    
    if len(datas["anomalies"]["bradycardia"]["values"]) > 0:
        values = datas["anomalies"]["bradycardia"]["values"]
        output["exists"]      = datas["anomalies"]["bradycardia"]["exists"]
        output["mean"]        = round(np.mean(values))
        output["duration"]    = 500
        output["percentage"]  = 500
    
    if output["exists"]:
        bradycardia_alert_icon = st.session_state.alert
    else:
        bradycardia_alert_icon = st.session_state.alert_no
    st.session_state.bradycardia_alert_icon = bradycardia_alert_icon
    
    return output
    
def get_tachycardia():
    datas = st.session_state.chronolife_indicators

    # !!! TO BE UPDATED !!!
    output = {}
    output["exists"]      = ""
    output["mean"]        = ""
    output["duration"]    = ""
    output["percentage"]  = ""

    if len(datas["anomalies"]["tachycardia"]["values"]) > 0:
        values = datas["anomalies"]["tachycardia"]["values"]
        output["exists"]      = datas["anomalies"]["tachycardia"]["exists"]
        output["mean"]        = round(np.mean(values))
        output["duration"]    = 500
        output["percentage"]  = 500
    
    if output["exists"]:
        tachycardia_alert_icon = st.session_state.alert
    else:
        tachycardia_alert_icon = st.session_state.alert_no
    st.session_state.tachycardia_alert_icon = tachycardia_alert_icon
    
    return output

def get_brpm():
    datas = st.session_state.commun_indicators

    # !!! TO BE UPDATED !!!
    output = {}
    output["mean"]  = ""
    output["min"]   = ""
    output["max"]   = ""
    output["rest"]  = ""
    output["high"]  = ""
    
    if len(datas) > 0 and datas["breath"]["rate_high"] is not None:
        output["mean"]  = 500
        output["min"]   = 500
        output["max"]   = 500
        output["rest"]  = datas["breath"]["rate_resting"] 
        output["high"]  = datas["breath"]["rate_high"] 
    
    return output

def get_brv():
    datas = st.session_state.commun_indicators

    # !!! TO BE UPDATED !!!
    output = {}
    output["mean"]  = ""
    output["min"]   = ""
    output["max"]   = ""
    output["rest"]  = ""
    output["high"]  = ""

    if len(datas) > 0 and datas["breath"]["rate_var_resting"] is not None:
        output["mean"]  = 1.2
        output["min"]   = 0.2
        output["max"]   = 2.0
        output["rest"]  = datas["breath"]["rate_var_resting"]
        output["high"]  = 1.8
    
    return output

def get_inexratio():
    datas = st.session_state.commun_indicators

    # !!! TO BE UPDATED !!!
    output = {}
    output["mean"]  = ""
    output["min"]   = ""
    output["max"]   = ""
    output["rest"]  = ""
    output["high"]  = ""

    if len(datas) > 0 and datas["breath"]["ratio_in_exhale"] is not None:
        output["mean"]  = datas["breath"]["ratio_in_exhale"]
        output["min"]   = 500
        output["max"]   = 500
        output["rest"]  = 500
        output["high"]  = 500
    
    return output


def get_bradycardia():
    datas = st.session_state.chronolife_indicators

    # !!! TO BE UPDATED !!!
    output = {}
    output["exists"]      = ""
    output["mean"]        = ""
    output["duration"]    = ""
    output["percentage"]  = ""
    
    if len(datas["anomalies"]["bradycardia"]["values"]) > 0:
        values = datas["anomalies"]["bradycardia"]["values"]
        output["exists"]      = datas["anomalies"]["bradycardia"]["exists"]
        output["mean"]        = round(np.mean(values))
        output["duration"]    = 500
        output["percentage"]  = 500
    
    if output["exists"]:
        bradycardia_alert_icon = st.session_state.alert
    else:
        bradycardia_alert_icon = st.session_state.alert_no
    st.session_state.bradycardia_alert_icon = bradycardia_alert_icon
    
    return output

def get_bradypnea():
    datas = st.session_state.chronolife_indicators

    # !!! TO BE UPDATED !!!
    output = {}
    output["exists"]      = ""
    output["mean"]        = ""
    output["duration"]    = ""
    output["percentage"]  = ""

    if len(datas["anomalies"]["bradypnea"]["values"]) > 0:
        values = datas["anomalies"]["bradypnea"]["values"]
        output["exists"]      = datas["anomalies"]["bradypnea"]["exists"]
        output["mean"]        = round(np.mean(values))
        output["duration"]    = 500
        output["percentage"]  = 500
    
    if output["exists"]:
        bradycardia_alert_icon = st.session_state.alert
    else:
        bradycardia_alert_icon = st.session_state.alert_no
    st.session_state.bradycardia_alert_icon = bradycardia_alert_icon
    
    return output
    
def get_tachypnea():
    datas = st.session_state.chronolife_indicators

    # !!! TO BE UPDATED !!!
    output = {}
    output["exists"]      = ""
    output["mean"]        = ""
    output["duration"]    = ""
    output["percentage"]  = ""

    if len(datas["anomalies"]["tachypnea"]["values"]) > 0:
        values = datas["anomalies"]["tachypnea"]["values"]
        output["exists"]      = datas["anomalies"]["tachypnea"]["exists"]
        output["mean"]        = round(np.mean(values))
        output["duration"]    = 500
        output["percentage"]  = 500
    
    if output["exists"]:
        tachycardia_alert_icon = st.session_state.alert
    else:
        tachycardia_alert_icon = st.session_state.alert_no
    st.session_state.tachycardia_alert_icon = tachycardia_alert_icon
    
    return output

def get_myendusers():
    
    username    = st.session_state.username
    api_key     = st.session_state.api_key
    url_user    = st.session_state.url_user
    url = url_user + "/{userId}".format(userId=username)

    reply = requests.get(url, headers={"X-API-Key": api_key})
    message, status_code = test.api_status(reply)
    
    myendusers = []
    if status_code == 200:
        myendusers = json.loads(reply.text) 
        myendusers = myendusers['users']
        myendusers_new = []
        for myenduser in myendusers:
            try:
                if isinstance(int(myenduser[0]), int):
                    myendusers_new.append(myenduser)
            except:
                pass
        myendusers = myendusers_new
    
    st.session_state.myendusers = myendusers
    
    return message, status_code
    
def get_sessions(end_user, year, month):
    
    translate = st.session_state.translate
    
    url         = st.session_state.url_data
    api_key     = st.session_state.api_key

    year = str(year)     
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    from_date = year + "-" + month
    to_date = np.datetime64(from_date) + np.timedelta64(1, 'M')
    to_date = np.datetime64(str(to_date) + "-01") - np.timedelta64(1, 'D')
    from_date += "-01"
    to_date = str(to_date)
        
    # %
    days_s                  = []
    starts_s                = []
    ends_s                  = []
    durations_s             = []
    heartbeat_qualitys_s    = []
    user_ids_s              = []

    types           = 'heartbeat_quality_index'
    
    from_date64 = np.datetime64(from_date) 
    to_date64   = np.datetime64(to_date) 
    dates       = np.arange(from_date64, to_date64 + np.timedelta64(1, 'D'))
    
    days                = []
    starts              = []
    ends                = []
    durations           = []
    heartbeat_qualitys  = []
    
    for it, date in enumerate(dates):
        
        # day
        params = {
               'user':      end_user, # sub-user username
               'types':     "heartbeat_quality_index", 
               'date':      date,
             }
        
        # Perform the POST request authenticated with YOUR API key (NOT the one of the sub-user!).
        reply = requests.get(url, headers={"X-API-Key": api_key}, params=params)
        message, status_code = test.api_status(reply)
        datas = []
        if status_code == 200:
            json_list_of_records = json.loads(reply.text) 
            for record in json_list_of_records:
                datas.append(record)

        if len(datas) > 0:
            
            results_mapped          = map_results(datas, types)
            heartbeat_quality_info  = get_result_info(datas=results_mapped, result_type='heartbeat_quality_index')
            
            hrq                     = unwrap(heartbeat_quality_info['values'])
            times                   = unwrap(heartbeat_quality_info['times'])
            
            array                   = np.array([times, hrq])
            df                      = pd.DataFrame(array.T, columns=['times', 'hrq'])
            df                      = df.sort_values(by='times')
            
            if len(df) == 0:
                continue
            
            timestamps              = df['times'].values.astype('datetime64[s]')
            hrqs                    = df['hrq'].values.astype('float')
            tdiff                   = (timestamps[1:] - timestamps[:-1])/np.timedelta64(1, 's')
            idiff                   = np.where(tdiff > 30*60)
            if len(idiff) > 0:
                idiff = idiff[0]+1
                timestamps_s    = np.split(timestamps, idiff)
                hrqs_s          = np.split(hrqs, idiff)
            else:
                timestamps_s    = timestamps
                hrqs_s          = hrqs
            if len(timestamps_s[0]) == 0:
                continue
                
            for i in range(len(timestamps_s)):
                timestamps              = timestamps_s[i]
                hrq                     = hrqs_s[i]
                start                   = timestamps[0]
                end                     = timestamps[-1]
    
                minutes_total           = (end - start)/np.timedelta64(1, 'm')
                hours                   = int(minutes_total/60)
                minutes                 = int((minutes_total/60 - hours)*60)
                duration                = str(hours) + ':' + str(minutes)
                
                hrq_mean                = int(round(sum(hrq)/len(hrq)*100))
                
                if duration == '0:0':
                    continue
                
                days.append(str(date))
                starts.append(str(start)[11:-3])
                ends.append(str(end)[11:-3])
                durations.append(duration)
                heartbeat_qualitys.append(hrq_mean)
    
    user_ids_s.extend(np.repeat(end_user, len(days)))
    days_s.extend(days)
    starts_s.extend(starts)
    ends_s.extend(ends)
    durations_s.extend(durations)
    heartbeat_qualitys_s.extend(heartbeat_qualitys)

    # %
    data    = [user_ids_s, days_s, starts_s, ends_s, durations_s]
    columns = [translate["enduser_id"], translate["date"], translate["start"], translate["stop"], translate["duration"]]

    df = pd.DataFrame(np.array(data).T, columns=columns)
    
    return df

def td_to_hhmm_str(td_seconds):
   
    sign = ''
    tdhours, rem = divmod(td_seconds, 3600)
    tdminutes, rem = divmod(rem, 60)
    tdstr = '{}{:}h {:02d}m'.format(sign, int(tdhours), int(tdminutes))
    return tdstr