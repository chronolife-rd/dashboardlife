import streamlit as st
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import template.data as data
from template.constant import (COLORS, UNIT, SHORTCUT,
                               TYPE_ECG,
                               TYPE_BREATH_ABDOMINAL,
                               TYPE_BREATH_THORACIC,
                               TYPE_ACCELERATION_X,
                               TYPE_ACCELERATION_Y,
                               TYPE_ACCELERATION_Z,
                               TYPE_SIGNALS)
from pylife.useful import unwrap
from scipy.signal import medfilt
import numpy as np
import datetime
from template.util import img_to_bytes

def test_chart():
    
    base = datetime.datetime(2023, 4, 19)
    x = np.array([base + datetime.timedelta(minutes=i) for i in range(0,24*60,5)])
    y = 100*np.random.rand(len(x))
    
    i_high = []
    x_high = np.where(y >= 50)
    if len(x_high[0]) > 0:
        i_high = x_high[0]
    x_high = x[i_high]
    y_high = y[i_high]
    
    i_low = []
    x_low = np.where(y < 50)
    if len(x_low[0]) > 0:
        i_low = x_low[0]
    x_low = x[i_low]
    y_low = y[i_low]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_low, 
                         y=y_low,
                         marker_color=COLORS['breath'],
                        name='tmp'))
    fig.add_trace(go.Bar(x=x_high, 
                         y=y_high,
                         marker_color=COLORS['temp'],
                        name='tmp'))
    
    fig.update_layout(xaxis_title="Times",
                      yaxis_title="test",
                      font=dict(size=14,),
                      height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      title=SHORTCUT['temp'],
                      # yaxis = dict(range=RANGE['bpm']),
                      )
    
    return fig

def temperature_mean():
    
    base = datetime.datetime(2023, 4, 19)
    x = np.array([base + datetime.timedelta(minutes=i) for i in range(0,24*60,5)])
    
    y = 35 + np.random.rand(len(x))
    line_width = 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, 
                             y=y,
                        mode='lines',
                        line=dict(color=COLORS['temp'], width=line_width),
                        name='tmp'))
    
    fig.update_layout(xaxis_title="Times",
                      yaxis_title=UNIT['temp'],
                      font=dict(size=14,),
                      height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      title=SHORTCUT['temp'],
                      # yaxis = dict(range=RANGE['bpm']),
                      )
    
    return fig

def sleep():
    
    base = datetime.datetime(2023, 4, 19)
    x = np.array([base + datetime.timedelta(minutes=i) for i in range(0,24*60,5)])

    y = np.linspace(0,100, num=len(x)) + 20*np.random.rand(len(x))

    thr_light     = 25
    thr_rem     = 50
    thr_awake    = 75

    idx = np.where(y < thr_light)
    if len(idx[0]) > 0:
        idx = idx[0]
    else:
        idx = []
    x_rest = x[idx]
    y_rest = y[idx]

    idx = np.where((y > thr_light) & (y <= thr_rem))
    if len(idx[0]) > 0:
        idx = idx[0]
    else:
        idx = []
    x_light = x[idx]
    y_light = y[idx]

    idx = np.where((y > thr_rem) & (y <= thr_awake))
    if len(idx[0]) > 0:
        idx = idx[0]
    else:
        idx = []
    x_rem = x[idx]
    y_rem = y[idx]

    idx = np.where(y > thr_awake)
    if len(idx[0]) > 0:
        idx = idx[0]
    else:
        idx = []
    x_awake = x[idx]
    y_awake = y[idx]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_rest, 
                         y=y_rest,
                         marker_color=COLORS['sleep_deep'],
                         name="Deep"))
    fig.add_trace(go.Bar(x=x_light, 
                         y=y_light,
                         marker_color=COLORS['sleep_light'],
                         name="Light"))
    fig.add_trace(go.Bar(x=x_rem, 
                         y=y_rem,
                         marker_color=COLORS['sleep_rem'],
                         name="REM"))
    fig.add_trace(go.Bar(x=x_awake, 
                         y=y_awake,
                         marker_color=COLORS['sleep_awake'],
                         name="Awake"))

    fig.update_layout(xaxis_title="Times",
                      yaxis_title="Sleep Scores",
                      font=dict(size=14,),
                      height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      title="Sleep scores",
                      showlegend=False,
                      )
    
    return fig

