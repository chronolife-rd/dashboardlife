import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import data.data as data
import data.cst_raw_data as cst_raw_data
import template.constant as constant 
from pylife.useful import unwrap
from scipy.signal import medfilt
import numpy as np
import datetime 
from template.util import img_to_bytes
from data.data import get_bpm_values, get_brpm_values, get_hrv_values, get_brv_values, get_duration_chronolife, get_duration_garmin, get_stress, get_spo2, get_bodybattery, get_temperature, get_sleep, get_brv,get_inex_values, get_steps
import random

BGCOLOR = 'rgba(255,255,255,1)'

def temperature_mean():

    translate = st.session_state.translate
    line_width = 2

    fig = go.Figure()

    
    values_df = get_temperature()["values"]

    if len(values_df) > 0:
        x = values_df["times"]
        y = values_df["temperature_values"]/100
    
        fig.add_trace(go.Scatter(x=x, 
                                y=y,
                                mode='lines',
                                line=dict(color=constant.COLORS()['temp'], width=line_width),
                                name='tmp'))
        
    fig.update_layout(xaxis_title = translate["times"],
                      yaxis_title=constant.UNIT()['temp'],
                      font=dict(size=14,),
                      height=300, 
                      template="plotly_white",
                      paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                      title=constant.SHORTCUT()['temp'],
                       yaxis = dict(range=constant.RANGE()['temp']),
                      )
    
    return fig

def sleep():
    translate = st.session_state.translate
        
    fig = go.Figure()
    map_sleep = get_sleep()['values']
    if isinstance(map_sleep, str) == False:

        # Add 2 point on the graph for refference
        date = st.session_state.date
        date_1 = datetime.datetime.strptime(date, "%Y-%m-%d")
        date_2 = date_1 + datetime.timedelta(hours = 10)
        fig.add_trace(go.Scatter(x=[date_1, date_2], y=[2, 2], marker_color="white"))

        if "awake" in map_sleep:
            for interval in map_sleep['awake']:
                xend = datetime.datetime.fromtimestamp(interval["endTimeInSeconds"])
                xstart = datetime.datetime.fromtimestamp(interval["startTimeInSeconds"])
                fig.add_shape(type="rect", line_width=0,
                                x0=xstart, y0=0, x1=xend, y1=8,
                                fillcolor=constant.COLORS()['sleep_awake'])
        if "rem" in map_sleep:
            for interval in map_sleep['rem']:
                xend = datetime.datetime.fromtimestamp(interval["endTimeInSeconds"])
                xstart = datetime.datetime.fromtimestamp(interval["startTimeInSeconds"])
                fig.add_shape(type="rect", line_width=0, 
                                x0=xstart, y0=0, x1=xend, y1=6,
                                fillcolor=constant.COLORS()['sleep_rem'])
        if "light" in map_sleep:
            for interval in map_sleep['light']:
                xend = datetime.datetime.fromtimestamp(interval["endTimeInSeconds"])
                xstart = datetime.datetime.fromtimestamp(interval["startTimeInSeconds"])
                fig.add_shape(type="rect", line_width=0, 
                                x0=xstart, y0=0, x1=xend, y1=4,
                                fillcolor=constant.COLORS()['sleep_light'])
        if "deep" in map_sleep:
            for interval in map_sleep['deep']:
                xend = datetime.datetime.fromtimestamp(interval["endTimeInSeconds"])
                xstart = datetime.datetime.fromtimestamp(interval["startTimeInSeconds"])
                fig.add_shape(type="rect", line_width=0, 
                                x0=xstart, y0=0, x1=xend, y1=2,
                                fillcolor=constant.COLORS()['sleep_deep'])

        fig.update_shapes(dict(xref='x', yref='y'))

    fig.update_layout(xaxis_title=translate["times"],
                    font=dict(size=14,),
                    yaxis = dict(
                            tickmode = 'array',
                            tickvals = [2, 4, 6, 8],
                            ticktext = ['Deep', 'Light', 'REM', 'Awake']
                            ),
                    height=300, 
                    template="plotly_white",
                    paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                    title="Sleep scores",
                    showlegend=False,
                    )

    return fig

