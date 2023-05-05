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
from data.api2_get_cst_data import get_cst_data
from data.api2_get_garmin_data import get_garmin_data

# from template.data.generate_pdf import generate_pdf
from data.garmin_data_for_pdf import garmin_data_for_pdf
from data.cst_data_for_pdf import cst_data_for_pdf
from data.commun_data_for_pdf import commun_data_for_pdf
from data.plot_images import plot_images


def get_health_indicators():
    
    end_user    = st.session_state.end_user
    date        = st.session_state.date
    prod        = st.session_state.prod
    
    # Start timer    
    user_id_cst = "7k6Hs3"
    date_cst = "2022-09-09"
    begin = time.time()

    cst_data = get_cst_data(
        user_id = end_user, 
        date    = date,
        prod    = prod
        )

    # Time intervals
    cst_time_intervals = cst_data['duration']['collected']
    # Alerts
    alerts_dict = cst_data['anomalies']

    # End timer
    end = time.time()
    print('Time taken to get CST data:',round((end-begin)/60,2),'min')

    # ----------------------------- Garmin -----------------------------------
    # Start timer    
    begin = time.time()
    user_id_garmin = "6o2Fzp" 
    date_garmin = '2023-05-02'

    garmin_data = get_garmin_data(
        user_id = end_user, 
        date = date,
        prod = prod
        )

    # Time intervals
    garmin_time_intervals = garmin_data['duration']['collected']

    # End timer
    end = time.time()
    print('Time taken to get Garmin data:',round((end-begin)/60,2),'min')

    # % -------------------------- Construct PDF --------------------------------
    # Format CST's text that will be added to pdf 
    cst_data_pdf = cst_data_for_pdf(user_id_cst, date_cst, cst_data)

    # Format Garmin's text that will be added to pdf 
    garmin_data_pdf = garmin_data_for_pdf(garmin_data)

    # %
    # Compute commun indicators: cardio, respiration and steps
    commun_data, commun_data_pdf, steps_dict = commun_data_for_pdf(cst_data, garmin_data) 

    # Plot and save graphs
    plot_images(garmin_data, steps_dict, cst_time_intervals, 
                garmin_time_intervals, date_cst)
    
    st.session_state.garmin_indicators      = garmin_data
    st.session_state.chronolife_indicators  = cst_data
    st.session_state.commun_indicators      = commun_data
    
    
def get_bodybattery():
    
    datas = st.session_state.garmin_indicators
    
    output = {}
    
    output["high"]  = ""
    output["low"]   = ""
    
    if datas["body_battery"]["highest"] is not None:
        output["high"]  = datas["body_battery"]["highest"]
        output["low"]   = datas["body_battery"]["lowest"]
    
    return output

def get_calories():
    
    datas = st.session_state.garmin_indicators
    
    output = {}
    
    output["total"]    = ""
    output["rest"]     = ""
    output["active"]   = ""
    
    if datas["calories"]["total"] is not None:
        output["total"]    = datas["calories"]["total"]
        output["rest"]     = datas["calories"]["resting"]
        output["active"]   = datas["calories"]["active"]
    
    return output

def get_intensity():
    
    datas = st.session_state.garmin_indicators
    
    output = {}
    output["total"]       = ""
    output["moderate"]    = ""
    output["vigurous"]    = ""
    
    if datas["intensity_min"]["total"] is not None:
        output["total"]       = datas["intensity_min"]["total"]
        output["moderate"]    = datas["intensity_min"]["moderate"]
        output["vigurous"]    = datas["intensity_min"]["vigurous"]
    
    return output

def get_sleep():
    
    datas = st.session_state.garmin_indicators
    
    output = {}
        
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
    
    if datas["sleep"]["score"] is not None:
        output["score"]             = datas["sleep"]["score"]
        output["quality"]           = datas["sleep"]["quality"]
        output["duration"]          = datas["sleep"]["recorded_time"]
        output["duration_deep"]     = int(round(datas["sleep"]["deep"]/60))
        output["duration_light"]    = int(round(datas["sleep"]["light"]/60))
        output["duration_rem"]      = int(round(datas["sleep"]["rem"]/60))
        output["duration_awake"]    = int(round(datas["sleep"]["awake"]/60))
        
        output["percentage_deep"]   = int(round(datas["sleep"]["light"]/datas["sleep"]["recorded_time"]*100))
        output["percentage_light"]  = int(round(datas["sleep"]["deep"]/datas["sleep"]["recorded_time"]*100))
        output["percentage_rem"]    = int(round(datas["sleep"]["rem"]/datas["sleep"]["recorded_time"]*100))
        output["percentage_awake"]  = int(round(datas["sleep"]["awake"]/datas["sleep"]["recorded_time"]*100))
    
    return output