def bodybattery():
    
    base = datetime.datetime(2023, 4, 19)
    x = np.array([base + datetime.timedelta(minutes=i) for i in range(0,24*60,5)])
    
    y = np.linspace(80,20,num=len(x)) + 20*np.random.rand(len(x))
    
    line_width = 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, 
                             y=y,
                        mode='lines',
                        line=dict(color=COLORS['bodybattery'], width=line_width),
                        name='tmp'))
    
    fig.update_layout(xaxis_title="Times",
                      yaxis_title=UNIT['bodybattery'],
                      font=dict(size=14,),
                      height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      title=SHORTCUT['bodybattery'],
                      # yaxis = dict(range=RANGE['bpm']),
                      )
    
    return fig

def pulseox():
    
    base = datetime.datetime(2023, 4, 19)
    x = np.array([base + datetime.timedelta(minutes=i) for i in range(0,24*60,5)])

    y = 95 - np.ones(len(x)) + 5*np.random.rand(len(x))

    thr_low     = 90
    thr_medium  = 80
    thr_high    = 70

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

    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_rest, 
                         y=y_rest,
                         marker_color=COLORS['spo2_green'],
                         name="Normal"))
    fig.add_trace(go.Bar(x=x_low, 
                         y=y_low,
                         marker_color=COLORS['spo2_low'],
                         name="Low"))
    fig.add_trace(go.Bar(x=x_medium, 
                         y=y_medium,
                         marker_color=COLORS['spo2_medium'],
                         name="Very Low"))
    fig.add_trace(go.Bar(x=x_high, 
                         y=y_high,
                         marker_color=COLORS['spo2_high'],
                         name="Extremely low"))

    fig.update_layout(xaxis_title="Times",
                      yaxis_title="SpO2",
                      font=dict(size=14,),
                      height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      title="Pulse Ox Scores",
                      showlegend=False,
                      )
    
    return fig

def stress():
    
    base = datetime.datetime(2023, 4, 19)
    x = np.array([base + datetime.timedelta(minutes=i) for i in range(0,24*60,5)])
    
    y = np.linspace(20,50,num=len(x)) + 20*np.random.rand(len(x))
    
    thr_low     = 25
    thr_medium  = 50
    thr_high    = 75
    
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
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x_rest, 
                         y=y_rest,
                         marker_color=COLORS['stress_rest'],
                         name="Rest"))
    fig.add_trace(go.Bar(x=x_low, 
                         y=y_low,
                         marker_color=COLORS['stress_low'],
                         name="Low"))
    fig.add_trace(go.Bar(x=x_medium, 
                         y=y_medium,
                         marker_color=COLORS['stress_medium'],
                         name="Medium"))
    fig.add_trace(go.Bar(x=x_high, 
                         y=y_high,
                         marker_color=COLORS['stress_high'],
                         name="High"))
    
    fig.update_layout(xaxis_title="Times",
                      yaxis_title="Stress Scores",
                      font=dict(size=14,),
                      height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      title="Stress scores",
                      showlegend=False,
                      )
    
    return fig

def breath_brv():
    
    base = datetime.datetime(2023, 4, 19)
    x = np.array([base + datetime.timedelta(minutes=i) for i in range(0,24*60,5)])
    
    y = 1 + np.random.rand(len(x))
    line_width = 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, 
                             y=y,
                        mode='lines',
                        line=dict(color=COLORS['breath'], width=line_width),
                        name='tmp'))
    
    fig.update_layout(xaxis_title="Times",
                      yaxis_title=UNIT['brv'],
                      height=400,
                      font=dict(
                          # family="Courier New, monospace",
                          size=14,
                          ))
    fig.update_layout(height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      title=SHORTCUT['brv'],
                      # yaxis = dict(range=RANGE['bpm']),
                      )
    
    return fig