def bodybattery():
    
    translate = st.session_state.translate
    line_width = 2

    fig = go.Figure()
   
    values_df = get_bodybattery()['values']
    if len(values_df) > 0:
        x = values_df["times"]
        y = values_df["values"]
        
        fig.add_trace(go.Scatter(x=x, 
                                    y=y,
                            mode='lines',
                            line=dict(color=constant.COLORS()['bodybattery'], width=line_width),
                            name='tmp'))
    
    fig.update_layout(xaxis_title=translate["times"],
                      yaxis_title=constant.UNIT()['bodybattery'],
                      font=dict(size=14,),
                      height=300, 
                      template="plotly_white",
                      paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                      title=constant.SHORTCUT()['bodybattery'],
                      yaxis = dict(range=constant.RANGE()['bodybattery']),
                      )
    
    return fig

def pulseox():
    
    translate = st.session_state.translate
    thr_low     = 90
    thr_medium  = 80
    thr_high    = 70

    fig = go.Figure()
    
    values_df = get_spo2()['values']

    if len(values_df) > 0:
        x = values_df["times"]
        y = values_df["values"]
    
        idx = np.where(y >= thr_low)
        if len(idx[0]) > 0:
            idx = idx[0]
        else:
            idx = []
        x_rest = x[idx]
        y_rest = y[idx]

        idx = np.where((y < thr_low) & (y >= thr_medium))
        if len(idx[0]) > 0:
            idx = idx[0]
        else:
            idx = []
        x_low = x[idx]
        y_low = y[idx]

        idx = np.where((y < thr_medium) & (y >= thr_high))
        if len(idx[0]) > 0:
            idx = idx[0]
        else:
            idx = []
        x_medium = x[idx]
        y_medium = y[idx]

        idx = np.where(y < thr_high)
        if len(idx[0]) > 0:
            idx = idx[0]
        else:
            idx = []
        x_high = x[idx]
        y_high = y[idx]

        fig.add_trace(go.Bar(x=x_rest, 
                            y=y_rest,
                            marker_color=constant.COLORS()['spo2_green'],
                            name="Normal"))
        fig.add_trace(go.Bar(x=x_low, 
                            y=y_low,
                            marker_color=constant.COLORS()['spo2_low'],
                            name="Low"))
        fig.add_trace(go.Bar(x=x_medium, 
                            y=y_medium,
                            marker_color=constant.COLORS()['spo2_medium'],
                            name="Very Low"))
        fig.add_trace(go.Bar(x=x_high, 
                            y=y_high,
                            marker_color=constant.COLORS()['spo2_high'],
                            name="Extremely low"))
        
    fig.update_layout(xaxis_title=translate["times"],
                yaxis_title="SpO2",
                font=dict(size=14,),
                height=300, 
                template="plotly_white",
                paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                title="Pulse Ox Scores",
                showlegend=False,
                )
    return fig

def stress():
    translate = st.session_state.translate
    thr_low     = 25
    thr_medium  = 50
    thr_high    = 75

    fig = go.Figure()

    values_df = get_stress()['values']
    if isinstance(values_df, str) == False: 
        values_df = values_df.loc[values_df["values"] > 0].dropna().reset_index(drop=True)
        if len(values_df) > 0:
            x = values_df["times"]
            y = values_df["values"]
        
            idx = np.where(y < thr_low)
            if len(idx[0]) > 0:
                idx = idx[0]
            else:
                idx = []
            x_rest = x[idx]
            y_rest = y[idx]
            
            idx = np.where((y > thr_low) & (y <= thr_medium))
            if len(idx[0]) > 0:
                idx = idx[0]
            else:
                idx = []
            x_low = x[idx]
            y_low = y[idx]
            
            idx = np.where((y > thr_medium) & (y <= thr_high))
            if len(idx[0]) > 0:
                idx = idx[0]
            else:
                idx = []
            x_medium = x[idx]
            y_medium = y[idx]
            
            idx = np.where(y > thr_high)
            if len(idx[0]) > 0:
                idx = idx[0]
            else:
                idx = []
            x_high = x[idx]
            y_high = y[idx]
                    
            fig.add_trace(go.Bar(x=x_rest, 
                                y=y_rest,
                                marker_color=constant.COLORS()['stress_rest'],
                                name="Rest"))
            fig.add_trace(go.Bar(x=x_low, 
                                y=y_low,
                                marker_color=constant.COLORS()['stress_low'],
                                name="Low"))
            fig.add_trace(go.Bar(x=x_medium, 
                                y=y_medium,
                                marker_color=constant.COLORS()['stress_medium'],
                                name="Medium"))
            fig.add_trace(go.Bar(x=x_high, 
                                y=y_high,
                                marker_color=constant.COLORS()['stress_high'],
                                name="High"))
            
    fig.update_layout(xaxis_title=translate["times"],
                    yaxis_title="Stress Scores",
                    font=dict(size=14,),
                    height=300, 
                    template="plotly_white",
                    paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                    title="Stress scores",
                    showlegend=False,
                    )
    
    return fig