def get_spo2():
    
    datas = st.session_state.garmin_indicators
    
    output = {}
    output["mean"]      = ""
    output["min"]       = ""
    output["values"]    = ""
    
    if datas["spo2"]["averege"] is not None:
        output["mean"]      = datas["spo2"]["averege"]
        output["min"]       = datas["spo2"]["lowest"]
        output["values"]    = datas["spo2"]["all_values"]
    
    return output

def get_stress():
    
    datas = st.session_state.garmin_indicators
    
    output = {}
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
    
    if datas["stress"]["score"] is not None:
        output["score"]             = datas["stress"]["score"]
        output["duration"]          = datas["stress"]["recorded_time"]
        output["duration_rest"]     = int(round(datas["stress"]["rest"]/60))
        output["duration_low"]      = int(round(datas["stress"]["low"]/60))
        output["duration_medium"]   = int(round(datas["stress"]["medium"]/60))
        output["duration_high"]     = int(round(datas["stress"]["high"]/60))
        
        output["percentage_rest"]   = int(round(datas["stress"]["rest"]/datas["stress"]["recorded_time"]*100))
        output["percentage_low"]    = int(round(datas["stress"]["low"]/datas["stress"]["recorded_time"]*100))
        output["percentage_medium"] = int(round(datas["stress"]["medium"]/datas["stress"]["recorded_time"]*100))
        output["percentage_high"]   = int(round(datas["stress"]["high"]/datas["stress"]["recorded_time"]*100))
        
    
    return output

def get_duration_chronolife():
    
    # !!! TO BE UPDATED !!!
    output = {}
    
    # output["duration"]          = ""
    # output["duration_day"]      = ""
    # output["duration_night"]    = ""
    # output["duration_rest"]     = "" 
    # output["duration_activity"] = ""
    
    output["duration"]          = 17
    output["duration_day"]      = 12
    output["duration_night"]    = 5
    output["duration_rest"]     = 16 
    output["duration_activity"] = 1
    
    return output

def get_duration_garmin():
    
    # !!! TO BE UPDATED !!!
    output = {}
    # output["duration"]          = ""
    # output["duration_day"]      = ""
    # output["duration_night"]    = ""
    # output["duration_rest"]     = "" 
    # output["duration_activity"] = ""
    
    output["duration"]          = 2
    output["duration_day"]      = 16
    output["duration_night"]    = 6
    output["duration_rest"]     = 16 
    output["duration_activity"] = 6
    
    return output    

def get_steps():
    
    # !!! TO BE UPDATED !!!
    output = {}
    
    # output["number"]    = ""
    # output["goal"]      = ""
    # output["score"]     = ""
    # output["distance"]  = ""
    
    output["number"]    = 1654
    output["goal"]      = 6955
    output["score"]     = int(output["number"]/output["goal"]*100)
    output["distance"]  = 4.2
    
    return output

def get_temperature():
    
    # !!! TO BE UPDATED !!!
    output = {}
    output["mean"]  = ""
    output["min"]   = ""
    output["max"]   = ""
    
    output["mean"]  = 35.4
    output["min"]   = 33.4
    output["max"]   = 37.1
    
    return output

def get_bpm():
    
    # !!! TO BE UPDATED !!!
    output = {}
    
    # output["mean"]  = ""
    # output["min"]   = ""
    # output["max"]   = ""
    # output["rest"]  = ""
    # output["high"]  = ""
    
    output["mean"]  = 67
    output["min"]   = 59
    output["max"]   = 123
    output["rest"]  = 65
    output["high"]  = 156
    
    return output

def get_hrv():
    
    # !!! TO BE UPDATED !!!
    output = {}
    # output["mean"]  = ""
    # output["min"]   = ""
    # output["max"]   = ""
    # output["rest"]  = ""
    # output["high"]  = ""
    
    output["mean"]  = 162
    output["min"]   = 42
    output["max"]   = 555
    output["rest"]  = 150
    output["high"]  = 111
    
    return output

def get_qt():
    
    # !!! TO BE UPDATED !!!
    output = {}
    # output["mean"]      = ""
    # output["min"]       = ""
    # output["max"]       = ""
    # output["rest"]      = ""
    # output["high"]      = ""
    # output["threshold"] = ""
    
    output["mean"]      = 50
    output["min"]       = 817
    output["max"]       = 324
    output["rest"]      = 324
    output["high"]      = 324
    output["threshold"] = 550
    
    if output["mean"] > output["threshold"]:
        qt_alert_icon = st.session_state.alert
    else:
        qt_alert_icon = st.session_state.alert_no
    st.session_state.qt_alert_icon          = qt_alert_icon
    
    return output