def breath_brpm():
    
    base = datetime.datetime(2023, 4, 19)
    x = np.array([base + datetime.timedelta(minutes=i) for i in range(0,24*60,5)])
    
    y = 14 + np.random.rand(len(x))
    line_width = 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, 
                             y=y,
                        mode='lines',
                        line=dict(color=COLORS['breath'], width=line_width),
                        name='tmp'))
    
    fig.update_layout(xaxis_title="Times",
                      yaxis_title=UNIT['brpm'],
                      height=400,
                      font=dict(
                          # family="Courier New, monospace",
                          size=14,
                          ))
    fig.update_layout(height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      title=SHORTCUT['brpm'],
                      # yaxis = dict(range=RANGE['bpm']),
                      )
    
    return fig

def heart_hrv():
    
    base = datetime.datetime(2023, 4, 19)
    x = np.array([base + datetime.timedelta(minutes=i) for i in range(0,24*60,5)])
    
    y = 162 + np.random.rand(len(x))
    line_width = 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, 
                             y=y,
                        mode='lines',
                        line=dict(color=COLORS['hrv'], width=line_width),
                        name='tmp'))
    
    fig.update_layout(xaxis_title="Times",
                      yaxis_title=UNIT['hrv'],
                      height=400,
                      font=dict(
                          # family="Courier New, monospace",
                          size=14,
                          ))
    fig.update_layout(height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      title=SHORTCUT['hrv'],
                      # yaxis = dict(range=RANGE['bpm']),
                      )
    
    return fig

def heart_bpm():
    
    base = datetime.datetime(2023, 4, 19)
    x = np.array([base + datetime.timedelta(minutes=i) for i in range(0,24*60,5)])
    y = 67 + np.random.rand(len(x))
    line_width = 2
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, 
                             y=y,
                        mode='lines',
                        line=dict(color=COLORS['ecg'], width=line_width),
                        name='tmp'))
    
    fig.update_layout(xaxis_title="Times",
                      yaxis_title=UNIT['bpm'],
                      height=400,
                      font=dict(
                          # family="Courier New, monospace",
                          size=14,
                          ))
    fig.update_layout(height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      title=SHORTCUT['bpm'],
                      # yaxis = dict(range=RANGE['bpm']),
                      )
    
    return fig

