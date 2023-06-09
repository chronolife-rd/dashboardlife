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
from automatic_reports.api2_get_cst_data import get_cst_data
from automatic_reports.api2_get_garmin_data import get_garmin_data
from automatic_reports.compute_common_for_html import get_common_indicators
from automatic_reports.compute_common_for_pdf import get_common_indicators_pdf
from automatic_reports.compute_cst_for_pdf import cst_data_for_pdf
from automatic_reports.compute_garmin_for_pdf import garmin_data_for_pdf
from automatic_reports.useful_functions import combine_data

def get_health_indicators():
    
    end_user    = st.session_state.end_user
    date        = st.session_state.date
    api         = st.session_state.api_key 
    url_cst     = st.session_state.url_data 
    url_garmin  = st.session_state.url_garmin
    
    garmin_data = []
    cst_data    = []
    common_data = []

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
    
    # Compute common data 
    common_data = combine_data(cst_data, garmin_data)

    # Compute common indicators for html
    common_indicators = get_common_indicators(common_data) 

    # Compute common indicators for pdf
    common_indicators_pdf = get_common_indicators_pdf(common_data) 

    # Format CST's text that will be added to pdf 
    chronolife_indicators_pdf = cst_data_for_pdf(end_user, date, cst_data)

    # Format Garmin's text that will be added to pdf 
    garmin_indicators_pdf = garmin_data_for_pdf(garmin_data)

    st.session_state.garmin_indicators          = garmin_data
    st.session_state.chronolife_indicators      = cst_data
    st.session_state.common_data                = common_data             
    st.session_state.common_indicators          = common_indicators       
    st.session_state.common_indicators_pdf      = common_indicators_pdf   
    st.session_state.garmin_indicators_pdf      = garmin_indicators_pdf   
    st.session_state.chronolife_indicators_pdf  = chronolife_indicators_pdf     

def get_offset():
    datas = st.session_state.chronolife_indicators

    output = {}
    output["value"] = ""
    output["sign"] = ""

    if len(datas) > 0  and isinstance(datas["offset"], str) == False:
        offset = datas["offset"]
        sign = 1
        if offset>=0:
            sign = 1
        elif offset<0:
            sign = -1 

        output["value"] = abs(offset)
        output["sign"]  = sign
    
    return output

def get_bodybattery():
    datas = st.session_state.garmin_indicators

    output = {}
    output["values"] = ""
    output["high"]   = ""
    output["low"]    = ""
    
    if len(datas) > 0 and isinstance(datas["body_battery"]["highest"], str) == False:
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
    
    if len(datas) > 0 and isinstance(datas["calories"]["total"], str) == False:
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
    
    if len(datas) > 0 and isinstance(datas["intensity_min"]["total"], str) == False:
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
    
    if isinstance(datas["sleep"]["score"], str) == False and datas["sleep"]["recorded_time"]>0:
        output["values"]            = datas["sleep"]["sleep_map"]
        output["score"]             = datas["sleep"]["score"]
        output["quality"]           = datas["sleep"]["quality"]
        output["duration"]          = datas["sleep"]["recorded_time"]
        output["duration_deep"]     = td_to_hhmm_str(datas["sleep"]["deep"])
        output["duration_light"]    = td_to_hhmm_str(datas["sleep"]["light"])
        output["duration_rem"]      = td_to_hhmm_str(datas["sleep"]["rem"])
        output["duration_awake"]    = td_to_hhmm_str(datas["sleep"]["awake"])

        output["percentage_deep"]   = datas["sleep"]["percentage_deep"]
        output["percentage_light"]  = datas["sleep"]["percentage_light"]
        output["percentage_rem"]    = datas["sleep"]["percentage_rem"]
        output["percentage_awake"]  = datas["sleep"]["percentage_awake"]

    return output

def get_spo2():
    datas = st.session_state.garmin_indicators
    
    output = {}
    output["mean"]    = ""
    output["min"]     = ""
    output["values"]  = ""
    
    if len(datas) > 0 and isinstance(datas["spo2"]["averege"], str) == False:
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
    
    if len(datas) > 0 and isinstance(datas["stress"]["recorded_time"], str) == False:
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
    output["intervals"]         = ""
    output["duration"]          = ""
    output["duration_day"]      = ""
    output["duration_night"]    = ""
    output["duration_rest"]     = "" 
    output["duration_activity"] = ""
    
    if len(datas) > 0 :
        output["intervals"]         = datas["duration"]["intervals"] 
        output["duration"]          = datas["duration"]["collected"] 
        output["duration_day"]      = datas["duration"]["day"]
        output["duration_night"]    = datas["duration"]["night"] 
        output["duration_rest"]     = datas["duration"]["rest"] 
        output["duration_activity"] = datas["duration"]["active"] 

    return output