def get_bradycardia():
    
    # !!! TO BE UPDATED !!!
    output = {}
    # output["exists"]      = ""
    # output["mean"]        = ""
    # output["duration"]    = ""
    # output["percentage"]  = ""
    
    output["exists"]      = False
    output["mean"]        = 0
    output["duration"]    = 0
    output["percentage"]  = 0
    
    if output["exists"]:
        bradycardia_alert_icon = st.session_state.alert
    else:
        bradycardia_alert_icon = st.session_state.alert_no
    st.session_state.bradycardia_alert_icon = bradycardia_alert_icon
    
    return output
    
def get_tachycardia():
    
    # !!! TO BE UPDATED !!!
    output = {}
    # output["exists"]      = ""
    # output["mean"]        = ""
    # output["duration"]    = ""
    # output["percentage"]  = ""
    output["exists"]      = False
    output["mean"]        = 0
    output["duration"]    = 0
    output["percentage"]  = 0
    
    if output["exists"]:
        tachycardia_alert_icon = st.session_state.alert
    else:
        tachycardia_alert_icon = st.session_state.alert_no
    st.session_state.tachycardia_alert_icon = tachycardia_alert_icon
    
    return output

def get_brpm():
    
    # !!! TO BE UPDATED !!!
    output = {}
    # output["mean"]  = ""
    # output["min"]   = ""
    # output["max"]   = ""
    # output["rest"]  = ""
    # output["high"]  = ""
    
    output["mean"]  = 15
    output["min"]   = 9
    output["max"]   = 21
    output["rest"]  = 12
    output["high"]  = 22
    
    return output

def get_brv():
    
    # !!! TO BE UPDATED !!!
    output = {}
    # output["mean"]  = ""
    # output["min"]   = ""
    # output["max"]   = ""
    # output["rest"]  = ""
    # output["high"]  = ""
    output["mean"]  = 1.2
    output["min"]   = 0.2
    output["max"]   = 2.0
    output["rest"]  = 1.3
    output["high"]  = 1.8
    
    return output

def get_inexratio():
    
    # !!! TO BE UPDATED !!!
    output = {}
    # output["mean"]  = ""
    # output["min"]   = ""
    # output["max"]   = ""
    # output["rest"]  = ""
    # output["high"]  = ""
    output["mean"]  = 1.5
    output["min"]   = 1.2
    output["max"]   = 2.1
    output["rest"]  = 1.3
    output["high"]  = 2.3
    
    return output

def get_bradypnea():
    
    # !!! TO BE UPDATED !!!
    output = {}
    # output["exists"]      = ""
    # output["mean"]        = ""
    # output["duration"]    = ""
    # output["percentage"]  = ""
    output["exists"]      = True
    output["mean"]        = 0
    output["duration"]    = 0
    output["percentage"]  = 0
    
    if output["exists"]:
        bradycardia_alert_icon = st.session_state.alert
    else:
        bradycardia_alert_icon = st.session_state.alert_no
    st.session_state.bradycardia_alert_icon = bradycardia_alert_icon
    
    return output
    
def get_tachypnea():
    
    # !!! TO BE UPDATED !!!
    output = {}
    # output["exists"]      = ""
    # output["mean"]        = ""
    # output["duration"]    = ""
    # output["percentage"]  = ""
    output["exists"]       = True
    output["mean"]        = 0
    output["duration"]    = 0
    output["percentage"]  = 0
    
    if output["exists"]:
        tachycardia_alert_icon = st.session_state.alert
    else:
        tachycardia_alert_icon = st.session_state.alert_no
    st.session_state.tachycardia_alert_icon = tachycardia_alert_icon
    
    return output

# @st.cache
def convert_data_to_excel(data_acc, data_breath, data_ecg, data_temp):
    # !!! TO BE UPDATED !!!
    # Cache the conversion to prevent computation on every rerun
    indicators = st.session_state.indicators.copy()
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data_acc.to_excel(writer, index=False, sheet_name='Acceleration')
    data_breath.to_excel(writer, index=False, sheet_name='Breath')
    data_ecg.to_excel(writer, index=False, sheet_name='ECG')
    data_temp.to_excel(writer, index=False, sheet_name='Skin Temperature')
    if indicators is not None:
        indicators = indicators.drop(columns=['sma_values'])
        indicators.to_excel(writer, index=False, sheet_name='Indicators')
    workbook = writer.book
    worksheet = writer.sheets['Acceleration']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

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
    
    """
    """
    
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