def duration():
    
    width = 20
    date = st.session_state.date
    xmin = date
    xmax = date + datetime.timedelta(days=1)
    
    y_chronolife    = np.repeat("Smart Textile", 2)
    y_garmin        = np.repeat("Garmin", 2)
    y_empty         = np.repeat(" ", 2)
    y_empty2        = np.repeat("", 2)

    fig = go.Figure()
    # fig.add_trace(go.Scatter(y=y_empty,
    #                           x=[datetime.datetime(date.year, date.month, date.day, 00, 0, 0),
    #                              datetime.datetime(date.year, date.month, date.day, 23, 59, 59)],
    #                           mode="lines", line=dict(color="white",width=width)))
    
    fig.add_trace(go.Scatter(y=y_garmin,
                              x=[datetime.datetime(date.year, date.month, date.day, 00, 0, 0),
                                 datetime.datetime(date.year, date.month, date.day, 23, 59, 0)],
                              mode="lines", line=dict(color=COLORS["garmin"],width=width)))
    # fig.add_trace(go.Scatter(y=y_garmin,
    #                          x=[datetime.datetime(date.year, date.month, date.day, 6, 0, 0),
    #                            datetime.datetime(date.year, date.month, date.day, 9, 0, 0)],
    #                          mode="lines",line=dict(color="white",width=width)))
    # fig.add_trace(go.Scatter(y=y_garmin,
    #                          x=[datetime.datetime(date.year, date.month, date.day, 9, 0, 0),
    #                            datetime.datetime(date.year, date.month, date.day, 13, 0, 0)],
    #                          mode="lines",line=dict(color=COLORS["garmin"],width=width)))
    # fig.add_trace(go.Scatter(y=y_garmin,
    #                          x=[datetime.datetime(date.year, date.month, date.day, 13, 0, 0),
    #                            datetime.datetime(date.year, date.month, date.day, 23, 59, 59)],
    #                          mode="lines",line=dict(color="white",width=width)))
    
    
    fig.add_trace(go.Scatter(y=y_chronolife,
                              x=[datetime.datetime(date.year, date.month, date.day, 00, 0, 0),
                                 datetime.datetime(date.year, date.month, date.day, 23, 59, 0)],
                              mode="lines", line=dict(color=COLORS["chronolife"],width=width)))
    # fig.add_trace(go.Scatter(y=y_chronolife,
    #                          x=[datetime.datetime(date.year, date.month, date.day, 6, 0, 0),
    #                            datetime.datetime(date.year, date.month, date.day, 9, 0, 0)],
    #                          mode="lines",line=dict(color="white",width=width)))
    # fig.add_trace(go.Scatter(y=y_chronolife,
    #                          x=[datetime.datetime(date.year, date.month, date.day, 9, 0, 0),
    #                            datetime.datetime(date.year, date.month, date.day, 13, 0, 0)],
    #                          mode="lines",line=dict(color=COLORS["chronolife"],width=width)))
    # fig.add_trace(go.Scatter(y=y_chronolife,
    #                          x=[datetime.datetime(date.year, date.month, date.day, 13, 0, 0),
    #                            datetime.datetime(date.year, date.month, date.day, 23, 59, 59)],
    #                          mode="lines",line=dict(color="white",width=width)))
    
    # fig.add_trace(go.Scatter(y=y_empty2,
    #                           x=[datetime.datetime(date.year, date.month, date.day, 00, 0, 0),
    #                              datetime.datetime(date.year, date.month, date.day, 23, 0, 0)],
    #                           mode="lines", line=dict(color="white",width=width)))
    
    fig.update_layout(barmode='stack', height=300, 
                      template="plotly_white",
                      paper_bgcolor='rgba(255,255,255,1)', plot_bgcolor='rgba(255,255,255,1)',
                      showlegend=False,
                      title='<span style="font-size:20px;">DURATION OF DATA COLLECTION</span>',
                      xaxis = dict(range=[xmin, xmax]), 
                      )
    
    return fig

def smart_textile_raw_data(layout=False):

    data.get_smart_textile_raw_data()
    
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
    # fig_acc     = acceleration_signal(template=template, width_line=width_line, height=height)
    
    st.plotly_chart(fig_ecg, use_container_width=True)
    st.plotly_chart(fig_breath, use_container_width=True)
    # st.plotly_chart(fig_acc, use_container_width=True)
    
def ecg_signal(template='plotly_white', width_line=2, height=500):
    # ECG
    raw_data = st.session_state.smart_textile_raw_data[TYPE_ECG]
    ymin = max([min(unwrap(raw_data['sig']))*1.1, -1000])
    ymax = min([max(unwrap(raw_data['sig']))*1.1, 1000])
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=unwrap(raw_data['times']), y=unwrap(raw_data['sig']),
                        mode='lines',
                        line=dict(color=COLORS["ecg"], width=width_line),
                                  name='ECG'))
    fig.update_layout(height=height,
                      title='Electrocardiogram',
                      yaxis = dict(range=[ymin, ymax]), 
                      template=template,
                      paper_bgcolor='rgba(255,255,255,1)', 
                      plot_bgcolor='rgba(255,255,255,1)',
                      showlegend=False,
                      )
    
    return fig
    