def get_duration_garmin():
    datas = st.session_state.garmin_indicators

    output = {}    
    output["intervals"]         = ""
    output["duration"]          = ""
    output["duration_day"]      = ""
    output["duration_night"]    = ""
    output["duration_rest"]     = "" 
    output["duration_activity"] = ""
    
    if len(datas) > 0 :
        output["intervals"]         = datas["duration"]["intervals"] 
        output["duration"]          = datas["duration"]["collected"] 
        output["duration_day"]      = datas["duration"]["day"]
        output["duration_night"]    = datas["duration"]["night"] 
        output["duration_rest"]     = datas["duration"]["rest"] 
        output["duration_activity"] = datas["duration"]["active"] 
    
    return output    

def get_steps():
    datas = st.session_state.common_indicators
  
    output = {}
    output["number"]    = ""
    output["goal"]      = 3000
    output["score"]     = ""
    output["distance"]  = ""

    if len(datas) > 0 and isinstance(datas["activity"]["distance"], str) == False:
        output["number"]    = datas["activity"]["steps"] 
        output["goal"]      = datas["activity"]["goal"] 
        output["distance"]  = datas["activity"]["distance"] 
        output["score"] = int(output["number"]/output["goal"]*100)

    return output

def get_temperature():
    datas = st.session_state.chronolife_indicators
    output = {}
    output["mean"]   = ""
    output["min"]    = ""
    output["max"]    = ""
    output["values"] = ""
    
    if len(datas) > 0 and isinstance(datas["temperature"]["mean"], str) == False:
        output["values"] = datas["temperature"]["values"]
        output["mean"]   = datas["temperature"]["mean"]
        output["min"]    = datas["temperature"]["min"]
        output["max"]    = datas["temperature"]["max"]

    return output

def get_bpm():
    datas = st.session_state.common_indicators
    output = {}
    output["values"]  = ""
    output["mean"]    = ""
    output["min"]     = ""
    output["max"]     = ""
    output["rest"]    = ""
    output["high"]    = ""
    
    if len(datas) > 0 and isinstance(datas["cardio"]["rate_high"], str) == False:
        output["values"]  = datas["cardio"]["rate_mean"] 
        output["mean"]    = datas["cardio"]["rate_mean"] 
        output["min"]     = datas["cardio"]["rate_min"] 
        output["max"]     = datas["cardio"]["rate_max"] 
        output["rest"]    = datas["cardio"]["rate_resting"] 
        output["high"]    = datas["cardio"]["rate_high"] 
    
    return output

def get_bpm_values():
    datas = st.session_state.common_data
    output = []
    if isinstance(datas["cardio"]["rate"], str) == False:
        output = datas["cardio"]["rate"] 

    return output

def get_hrv_values():
    datas = st.session_state.common_data
    output = []
    if isinstance(datas["cardio"]["rate_var"], str) == False:
        output = datas["cardio"]["rate_var"] 
    st.session_state.hrv_values = output
    return output

def get_brpm_values():
    datas = st.session_state.common_data
    output = []
    if isinstance(datas["breath"]["rate"], str) == False:
        output = datas["breath"]["rate"] 
    st.session_state.brpm_values = output
    return output

def get_inex_values():
    datas = st.session_state.common_data
    output = []
    if isinstance(datas["breath"]["inspi_expi"], str) == False:
        output = datas["breath"]["inspi_expi"] 
    st.session_state.inex_values = output
    return output



def get_brv_values():
    datas = st.session_state.common_data
    output = []
    if isinstance(datas["breath"]["rate_var"], str) == False:
        output = datas["breath"]["rate_var"] 
    st.session_state.brv_values = output
    return output

def get_hrv():
    datas = st.session_state.common_indicators
    output = {}
    output["mean"]  = ""
    output["min"]   = ""
    output["max"]   = ""
    output["rest"]  = ""
    output["high"]  = ""

    if len(datas) > 0 and isinstance(datas["cardio"]["rate_var_resting"], str) == False:
        output["mean"]  = datas["cardio"]["rate_var_mean"] 
        output["min"]   = datas["cardio"]["rate_var_min"] 
        output["max"]   = datas["cardio"]["rate_var_max"] 
        output["rest"]  = datas["cardio"]["rate_var_resting"] 
        output["high"]  = datas["cardio"]["rate_var_high"] 
    
    return output

def get_qt():
    datas = st.session_state.chronolife_indicators
    
    output = {}
    output["exists"]  = False
    output["values"]  = ""
    output["night"]    = ""
    output["morning"]     = ""
    output["evening"]     = ""
    
    if isinstance(datas["anomalies"]["qt"]["values"], str) == False:
        output["exists"] = datas["anomalies"]["qt"]["exists"]
        output["night"]   = datas["anomalies"]["qt"]["night"]
        output["morning"]    = datas["anomalies"]["qt"]["morning"]
        output["evening"]    = datas["anomalies"]["qt"]["evening"]
    
    if output["exists"]:
        qt_alert_icon = st.session_state.alert
    else:
        qt_alert_icon = st.session_state.alert_no
    st.session_state.qt_alert_icon = qt_alert_icon
    
    return output

