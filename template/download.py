import streamlit as st
import io
import pandas as pd
import template.constant as constant

from pylife.useful import unwrap

@st.cache_data
def data_report_pdf():
    # !!! TO BE UPDATED !!!
    
    with open(constant.PDF_FILE, "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    return PDFbyte
    
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
    writer.save()
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
    writer.save()
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