def breath_signal(template='plotly_white', width_line=2, height=500):
    # Breath
    raw_data = st.session_state.smart_textile_raw_data[TYPE_BREATH_ABDOMINAL]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=unwrap(raw_data['times']), y=unwrap(raw_data['sig']),
                              mode='lines',
                              line=dict(color=COLORS["breath_2"], width=width_line),
                              name='Abdominal Breath'))
    raw_data = st.session_state.smart_textile_raw_data[TYPE_BREATH_THORACIC]
    fig.add_trace(go.Scatter(x=unwrap(raw_data['times']), y=unwrap(raw_data['sig']),
                        mode='lines',
                        line=dict(color=COLORS["breath"], width=width_line),
                        name='Thoracic Breath'))
    fig.update_layout(height=height, 
                      template=template, 
                      title='Breath',
                      paper_bgcolor='rgba(255,255,255,1)', 
                      plot_bgcolor='rgba(255,255,255,1)',
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
    accx = st.session_state.smart_textile_raw_data[TYPE_ACCELERATION_X]
    accy = st.session_state.smart_textile_raw_data[TYPE_ACCELERATION_Y]
    accz = st.session_state.smart_textile_raw_data[TYPE_ACCELERATION_Z]
    sig = 1/3*(abs(unwrap(accx["sig"])) + abs(unwrap(accy["sig"])) + abs(unwrap(accz["sig"])))
    sig = medfilt(sig, kernel_size=11)
    fig.add_trace(go.Scatter(x=unwrap(accx["times"]), 
                              y=sig,
                        mode='lines',
                        line=dict(color=COLORS["acc"], width=width_line),
                        name='Acceleration'))
    fig.update_layout(height=height, 
                      template=template, 
                      yaxis = dict(range=[ymin, ymax]),
                      title='Acceleration',
                      paper_bgcolor='rgba(255,255,255,1)', 
                      plot_bgcolor='rgba(255,255,255,1)',
                      showlegend=False,
                      )
    
    return fig 

def temperature(al, template='plotly_white', width_line=2, height=500):
    # Temperature
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=unwrap(al.temp_2.times_), 
                              y=1/2*(unwrap(al.temp_2.sig_)+unwrap(al.temp_1.sig_)),
                        mode='lines',
                        line=dict(color=COLORS["temp_2"], width=width_line),
                        name='Temperature'))
    fig.update_layout(height=height, 
                      template=template, 
                      yaxis = dict(range=[21, 40]), 
                      title='Skin temperature',
                      )
    
    return fig 

def sleep_donut():
    
    sleep   = data.get_sleep()
    score   = sleep["score"]
    deep    = sleep["percentage_deep"]
    light   = sleep["percentage_light"]
    rem     = sleep["percentage_rem"]
    awake   = sleep["percentage_awake"]
    
    plt.rcParams['figure.facecolor'] = "white" #cycler(color="#F0F2F6")
    size_of_groups=[deep, light, rem, awake]
    wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    
    plt.figure()
    plt.pie(size_of_groups, 
            colors=[COLORS["sleep_deep"], 
                    COLORS["sleep_light"], 
                    COLORS["sleep_rem"], 
                    COLORS["sleep_awake"],
                    ], 
            startangle=90,
            counterclock=False,
            wedgeprops=wedgeprops)
    
    my_circle=plt.Circle( (0,0), 0.8, color="white")
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    plt.text(0, 0.2, (str(score) + '/100'), fontsize=30, color=COLORS["text"],
             horizontalalignment='center')
    plt.text(0, -.2, 'Quality', fontsize=20, color=COLORS["text"],
             horizontalalignment='center')
    plt.text(0, -.5, 'Good', fontsize=20, color=COLORS["text"],
             horizontalalignment='center')
    
    plt.savefig("assets/sleep_donut.png", transparent=True)
    st.session_state.sleep_donut = img_to_bytes('assets/sleep_donut.png')
    