def breath_brv():
    
    translate = st.session_state.translate
    
    # !!! TO BE UPDATED WITH REAL DATA !!!
    values_df = get_brv_values()
    x = values_df["times"]
    y = values_df["values"]

    line_width = 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, 
                             y=y,
                        mode='lines',
                        line=dict(color=constant.COLORS()['breath'], width=line_width),
                        name='tmp'))
    
    fig.update_layout(xaxis_title=translate["times"],
                      yaxis_title=constant.UNIT()['brv'],
                      height=400,
                      font=dict(size=14))
    fig.update_layout(height=300, 
                      template="plotly_white",
                      paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                      title=constant.SHORTCUT()['brv'],
                       yaxis = dict(range=constant.RANGE()['brv']),
                      )
    
    return fig

def breath_brpm():
    
    translate = st.session_state.translate    
    line_width = 2

    fig = go.Figure()

    values_df = get_brpm_values()
    if len(values_df) > 0:
        x = values_df["times"]
        y = values_df["values"]

        fig.add_trace(go.Scatter(x=x, 
                                y=y,
                            mode='lines',
                            line=dict(color=constant.COLORS()['breath'], width=line_width),
                            name='tmp'))
    
    fig.update_layout(xaxis_title=translate["times"],
                      yaxis_title=constant.UNIT()['brpm'],
                      height=400,
                      font=dict(size=14,))
    fig.update_layout(height=300, 
                      template="plotly_white",
                      paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                      title=constant.SHORTCUT()['brpm'],
                       yaxis = dict(range=constant.RANGE()['brpm']),
                      )
    
    return fig

def breath_inex():
    
    translate = st.session_state.translate
    
    values_df = get_inex_values()
    x = values_df["times"]
    y = values_df["values"]
    
    line_width = 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, 
                             y=y,
                        mode='lines',
                        line=dict(color=constant.COLORS()['breath'], width=line_width),
                        name='tmp'))
    
    fig.update_layout(xaxis_title=translate["times"],
                      yaxis_title=constant.UNIT()['inspi_expi'],
                      height=400,
                      font=dict(size=14,))
    fig.update_layout(height=300, 
                      template="plotly_white",
                      paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                      title=constant.SHORTCUT()['bior'],
                       yaxis = dict(range=constant.RANGE()['bior']),
                      )
    
    return fig



def heart_hrv():
    
    translate = st.session_state.translate
    
    values_df = get_hrv_values()
    x = values_df["times"]
    y = values_df["values"]
    
    line_width = 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, 
                             y=y,
                        mode='lines',
                        line=dict(color=constant.COLORS()['hrv'], width=line_width),
                        name='tmp'))
    
    fig.update_layout(xaxis_title=translate["times"],
                      yaxis_title=constant.UNIT()['hrv'],
                      height=400,
                      font=dict(size=14,))
    fig.update_layout(height=300, 
                      template="plotly_white",
                      paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                      title=constant.SHORTCUT()['hrv'],
                      )
    
    return fig