def get_bradycardia():
    datas = st.session_state.chronolife_indicators
    output = {}
    output["exists"]      = ""
    output["mean"]        = ""
    output["duration"]    = ""
    output["percentage"]  = ""
    
    if isinstance(datas["anomalies"]["bradycardia"]["values"], str) == False:
        output["exists"]      = datas["anomalies"]["bradycardia"]["exists"]
        output["mean"]        = datas["anomalies"]["bradycardia"]["mean"]
        output["duration"]    = datas["anomalies"]["bradycardia"]["duration"]
        output["percentage"]  = datas["anomalies"]["bradycardia"]["percentage"]
    
    if output["exists"]:
        bradycardia_alert_icon = st.session_state.alert
    else:
        bradycardia_alert_icon = st.session_state.alert_no
    st.session_state.bradycardia_alert_icon = bradycardia_alert_icon
    
    return output
    
def get_tachycardia():
    datas = st.session_state.chronolife_indicators
    output = {}
    output["exists"]      = ""
    output["mean"]        = ""
    output["duration"]    = ""
    output["percentage"]  = ""

    if isinstance(datas["anomalies"]["tachycardia"]["values"], str) == False:
        output["exists"]      = datas["anomalies"]["tachycardia"]["exists"]
        output["mean"]        = datas["anomalies"]["tachycardia"]["mean"]
        output["duration"]    = datas["anomalies"]["tachycardia"]["duration"]
        output["percentage"]  = datas["anomalies"]["tachycardia"]["percentage"]
    
    if output["exists"]:
        tachycardia_alert_icon = st.session_state.alert
    else:
        tachycardia_alert_icon = st.session_state.alert_no
    st.session_state.tachycardia_alert_icon = tachycardia_alert_icon
    
    return output

def get_brpm():
    datas = st.session_state.common_indicators

    output = {}
    output["mean"]  = ""
    output["min"]   = ""
    output["max"]   = ""
    output["rest"]  = ""
    output["high"]  = ""
    
    if len(datas) > 0 and isinstance(datas["breath"]["rate_high"], str) == False:
        output["mean"]  = datas["breath"]["rate_mean"] 
        output["min"]   = datas["breath"]["rate_min"] 
        output["max"]   = datas["breath"]["rate_max"] 
        output["rest"]  = datas["breath"]["rate_resting"] 
        output["high"]  = datas["breath"]["rate_high"] 
    
    return output

def get_brv():
    datas = st.session_state.common_indicators

    output = {}
    output["mean"]  = ""
    output["min"]   = ""
    output["max"]   = ""
    output["rest"]  = ""
    output["high"]  = ""

    if len(datas) > 0 and isinstance(datas["breath"]["rate_var_resting"], str) == False:
        output["mean"]  = datas["breath"]["rate_var_mean"]
        output["min"]   = datas["breath"]["rate_var_min"]
        output["max"]   = datas["breath"]["rate_var_max"]
        output["rest"]  = datas["breath"]["rate_var_resting"]
        output["high"]  = datas["breath"]["rate_var_high"]
    
    return output

def get_inexratio():
    datas = st.session_state.common_indicators
    common_data = st.session_state.common_data

    output = {}
    output["values"] = ""
    output["mean"]   = ""
    output["min"]    = ""
    output["max"]    = ""

    if len(datas) > 0 and isinstance(datas["breath"]["inspi_expi_mean"], str) == False:
        
        output["values"] = common_data["breath"]["inspi_expi"]
        output["mean"]   = datas["breath"]["inspi_expi_mean"]
        output["min"]    = datas["breath"]["inspi_expi_min"]
        output["max"]    = datas["breath"]["inspi_expi_max"]     
    return output

def get_bradypnea():
    datas = st.session_state.chronolife_indicators

    output = {}
    output["exists"]      = ""
    output["mean"]        = ""
    output["duration"]    = ""
    output["percentage"]  = ""

    if isinstance(datas["anomalies"]["bradypnea"]["values"], str) == False:
        output["exists"]      = datas["anomalies"]["bradypnea"]["exists"]
        output["mean"]        = datas["anomalies"]["bradypnea"]["mean"]
        output["duration"]    = datas["anomalies"]["bradypnea"]["duration"]
        output["percentage"]  = datas["anomalies"]["bradypnea"]["percentage"]
    
    if output["exists"]:
        bradypnea_alert_icon = st.session_state.alert
    else:
        bradypnea_alert_icon = st.session_state.alert_no
    st.session_state.bradypnea_alert_icon = bradypnea_alert_icon
    
    return output
    
def get_tachypnea():
    datas = st.session_state.chronolife_indicators

    output = {}
    output["exists"]      = ""
    output["mean"]        = ""
    output["duration"]    = ""
    output["percentage"]  = ""

    if isinstance(datas["anomalies"]["tachypnea"]["values"], str) == False:
        output["exists"]      = datas["anomalies"]["tachypnea"]["exists"]
        output["mean"]        = datas["anomalies"]["tachypnea"]["mean"]
        output["duration"]    = datas["anomalies"]["tachypnea"]["duration"]
        output["percentage"]  = datas["anomalies"]["tachypnea"]["percentage"]
    
    if output["exists"]:
        tachypnea_alert_icon = st.session_state.alert
    else:
        tachypnea_alert_icon = st.session_state.alert_no
    st.session_state.tachypnea_alert_icon = tachypnea_alert_icon
    
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