def spo2_donut():
    
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
                    COLORS['spo2_green'], 
                    COLORS['spo2_low'], 
                    COLORS['spo2_medium'], 
                    COLORS['spo2_high'], 
                    "white"], 
            startangle=270,
            wedgeprops=wedgeprops)
    my_circle=plt.Circle( (0,0), 0.85, color="white")
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    plt.text(0, 0.20, (str(score_mean) + '%'), fontsize=40, color=COLORS['text'],
             horizontalalignment='center')
    plt.text(0, -0.20, 'Lowest', fontsize=20, color=COLORS['text'],
             horizontalalignment='center')
    plt.text(0, -0.50, (str(score_min) + '%'), fontsize=20, color=COLORS['text'],
             horizontalalignment='center')

    # setting the axes projection as polar
    plt.axes(projection = 'polar')
    radius = 0.75

    score_reshape = ((100 - 0)/(100-60)) * (score_mean - 60)
    deg = (270-(4/100*360)) - score_reshape/100*(92/100*360)
    rad = np.deg2rad(deg)

    if score_mean < 70:
        color_spo2_score = COLORS['spo2_high']
    elif 70 <= score_mean < 80:
        color_spo2_score = COLORS['spo2_medium']
    elif 80 <= score_mean < 90:
        color_spo2_score = COLORS['spo2_low']
    elif 90 <= score_mean <= 100:
        color_spo2_score = COLORS['spo2_green']
        
    plt.polar(rad, radius, '.', markersize=75, color=color_spo2_score)
    plt.polar(rad, 1, '.', color="white")
    plt.axis('off')
    
    plt.savefig("assets/spo2_donut.png", transparent=True)
    st.session_state.spo2_donut = img_to_bytes('assets/spo2_donut.png')
    
def steps_donut():
    
    steps           = data.get_steps()
    steps_score     = steps["score"]
    
    color_text = '#3E738D'
    size_of_groups=[steps_score, 100-steps_score]
    wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    plt.close('all')
    plt.figure()
    plt.pie(size_of_groups, 
            colors=['green', "#e8e8e8"], 
            startangle=90,
            counterclock=False,
            wedgeprops=wedgeprops)
    my_circle=plt.Circle( (0,0), 0.8, color="white")
    plt.text(0, 0, (str(steps_score) + '%'), fontsize=40, color=color_text,
             horizontalalignment='center')
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    
    plt.savefig("assets/steps_donut.png", transparent=True)
    st.session_state.steps_donut = img_to_bytes('assets/steps_donut.png')
    
def stress_donut():
    
    stress      = data.get_stress()
    score_mean  = stress["mean"]
    rest        = stress["percentage_rest"]
    low         = stress["percentage_low"]
    medium      = stress["percentage_medium"]
    high        = stress["percentage_high"]
    
    size_of_groups = [rest,low,medium,high]
    wedgeprops = {"linewidth": 1, "edgecolor": "white"}
    plt.close('all')
    plt.figure()
    plt.pie(size_of_groups, 
            colors=[COLORS["stress_rest"], 
                    COLORS["stress_low"], 
                    COLORS["stress_medium"], 
                    COLORS["stress_high"],
                    ], 
            startangle=90,
            counterclock=False,
            wedgeprops=wedgeprops)
    my_circle=plt.Circle( (0,0), 0.85, color="white")
    p=plt.gcf()
    p.gca().add_artist(my_circle)
    plt.text(0, 0.2, (str(score_mean)), fontsize=40, color=COLORS["text"],
             horizontalalignment='center',
             verticalalignment='center')
    plt.text(0, -.3, 'Overall', fontsize=30, color=COLORS["text"],
             horizontalalignment='center')
    
    plt.savefig("assets/stress_donut.png", transparent=True)
    st.session_state.stress_donut = img_to_bytes('assets/stress_donut.png')