def heart_bpm():
    
    translate = st.session_state.translate
           
    line_width = 2
    fig = go.Figure()

    values_df = get_bpm_values()
    if len(values_df) > 0:
        x = values_df["times"]
        y = values_df["values"]
        fig.add_trace(go.Scatter(x=x, 
                                y=y,
                            mode='lines',
                            line=dict(color=constant.COLORS()['ecg'], width=line_width),
                            name='tmp'))
    
    fig.update_layout(xaxis_title=translate["times"],
                      yaxis_title=constant.UNIT()['bpm'],
                      height=400,
                      font=dict(size=14))
    fig.update_layout(height=300, 
                      template="plotly_white",
                      paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                      title=constant.SHORTCUT()['bpm'],
                       yaxis = dict(range=constant.RANGE()['bpm']),
                      )
    
    return fig

def duration():
    
    translate = st.session_state.translate

    date = st.session_state.date
    date = datetime.datetime.strptime(date, "%Y-%m-%d")   
    xmin = date
    xmax = date + datetime.timedelta(days = 1)
        
    y_chronolife    = np.repeat("Smart Textile", 2)
    y_garmin        = np.repeat("Garmin", 2)
    y_empty         = np.repeat(" ", 2)
    y_empty2        = np.repeat("", 2)

    x_garmin        = get_duration_garmin()['intervals']
    x_chronolife    = get_duration_chronolife()['intervals']
    
    width = 20
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=y_empty,
                              x=[datetime.datetime(date.year, date.month, date.day, 00, 0, 0),
                                 datetime.datetime(date.year, date.month, date.day, 23, 59, 59)],
                              mode="lines", line=dict(color="white",width=width)))
    
    # Add Garmin
    for i in range(len(x_garmin)):
        interval = x_garmin[i][:]
        if (len(interval) > 10):
            interval_start = interval.iloc[0]
            interval_end = interval.iloc[-1]
            fig.add_trace(go.Scatter(y = y_garmin, x=[interval_start, interval_end],
                        mode="lines", line=dict(color=constant.COLORS()["garmin"],width=width)))

    # Add Chronolife
    for i in range(len(x_chronolife)):
        interval = x_chronolife[i][:]
        if (len(interval) > 10):
            interval_start = interval.iloc[0]
            interval_end = interval.iloc[-1]
            fig.add_trace(go.Scatter(y = y_chronolife, x=[interval_start, interval_end],
                        mode="lines", line=dict(color=constant.COLORS()["chronolife"],width=width)))
    
    fig.add_trace(go.Scatter(y=y_empty2,
                              x=[datetime.datetime(date.year, date.month, date.day, 00, 0, 0),
                                 datetime.datetime(date.year, date.month, date.day, 23, 0, 0)],
                              mode="lines", line=dict(color="white",width=width)))
    
    fig.update_layout(barmode='stack', height=300, 
                      template="plotly_white",
                      paper_bgcolor=BGCOLOR, plot_bgcolor=BGCOLOR,
                      showlegend=False,
                      title="<span style='font-size:20px;'>" + translate["data_collection_duration"] + "</span>",
                      xaxis = dict(range=[xmin, xmax]), 
                      )
    
    return fig

def smart_textile_raw_data():

    cst_raw_data.get_raw_data()
    
    error = False
    if len(st.session_state.smart_textile_raw_data) == 0:
        error = True 
    if error:
        return error
    
    # Figure Params
    template = 'plotly_white'
    width_line = 2
    height = 275
    
    fig_ecg     = ecg_signal(template=template, width_line=width_line, height=height)
    fig_breath  = breath_signal(template=template, width_line=width_line, height=height)
    #/ fig_acc     = acceleration_signal(template=template, width_line=width_line, height=height)
    
    st.plotly_chart(fig_ecg, use_container_width=True)
    st.plotly_chart(fig_breath, use_container_width=True)
    # st.plotly_chart(fig_acc, use_container_width=True)
    
