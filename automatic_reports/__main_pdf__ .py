# -*- coding: utf-8 -*-
"""
Get Chronolife data
Get Garmin data 
Complete Chronolife and Garmin data
CST = chronolife smart textile

@author: aterman
Last update: 6 April 2023  
"""
# Imports 
import time 
from api2_get_cst_data import get_cst_data
from api2_get_garmin_data import get_garmin_data

from generate_pdf import generate_pdf
from compute_garmin_for_pdf import garmin_data_for_pdf
from compute_cst_for_pdf import cst_data_for_pdf
from compute_common_for_pdf import get_common_indicators
from plot_images import plot_images

API_KEY_PROD = 'CLjfUipLb32dfMC8ZCCwUA' 
API_KEY_PREPROD = '3-1krbPQoufnmNVN6semRA'

URL_CST_PROD = "https://prod.chronolife.net/api/2/data"
URL_CST_PREPROD = "https://preprod.chronolife.net/api/2/data"
URL_GARMIN_PROD = "https://prod.chronolife.net/api/2/garmin/data" 
URL_GARMIN_PREPROD = "https://preprod.chronolife.net/api/2/garmin/data" 

# -- Adriana
user_id = "6o2Fzp"
date = "2023-05-24"

# -- Michel
# user_id = "5Nwwut" 
# date = "2023-05-04" 

# -- Laurent
# user_id = "342pv5"
# date = "2023-05-03"

# -- Ludo 
# user_id = "4vk5VJ"
# date = "2023-05-17"
# ----------------------------- Chronolife ------------------------------------
# Start timer    
begin = time.time()

cst_data = get_cst_data(
    user_id = user_id, 
    date = date,
    api = API_KEY_PREPROD,
    url = URL_CST_PREPROD
    )

# Time intervals
cst_time_intervals = cst_data['duration']['intervals']
# Alerts
alerts_dict = cst_data['anomalies']

# End timer
end = time.time()
print('Time taken to get CST data:',round((end-begin)/60,2),'min')

# ----------------------------- Garmin ----------------------------------------
# Start timer    
begin = time.time()

garmin_data = get_garmin_data(
    user_id = user_id, 
    date = date,
    api = API_KEY_PREPROD,
    url = URL_GARMIN_PREPROD
    )

# Time intervals
garmin_time_intervals = garmin_data['duration']['intervals']

# End timer
end = time.time()
print('Time taken to get Garmin data:',round((end-begin)/60,2),'min')

# ----------------------------- Common ----------------------------------------
# Compute common indicators: cardio, respiration and steps
common_data, common_data_pdf, steps_dict = get_common_indicators(cst_data, garmin_data) 

# Plot and save graphs
plot_images(garmin_data, steps_dict, cst_time_intervals, 
            garmin_time_intervals, date)

# %% -------------------------- Construct PDF ---------------------------------
# Format CST's text that will be added to pdf 
cst_data_pdf = cst_data_for_pdf(user_id, date, cst_data)

# Format Garmin's text that will be added to pdf 
garmin_data_pdf = garmin_data_for_pdf(garmin_data)

# Construct pdf
generate_pdf(cst_data_pdf, garmin_data_pdf, common_data_pdf, alerts_dict)

