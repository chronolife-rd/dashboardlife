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
from data.data import get_steps,get_bpm_values,get_temperature,get_sleep,get_bodybattery,get_spo2,get_stress,get_qt,get_bradypnea,get_bradycardia,get_tachypnea,get_tachycardia,get_brv_values,get_inexratio,get_brpm,get_hrv_values

from pylife.useful import unwrap, unwrap_signals_dashboard

# @st.cache_data
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
      
# @st.cache_data
def health_indicators_to_excel():
  # Cache the conversion to prevent computation on every rerun
  output = io.BytesIO()
  writer = pd.ExcelWriter(output,engine='xlsxwriter')
  workbook = writer.book

  #on verifie s'il y a des donnees cote chronolife pour les enregistrer ou non dans le fichier
  
  #init
  HR_value = get_bpm_values()
  HRV_value = get_hrv_values()
  BR_value = get_brpm()
  Inex_value = get_inexratio()
  BRV_value = get_brv_values()
  tachycardia_value = get_tachycardia()
  tachypnea_value = get_tachypnea()
  bradycardia_value = get_bradycardia()
  bradypnea_value = get_bradypnea()
  Qt_value = get_qt()
  Stress_value = get_stress()
  Pulseox_value = get_spo2()
  Bodybatt_value = get_bodybattery()
  Sleep_value = get_sleep()
  Temp_value = get_temperature()
  
  fonction = [HR_value,HRV_value,BR_value,BRV_value,Inex_value,tachycardia_value,tachypnea_value,bradypnea_value,bradycardia_value,Qt_value, Stress_value, Pulseox_value, Bodybatt_value, Sleep_value, Temp_value]
  nom_donnee = ["HR", "HRV","BR","BRV","Ratio Inex","Tachycardie","Tachypnée","Bradypnée","Bradycardie","Intervalle QT", "Stress","SpO2","Body Battery","Sommeil", "Température"]

  #pour chaque fonction on teste la longueur de ce qui est retourné pour attribuer la valeur a une variable ou la mettre à 0
  for i in range(len(fonction)):
      print("valeur de i :",i)
      if len(fonction[i]) > 0 : 
          print("Donnee de", nom_donnee[i],"trouvee")
          print(fonction[i])
      else : 
          fonction[i] = 0
          print("No", nom_donnee[i], "data found")
          print("valeur de",nom_donnee[i],":", fonction[i])
  
  #on crée des dictionnaires pour que l'on puisse classer les données dans des feuillets

  HR_dict = {
    'Time': HR_value['times'],
    'Valeur': HR_value['values']
  }

  HRV_dict = {
    'Time': HRV_value['times'],
    'Valeur': HRV_value['values'],
    'Activité': HRV_value['activity_values'],
    'Température': HRV_value['temperature_values']
  }

  BR_dict = {
      'Moyenne' : BR_value['mean'],
      'Minimum' : BR_value['min'],
      'Maximum' : BR_value['max'],
      'Repos' : BR_value['rest'],
      'Haut' : BR_value['high']
  }

  BRV_dict = {
    'Time': BRV_value['times'],
    'Valeur': BRV_value['values'],
    'Activité': BRV_value['activity_values'],
    'Température': BRV_value['temperature_values']
  }

  Inex_dict = {
      'Temps': Inex_value['values']['times'],
      'Valeur' : Inex_value['values']['values'],
      'Moyenne': Inex_value['mean'],
      'Minimum': Inex_value['min'],
      'Maximum': Inex_value['max']
  }

  Bradycardia_dict = {
      'HR' : bradycardia_value['mean'],
      'Durée' : bradycardia_value['duration'],
      'Proportion' : bradycardia_value['percentage']
  }

  Bradypnea_dict = {
      'HR' : bradypnea_value['mean'],
      'Durée' : bradypnea_value['duration'],
      'Proportion' : bradypnea_value['percentage']
  }

  Tachypnea_dict = {
      'HR' : tachypnea_value['mean'],
      'Durée' : tachypnea_value['duration'],
      'Proportion' : tachypnea_value['percentage']
  }

  Tachycardia_dict = {
      'Moyenne' : tachycardia_value['mean'],
      'Durée' : tachycardia_value['duration'],
      'Pourcentage' : tachycardia_value['percentage']
  }

  Qt_dict = {
      'Valeur' : Qt_value['values'],
      'Nuit' : Qt_value['night'],
      'Matin' : Qt_value['morning'],
      'Soir' : Qt_value['evening']
  }

  Stress_dict = {
      'Valeur' : Stress_value['values'],
      'Score' : Stress_value['score'],
      'Durée' : Stress_value['duration'],
      'Durée au repos' : Stress_value['duration_rest'],
      'Durée au plus bas' : Stress_value['duration_low'],
      'Durée moyenne' : Stress_value['duration_medium'],
      'Durée au plus haut' : Stress_value['duration_high'],
      'Pourcentage au repos' : Stress_value['percentage_rest'],
      'Pourcentage au plus bas' : Stress_value['percentage_low'],
      'Pourcentage moyen' : Stress_value['percentage_medium'],
      'Pourcentage au plus haut' : Stress_value['percentage_high']
  }

  Pulseox_dict = {
      'Moyenne': Pulseox_value['mean'],
      'Minimum': Pulseox_value['min'],
      'Valeur': Pulseox_value['values']
  }

  Bodybatt_dict = {
      'Valeur': Bodybatt_value['values'],
      'Maximum': Bodybatt_value['high'],
      'Minimum': Bodybatt_value['low']
  }

  Sleep_dict = {
      'Valeur' : Sleep_value['values'],
      'Score' : Sleep_value['score'],
      'Qualité' : Sleep_value['quality'],
      'Durée' : Sleep_value['duration'],
      'Durée profond' : Sleep_value['duration_deep'],
      'Durée léger' : Sleep_value['duration_light'],
      'Durée paradoxal' : Sleep_value['duration_rem'],
      'Durée éveillé' : Sleep_value['duration_awake'],
      'Pourcentage profond' : Sleep_value['percentage_deep'],
      'Pourcentage léger' : Sleep_value['percentage_light'],
      'Pourcentage paradoxal' : Sleep_value['percentage_rem'],
      'Pourcentage éveillé' : Sleep_value['percentage_awake']
  }

  Temp_dict = {
      'Temps' : Temp_value['values']['times'],
      'Valeur' : Temp_value['values']['temperature_values'],
      'Moyenne' : Temp_value['mean'],
      'Minimum' : Temp_value['min'],
      'Maximum' : Temp_value['max']
  }


  #load data into a DataFrame object:
  #-------Sheet for HR-------#
  df = pd.DataFrame.from_dict(HR_dict)
  df.to_excel(writer, index=False, sheet_name='HR')
  worksheet = writer.sheets['HR']
  #-------Sheet for HRV-------#
  df = pd.DataFrame.from_dict(HRV_dict)
  df.to_excel(writer, index=False, sheet_name='HRV')
  worksheet = writer.sheets['HRV']
  #-------Sheet for BR-------#
  df = pd.DataFrame.from_dict([BR_dict])
  df.to_excel(writer, index=False, sheet_name='BR')
  worksheet = writer.sheets['BR']
  #-------Sheet for BRV -------#
  df = pd.DataFrame.from_dict(BRV_dict)
  df.to_excel(writer, index=False, sheet_name='BRV')
  worksheet = writer.sheets['BRV']
  #-------Sheet for Ratio Inspi-Expi -------#
  df = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in Inex_dict.items()]))
  df.to_excel(writer, index=False, sheet_name='Ration Inspi-Expi')
  worksheet = writer.sheets['Ration Inspi-Expi']
  #-------Sheet for Bradycardie-------#
  df = pd.DataFrame.from_dict([Bradycardia_dict])
  df.to_excel(writer, index=False, sheet_name='Bradycardie')
  worksheet = writer.sheets['Bradycardie']
  #-------Sheet for Bradypnée-------#
  df = pd.DataFrame.from_dict([Bradypnea_dict])
  df.to_excel(writer, index=False, sheet_name='Bradypnée')
  worksheet = writer.sheets['Bradypnée']
  #-------Sheet for Tachycardie-------#
  df = pd.DataFrame.from_dict([Tachycardia_dict])
  df.to_excel(writer, index=False, sheet_name='Tachycardie')
  worksheet = writer.sheets['Tachycardie']
  #-------Sheet for Tachypnée-------#
  df = pd.DataFrame.from_dict([Tachypnea_dict])
  df.to_excel(writer, index=False, sheet_name='Tachypnée')
  worksheet = writer.sheets['Tachypnée']
  #-------Sheet for Intervalle de QT-------#
  df = pd.DataFrame.from_dict([Qt_dict])
  df.to_excel(writer, index=False, sheet_name='Intervalle de QT')
  worksheet = writer.sheets['Intervalle de QT']
  #-------Sheet for Stress value-------#
  df = pd.DataFrame.from_dict([Stress_dict])
  df.to_excel(writer, index=False, sheet_name='Stress')
  worksheet = writer.sheets['Stress']
  #-------Sheet for SpO2-------#
  df = pd.DataFrame.from_dict([Pulseox_dict])
  df.to_excel(writer, index=False, sheet_name='SpO2')
  worksheet = writer.sheets['SpO2']
  #-------Sheet for Body battery-------#
  df = pd.DataFrame.from_dict([Bodybatt_dict])
  df.to_excel(writer, index=False, sheet_name='Body battery')
  worksheet = writer.sheets['Body battery']
  #-------Sheet for Sommeil-------#
  df = pd.DataFrame.from_dict([Sleep_dict])
  df.to_excel(writer, index=False, sheet_name='Sommeil')
  worksheet = writer.sheets['Sommeil']
  #-------Sheet for Temperature-------#
  df = pd.DataFrame(dict([(key, pd.Series(value)) for key, value in Temp_dict.items()]))
  df.to_excel(writer, index=False, sheet_name='Température de la peau')
  worksheet = writer.sheets['Température de la peau']

  
  format1 = workbook.add_format({'num_format': '0.00'}) 
  worksheet.set_column('A:A', None, format1)
  writer.close()
  data = output.getvalue()
  return data


# @st.cache_data
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
    
    times   = unwrap_signals_dashboard(accx['times'])
    x       = unwrap_signals_dashboard(accx['sig'])
    y       = unwrap_signals_dashboard(accy['sig'])
    z       = unwrap_signals_dashboard(accz['sig'])
    
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
    times       = unwrap_signals_dashboard(breath_1['times'])
    breath_tho  = unwrap_signals_dashboard(breath_1['sig'])
    breath_abd  = unwrap_signals_dashboard(breath_2['sig'])
    
    data_dict = {
      "Date": times,
      "Abdominal values": breath_abd,
      "Thoracic values": breath_tho
    }
    df = pd.DataFrame(data_dict)
    
    return df

def parse_ecg_for_excel():
    ecg     = st.session_state.smart_textile_raw_data[constant.TYPE()['ECG']]
    times   = unwrap_signals_dashboard(ecg['times'])
    values  = unwrap_signals_dashboard(ecg['sig'])
    
    data_dict = {
      "Date": times,
      "ECG values": values
    }
    df = pd.DataFrame(data_dict)
    
    return df