def ecg_signal(template='plotly_white', width_line=2, height=500):
    # ECG
    raw_data = st.session_state.smart_textile_raw_data[constant.TYPE()['ECG']]
    ymin = max([min(unwrap(raw_data['sig']))*1.1, -1000])
    ymax = min([max(unwrap(raw_data['sig']))*1.1, 1000])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=unwrap(raw_data['times']), y=unwrap(raw_data['sig']),
                        mode='lines',
                        line=dict(color=constant.COLORS()["ecg"], width=width_line),
                                  name='ECG'))
    fig.update_layout(height=height,
                      title='Electrocardiogram',
                      yaxis = dict(range=[ymin, ymax]), 
                      template=template,
                      paper_bgcolor=BGCOLOR, 
                      plot_bgcolor=BGCOLOR,
                      showlegend=False,
                      )
    
    return fig
    
def breath_signal(template='plotly_white', width_line=2, height=500):
    # Breath
    raw_data = st.session_state.smart_textile_raw_data[constant.TYPE()["BREATH_ABDOMINAL"]]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=unwrap(raw_data['times']), y=unwrap(raw_data['sig']),
                              mode='lines',
                              line=dict(color=constant.COLORS()["breath_2"], width=width_line),
                              name='Abdominal Breath'))
    raw_data = st.session_state.smart_textile_raw_data[constant.TYPE()["BREATH_THORACIC"]]
    fig.add_trace(go.Scatter(x=unwrap(raw_data['times']), y=unwrap(raw_data['sig']),
                        mode='lines',
                        line=dict(color=constant.COLORS()["breath"], width=width_line),
                        name='Thoracic Breath'))
    fig.update_layout(height=height, 
                      template=template, 
                      title='Breath',
                      paper_bgcolor=BGCOLOR, 
                      plot_bgcolor=BGCOLOR,
                      showlegend=True,
                      legend=dict(yanchor="top",
                                  y=0.99, xanchor="left", 
                                  x=0.01,
                                  ),
                      )
    return fig

def acceleration_signal(template='plotly_white', width_line=2, height=500):
    # Acceleration
    ymin = -200
    ymax = 200
    fig = go.Figure()
    accx = st.session_state.smart_textile_raw_data[constant.TYPE()["ACCELERATION_X"]]
    accy = st.session_state.smart_textile_raw_data[constant.TYPE()["ACCELERATION_Y"]]
    accz = st.session_state.smart_textile_raw_data[constant.TYPE()["ACCELERATION_Z"]]
    sig = 1/3*(abs(unwrap(accx["sig"])) + abs(unwrap(accy["sig"])) + abs(unwrap(accz["sig"])))
    sig = medfilt(sig, kernel_size=11)
    fig.add_trace(go.Scatter(x=unwrap(accx["times"]), 
                              y=sig,
                        mode='lines',
                        line=dict(color=constant.COLORS()["acc"], width=width_line),
                        name='Acceleration'))
    fig.update_layout(height=height, 
                      template=template, 
                      yaxis = dict(range=[ymin, ymax]),
                      title='Acceleration',
                      paper_bgcolor=BGCOLOR, 
                      plot_bgcolor=BGCOLOR,
                      showlegend=False,
                      )
    
    return fig 

def temperature(al, template='plotly_white', width_line=2, height=500):
    # Temperature
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=unwrap(al.temp_2.times_), 
                              y=1/2*(unwrap(al.temp_2.sig_)+unwrap(al.temp_1.sig_)),
                        mode='lines',
                        line=dict(color=constant.COLORS()["temp_2"], width=width_line),
                        name='Temperature'))
    fig.update_layout(height=height, 
                      template=template, 
                      yaxis = dict(range=[21, 40]), 
                      title='Skin temperature',
                      )
    
    return fig 

