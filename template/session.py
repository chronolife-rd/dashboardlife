import streamlit as st
from template.util import img_to_bytes

def init():
    if 'username' not in st.session_state:
        st.session_state.username = ''
        
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ''
        
    if 'myendusers' not in st.session_state:
        st.session_state.myendusers = ''

    if 'date' not in st.session_state:
            st.session_state.date = ''
            
    if 'start_time' not in st.session_state:
            st.session_state.start_time = ''
            
    if 'end_time' not in st.session_state:
            st.session_state.end_time = ''
            
    if 'end_user' not in st.session_state:
            st.session_state.end_user = ''
            
    if 'timezone' not in st.session_state:
            st.session_state.timezone = ''
            
    if 'enduser_sessions' not in st.session_state:
            st.session_state.enduser_sessions = ''
    
            
    if 'form_indicators_layout' not in st.session_state:
            st.session_state.form_indicators_layout = ''
            
    if 'form_indicators_submit' not in st.session_state:
            st.session_state.form_indicators_submit = False
            
    if 'form_raw_layout' not in st.session_state:
            st.session_state.form_raw_layout = False
            
    if 'form_raw_submit' not in st.session_state:
            st.session_state.form_raw_submit = False
            
    if 'is_logged' not in st.session_state:
            st.session_state.is_logged = False
    
    if 'logout_submit' not in st.session_state:
            st.session_state.logout_submit = False
            
    if 'is_data' not in st.session_state:
            st.session_state.is_data = False

    # if 'count' not in st.session_state:
    #         st.session_state.count = 0
        
    if 'al' not in st.session_state:
            st.session_state.al = None
    
    if 'indicators' not in st.session_state:
            st.session_state.indicators = None
            
    if 'end_users_list' not in st.session_state:
            st.session_state.end_users_list = None
            
    if 'all_end_users_sessions' not in st.session_state:
            st.session_state.all_end_users_sessions = None
            
    if 'end_user_sessions' not in st.session_state:
            st.session_state.end_user_sessions = None
            
    if 'end_user_sessions_run' not in st.session_state:
            st.session_state.end_user_sessions_run = False
            
    if 'tachycardia_alert_icon' not in st.session_state:
            st.session_state.tachycardia_alert_icon = None
            
    if 'bradycardia_alert_icon' not in st.session_state:
            st.session_state.bradycardia_alert_icon = None
            
    if 'qt_alert_icon' not in st.session_state:
            st.session_state.qt_alert_icon = None
            
    if 'tachypnea_alert_icon' not in st.session_state:
            st.session_state.tachypnea_alert_icon = None
            
    if 'bradypnea_alert_icon' not in st.session_state:
            st.session_state.bradypnea_alert_icon = None
            
    if 'smart_textile_raw_data' not in st.session_state:
            st.session_state.smart_textile_raw_data = None
            
    if 'background_wave' not in st.session_state:
        st.session_state.background_wave = img_to_bytes('assets/background_wave.png')
            
    if 'logo_clife_white' not in st.session_state:
        st.session_state.logo_clife_white = img_to_bytes('assets/logo_clife_white.png')
    
    if 'night' not in st.session_state:
        st.session_state.night = img_to_bytes('assets/night.png')

    if 'day' not in st.session_state:
        st.session_state.day = img_to_bytes('assets/day.png')

    if 'rest' not in st.session_state:
        st.session_state.rest = img_to_bytes('assets/rest.png')

    if 'activity' not in st.session_state:
        st.session_state.activity = img_to_bytes('assets/activity.png')

    if 'tshirt_right' not in st.session_state:
        st.session_state.tshirt_right = img_to_bytes('assets/tshirt_right.png')
    
    if 'garrmin' not in st.session_state:
        st.session_state.garrmin = img_to_bytes('assets/garrmin.png')
    
    if 'alert' not in st.session_state:
        st.session_state.alert = img_to_bytes('assets/alert.png')
    
    if 'alert_no' not in st.session_state:
        st.session_state.alert_no = img_to_bytes('assets/alert_no.png')
    
    if 'heart_icon' not in st.session_state:
        st.session_state.heart_icon = img_to_bytes('assets/heart.png')
    
    if 'breath_icon' not in st.session_state:
        st.session_state.breath_icon = img_to_bytes('assets/breath.png')
    
    if 'steps_icon' not in st.session_state:
        st.session_state.steps_icon = img_to_bytes('assets/steps.png')

    if 'stress_icon' not in st.session_state:
        st.session_state.stress_icon = img_to_bytes('assets/stress.png')
    
    if 'stress_rest' not in st.session_state:
        st.session_state.stress_rest = img_to_bytes('assets/stress_rest.png')
    
    if 'stress_low' not in st.session_state:
        st.session_state.stress_low = img_to_bytes('assets/stress_low.png')
    
    if 'stress_medium' not in st.session_state:
        st.session_state.stress_medium = img_to_bytes('assets/stress_medium.png')
        
    if 'stress_high' not in st.session_state:
        st.session_state.stress_high = img_to_bytes('assets/stress_high.png')
        
    if 'pulseox_icon' not in st.session_state:
        st.session_state.pulseox_icon = img_to_bytes('assets/pulseox.png')
        
    if 'spo2_green' not in st.session_state:
        st.session_state.spo2_green = img_to_bytes('assets/spo2_green.png')

    if 'spo2_yellow' not in st.session_state:
        st.session_state.spo2_yellow = img_to_bytes('assets/spo2_yellow.png')

    if 'spo2_orange' not in st.session_state:
        st.session_state.spo2_orange = img_to_bytes('assets/spo2_orange.png')
    
    if 'spo2_red' not in st.session_state:
        st.session_state.spo2_red = img_to_bytes('assets/spo2_red.png')
        
    if 'sleep_icon' not in st.session_state:
        st.session_state.sleep_icon = img_to_bytes('assets/sleep.png')
    
    if 'sleep_deep' not in st.session_state:
        st.session_state.sleep_deep = img_to_bytes('assets/sleep_deep.png')
        
    if 'sleep_light' not in st.session_state:
        st.session_state.sleep_light = img_to_bytes('assets/sleep_light.png')    
        
    if 'sleep_rem' not in st.session_state:
        st.session_state.sleep_rem = img_to_bytes('assets/sleep_rem.png')
    
    if 'sleep_awake' not in st.session_state:
        st.session_state.sleep_awake = img_to_bytes('assets/sleep_awake.png')
        
    if 'calories_icon' not in st.session_state:
        st.session_state.calories_icon = img_to_bytes('assets/calories.png')
    
    if 'intensity_icon' not in st.session_state:
        st.session_state.intensity_icon = img_to_bytes('assets/intensity_minutes.png')
    
    if 'bodybattery_icon' not in st.session_state:
        st.session_state.bodybattery_icon = img_to_bytes('assets/body_battery.png')
        
    if 'temperature_icon' not in st.session_state:
        st.session_state.temperature_icon = img_to_bytes('assets/temperature.png')
        
    if 'to_top' not in st.session_state:
        st.session_state.to_top = img_to_bytes('assets/to_top.png')
        
    if 'stress_donut' not in st.session_state:
        st.session_state.stress_donut = None
        
    if 'spo2_donut' not in st.session_state:
        st.session_state.spo2_donut = None
        
    if 'sleep_donut' not in st.session_state:
        st.session_state.sleep_donut = None
        
    if 'steps_donut' not in st.session_state:
        st.session_state.steps_donut = None
        
    
def init_simul():
    st.session_state.tachycardia_alert_icon = st.session_state.alert
    st.session_state.bradycardia_alert_icon = st.session_state.alert
    st.session_state.qt_alert_icon = st.session_state.alert_no
    st.session_state.tachypnea_alert_icon = st.session_state.alert
    st.session_state.bradypnea_alert_icon = st.session_state.alert_no
        
def restart():
    for key in st.session_state.keys():
        del st.session_state[key]
    init()
    st.experimental_rerun()