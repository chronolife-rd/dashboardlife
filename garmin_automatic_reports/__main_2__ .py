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
from garmin_data_for_pdf import garmin_data_for_pdf
from cst_data_for_pdf import cst_data_for_pdf
from commun_data_for_pdf import commun_data_for_pdf
from plot_images import plot_images

user_id = "5Nwwut"
date = "2023-05-04"

# ----------------------------- Chronolife -------------------------------
# # Start timer    
# user_id_cst = "7k6Hs3" # prod
# date_cst = "2022-09-09"
begin = time.time()

cst_data = get_cst_data(
    user_id = user_id, 
    date = date,
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
# begin = time.time()
# user_id_garmin = "6o2Fzp" # prepros
# date_garmin = '2023-05-02'

garmin_data = get_garmin_data(
    user_id = user_id, 
    date = date,
    )

# Time intervals
garmin_time_intervals = garmin_data['duration']['collected']

# End timer
end = time.time()
print('Time taken to get Garmin data:',round((end-begin)/60,2),'min')

# %% -------------------------- Construct PDF --------------------------------
# Format CST's text that will be added to pdf 
cst_data_pdf = cst_data_for_pdf(user_id, date, cst_data)

# Format Garmin's text that will be added to pdf 
garmin_data_pdf = garmin_data_for_pdf(garmin_data)

# %% 
# Compute commun indicators: cardio, respiration and steps
commun_data, commun_data_pdf, steps_dict = commun_data_for_pdf(cst_data, garmin_data) 

# Plot and save graphs
plot_images(garmin_data, steps_dict, cst_time_intervals, 
            garmin_time_intervals, date)

# Construct pdf
generate_pdf(cst_data_pdf, garmin_data_pdf, commun_data_pdf, alerts_dict)

