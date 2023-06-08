import streamlit as st
import io
import os
import pandas as pd
import template.constant as constant

from data.data import get_health_indicators
from automatic_reports.generate_pdf import generate_pdf
from automatic_reports.compute_garmin_for_pdf import garmin_data_for_pdf
from automatic_reports.compute_cst_for_pdf import cst_data_for_pdf
from automatic_reports.compute_common_for_pdf import get_common_indicators_pdf
from automatic_reports.plot_images import plot_images
from data.data import get_steps

from pylife.useful import unwrap

@st.cache_data
def data_report_pdf():
    
    # Delete pdf if exists
    if os.path.exists(constant.PDF_FILE):
        os.remove(constant.PDF_FILE)

    date                        = st.session_state.date
    garmin_data                 = st.session_state.garmin_indicators    
    chronolife_data             = st.session_state.chronolife_indicators  
    common_indicators_pdf       = st.session_state.common_indicators_pdf 
    chronolife_indicators_pdf   = st.session_state.chronolife_indicators_pdf 
    garmin_indicators_pdf       = st.session_state.garmin_indicators_pdf 
  
    print(date)
    # Get intervals and alerts
    garmin_time_intervals = garmin_data['duration']['intervals']
    cst_time_intervals = chronolife_data['duration']['intervals']
    alerts_dict = chronolife_data['anomalies']
    steps           = get_steps()
    steps_score     = steps["score"]
    
    # Plot and save graphs
    plot_images(garmin_data, cst_time_intervals, garmin_time_intervals, date, steps_score)
    
    # Construct pdf
    generate_pdf(chronolife_indicators_pdf, garmin_indicators_pdf, common_indicators_pdf, alerts_dict)
    
    with open(constant.PDF_FILE, "rb") as pdf_file:
        return pdf_file.read()
      
@st.cache_data
def health_indicators_to_excel():
    # !!! TO BE UPDATED !!!
    # Cache the conversion to prevent computation on every rerun
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    data_dict = {
      "calories": [420, 380, 390],
      "duration": [50, 40, 45]
    }
    
    #load data into a DataFrame object:
    df = pd.DataFrame(data_dict)
    df.to_excel(writer, index=False, sheet_name='Results')
    worksheet = writer.sheets['Results']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.close()
    data = output.getvalue()
    return data

@st.cache_data
def raw_data_to_excel():
        
    output = io.BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    workbook = writer.book
    
    df_acc = parse_acceleration_for_excel()
    df_acc.to_excel(writer, index=False, sheet_name='Acceleration')
    
    df_breath = parse_breath_for_excel()
    df_breath.to_excel(writer, index=False, sheet_name='Respiratory')
    
    df_ecg = parse_ecg_for_excel()
    df_ecg.to_excel(writer, index=False, sheet_name='ECG')
    
    worksheet = writer.sheets['Acceleration']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.close()
    data = output.getvalue()
    return data

def parse_acceleration_for_excel():
    accx    = st.session_state.smart_textile_raw_data[constant.TYPE()["ACCELERATION_X"]]
    accy    = st.session_state.smart_textile_raw_data[constant.TYPE()["ACCELERATION_Y"]]
    accz    = st.session_state.smart_textile_raw_data[constant.TYPE()["ACCELERATION_Z"]]
    
    times   = unwrap(accx['times'])
    x       = unwrap(accx['sig'])
    y       = unwrap(accy['sig'])
    z       = unwrap(accz['sig'])
    
    data_dict = {
      "Date": times,
      "X values": x,
      "Y values": y,
      "Z values": z,
    }
    df = pd.DataFrame(data_dict)
    
    return df

def parse_breath_for_excel():
    breath_1    = st.session_state.smart_textile_raw_data[constant.TYPE()["BREATH_THORACIC"]]
    breath_2    = st.session_state.smart_textile_raw_data[constant.TYPE()["BREATH_ABDOMINAL"]]
    times       = unwrap(breath_1['times'])
    breath_tho  = unwrap(breath_1['sig'])
    breath_abd  = unwrap(breath_2['sig'])
    
    data_dict = {
      "Date": times,
      "Abdominal values": breath_abd,
      "Thoracic values": breath_tho
    }
    df = pd.DataFrame(data_dict)
    
    return df

def parse_ecg_for_excel():
    ecg     = st.session_state.smart_textile_raw_data[constant.TYPE()['ECG']]
    times   = unwrap(ecg['times'])
    values  = unwrap(ecg['sig'])
    
    data_dict = {
      "Date": times,
      "ECG values": values
    }
    df = pd.DataFrame(data_dict)
    
    return df