def sleep_donut():
    
    translate   = st.session_state.translate
    sleep       = data.get_sleep()
    
    recoded_time   = sleep["duration"]
    if isinstance(recoded_time, str) == False:
        deep    = sleep["percentage_deep"]
        light   = sleep["percentage_light"]
        rem     = sleep["percentage_rem"]
        awake   = sleep["percentage_awake"]
        score   = sleep["score"]
        quality = sleep["quality"]
    else:
        deep    = 25
        light   = 25
        rem     = 25
        awake   = 25
        score   = ""
        quality = "no data"
    
    plt.rcParams['figure.facecolor'] = "white" #cycler(color="#F0F2F6")
    size_of_groups=[deep, light, rem, awake]
    wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    
    plt.figure()
    plt.pie(size_of_groups, 
            colors=[constant.COLORS()["sleep_deep"], 
                    constant.COLORS()["sleep_light"], 
                    constant.COLORS()["sleep_rem"], 
                    constant.COLORS()["sleep_awake"],
                    ], 
            startangle=90,
            counterclock=False,
            wedgeprops=wedgeprops)
    
    my_circle=plt.Circle( (0,0), 0.8, color="white")
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    if score == "":
        plt.text(0, -1.5, translate["no_data"], fontsize=40, color=constant.COLORS()["text"],
                 horizontalalignment='center',verticalalignment='center')
        
    else:
        plt.text(0, 0.2, (str(score) + '/100'), fontsize=30, color=constant.COLORS()["text"],
                 horizontalalignment='center')
        plt.text(0, -.2, translate["quality"], fontsize=20, color=constant.COLORS()["text"],
                 horizontalalignment='center')
        plt.text(0, -.5, quality, fontsize=20, color=constant.COLORS()["text"],
                 horizontalalignment='center')
    
    plt.savefig("template/images/sleep_donut.png", transparent=True)
    st.session_state.sleep_donut = img_to_bytes('template/images/sleep_donut.png')
    
def spo2_donut():
    
    translate = st.session_state.translate
    
    spo2        = data.get_spo2()
    score_mean  = spo2["mean"]
    score_min   = spo2["min"]
    
    # create data
    size_of_groups=[4,23,23,23,23,4]
    wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    plt.close('all')
    plt.figure()
    plt.pie(size_of_groups, 
            colors=["white", 
                    constant.COLORS()['spo2_green'], 
                    constant.COLORS()['spo2_low'], 
                    constant.COLORS()['spo2_medium'], 
                    constant.COLORS()['spo2_high'], 
                    "white"], 
            startangle=270,
            wedgeprops=wedgeprops)
    my_circle=plt.Circle( (0,0), 0.85, color="white")
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    
    if spo2["mean"] == "":
        plt.text(0, -1.5, translate["no_data"], fontsize=40, color=constant.COLORS()["text"],
                 horizontalalignment='center',verticalalignment='center')
    else:
        plt.text(0, 0.20, (str(score_mean) + '%'), fontsize=40, color=constant.COLORS()['text'],
                 horizontalalignment='center')
        plt.text(0, -0.20, translate["lowest"], fontsize=20, color=constant.COLORS()['text'],
                 horizontalalignment='center')
        plt.text(0, -0.50, (str(score_min) + '%'), fontsize=20, color=constant.COLORS()['text'],
                 horizontalalignment='center')

        # setting the axes projection as polar
        plt.axes(projection = 'polar')
        radius = 0.75
    
        score_reshape = ((100 - 0)/(100-60)) * (score_mean - 60)
        deg = (270-(4/100*360)) - score_reshape/100*(92/100*360)
        rad = np.deg2rad(deg)
    
        if score_mean < 70:
            color_spo2_score = constant.COLORS()['spo2_high']
        elif 70 <= score_mean < 80:
            color_spo2_score = constant.COLORS()['spo2_medium']
        elif 80 <= score_mean < 90:
            color_spo2_score = constant.COLORS()['spo2_low']
        elif 90 <= score_mean <= 100:
            color_spo2_score = constant.COLORS()['spo2_green']
            
        plt.polar(rad, radius, '.', markersize=75, color=color_spo2_score)
        plt.polar(rad, 1, '.', color="white")
    plt.axis('off')
    
    plt.savefig("template/images/spo2_donut.png", transparent=True)
    st.session_state.spo2_donut = img_to_bytes('template/images/spo2_donut.png')
    
