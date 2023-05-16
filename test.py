import garmin_automatic_reports.api2_get_garmin_data as getGarminData
import garmin_automatic_reports.api2_get_cst_data as getCSTData
import data.data as indicators
import streamlit as st


# Constants
date = '2023-05-05'
user_id = "5Nwwut" 


garmin_date = '2023-05-04'
garmin_user_id = "6o2Fzp" 

garmin_output = getGarminData.get_garmin_data(garmin_user_id,garmin_date,False)
cst_data = getCSTData.get_cst_data(user_id,date,False)

cst_time_intervals = cst_data['duration']['collected']


st.json(cst_data)

print(cst_time_intervals)