def steps_donut_old():
    plt.close('all')
    color_text = '#3E738D'

    translate = st.session_state.translate
    steps           = get_steps()
    steps_score     = steps["score"]
            
    wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    
    plt.figure()
    if isinstance(steps_score, str) == False:
        if (steps_score < 100):
            size_of_groups=[steps_score, 100-steps_score]
            plt.pie(size_of_groups, 
                    colors=["#4393B4", "#E6E6E6"], 
                    startangle=90,
                    counterclock=False,
                    wedgeprops=wedgeprops)
        if (steps_score >= 100) :
            size_of_groups=[100]
            plt.pie(size_of_groups, 
                colors=["#13A943"], 
                startangle=90,
                counterclock=False,
                wedgeprops=wedgeprops)  

    my_circle=plt.Circle( (0,0), 0.8, color="white")
    if steps["score"] == "":
        plt.text(0, -1.5, translate["no_data"], fontsize=40, color=constant.COLORS()["text"],
                 horizontalalignment='center',verticalalignment='center')
    else:
        plt.text(0, 0, (str(steps_score) + '%'), fontsize=40, color=color_text,
                 horizontalalignment='center')
        
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    
    plt.savefig("template/images/steps_donut.png", transparent=True)
    st.session_state.steps_donut = img_to_bytes('template/images/steps_donut.png')


def steps_donut():
    
    translate = st.session_state.translate
    steps           = data.get_steps()
    steps_score     = steps["score"]
    
    color_text = '#3E738D'
    
    if steps_score == "":
        size_of_groups=[0, 100]

    elif (steps_score < 100):
        size_of_groups=[steps_score, 100-steps_score]
        plt.pie(size_of_groups, 
                colors=["#4393B4", "#E6E6E6"], 
                startangle=90,
                counterclock=False)
        
    elif (steps_score >= 100) :
        size_of_groups=[100]
        plt.pie(size_of_groups,  
        colors=["#13A943"], 
        startangle=90,
        counterclock=False)
        
    wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    plt.close('all')
    plt.figure()
    plt.pie(size_of_groups, 
            colors=['green', "#e8e8e8"], 
            startangle=90,
            counterclock=False,
            wedgeprops=wedgeprops)
    

    my_circle=plt.Circle( (0,0), 0.8, color="white")
    
    if steps["score"] == "":
        plt.text(0, -1.5, translate["no_data"], fontsize=40, color=constant.COLORS()["text"],
                 horizontalalignment='center',verticalalignment='center')
    else:
        plt.text(0, 0, (str(steps_score) + '%'), fontsize=40, color=color_text,
                 horizontalalignment='center')
        
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    
    plt.savefig("template/images/steps_donut.png", transparent=True)
    st.session_state.steps_donut = img_to_bytes('template/images/steps_donut.png')
    
def stress_donut():
    
    translate = st.session_state.translate
    
    stress      = data.get_stress()
    
    score_mean  = stress["score"]
    if stress["score"] == "":
        rest        = 25
        low         = 25
        medium      = 25
        high        = 25
    else:
        rest        = stress["percentage_rest"]
        low         = stress["percentage_low"]
        medium      = stress["percentage_medium"]
        high        = stress["percentage_high"]
        
    size_of_groups = [rest,low,medium,high]
    wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    plt.close('all')
    plt.figure()
    plt.pie(size_of_groups, 
            colors=[constant.COLORS()["stress_rest"], 
                    constant.COLORS()["stress_low"], 
                    constant.COLORS()["stress_medium"], 
                    constant.COLORS()["stress_high"],
                    ], 
            startangle=90,
            counterclock=False,
            wedgeprops=wedgeprops)
    my_circle=plt.Circle( (0,0), 0.85, color="white")
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    
    if stress["score"] == "":
        plt.text(0, -1.5, translate["no_data"], fontsize=40, color=constant.COLORS()["text"],
                 horizontalalignment='center',verticalalignment='center')
        
    else:
        plt.text(0, 0.2, (str(score_mean)), fontsize=40, color=constant.COLORS()["text"],
                 horizontalalignment='center',verticalalignment='center')
                 
        plt.text(0, -.3, translate["overall"], fontsize=30, color=constant.COLORS()["text"],
                 horizontalalignment='center')
    
    plt.savefig("template/images/stress_donut.png", transparent=True)
    st.session_state.stress_donut = img_to_bytes('template/images/stress_donut.png')