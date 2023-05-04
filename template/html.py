import streamlit as st
import template.data as data
import template.chart as chart
from template.version import VERSION
from template.util import img_to_bytes

def head():
    
    html = """
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/css/bootstrap.min.css">
        <script src="https://cdn.jsdelivr.net/npm/jquery@3.6.3/dist/jquery.slim.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>
        <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.8/jquery.min.js"></script>
    </head>
    """
    
    return html

def header():
    translate = st.session_state.translate
    
    html = """
    <div id="top" class='intro_section'>
        <p><img class='intro_logo' src='data:image/png;base64,""" + st.session_state.logo_clife_white + """'/></p>
        <center>
        <p class='intro_style'><b>""" + translate["header_title"] + """</b></p>
        </center>
    </div>
    """
    
    return html

def footer():
    html = """
    <div class="footer">
        <p style="color: grey;">Version
    """
    html += VERSION 
    html +="""
        </p>
    </div>
    """
    
    return html

def language_label():
    translate = st.session_state.translate
    
    
    html = """
    <div>
        <p class='language_label'><b>""" + translate["language_label"] + """</b></p>
    </div>
    """
    
    return html

def profile():
    
    username = st.session_state.username
    
    html = """
    <div class="user_icon_section">
        <p>    
            <img class="user_icon" src='data:image/png;base64,""" + st.session_state.user_icon + """'/>
            <br>
        </p>
        <p>""" + username + """</p>
    </div>
    """
    
    return html

def button_scroll_to_top():
    html = """
    <div id="scrollUp" class="scrollUp">
        <a href="#top"><img src='data:image/png;base64,""" + st.session_state.to_top + """'/></a>
    </div>
    """
    
    return html

def menu_overview():
    
    translate = st.session_state.translate
    
    html = """
    <div class="menu">
        <p>
            <a href="#overview">
                <span>""" + translate["overview"] + """</span>
            </a>
        </p>
    </div>
    """
            
    return html

def menu_smart_textile_raw_data():
    translate = st.session_state.translate
    
    html = """
    <div class="menu">
        <p>
            <a href="#smart_textile_raw_data">
                <span>""" + translate["smart_textile_raw_data"] + """</span>
            </a>
        </p>
    </div>
    """
    
    return html

def menu_health_indicators():
    
    translate = st.session_state.translate
    
    html = """
    <div class="menu">
        <p>
            <a href="#health_indicators">
                <span>""" + translate["health_indicators"] + """</span>
            </a>
        </p>
    </div>
    """
    
    return html

def menu_data_report():
    
    translate = st.session_state.translate
    
    html = """
    <div class="menu">
        <p>
            <a href="#data_report">
                <span>""" + translate["data_report"] + """</span>
            </a>
        </p>
    </div>
    """
    
    return html

def menu_definitions():
    
    translate = st.session_state.translate
    
    html = """
    <div class="menu">
        <p>
            <a href="#definitions">
                <span>""" + translate["definitions"] + """</span>
            </a>
        </p>
    </div>
    """
    
    return html

def overview_title():
    
    translate = st.session_state.translate
    
    html = """
        <div id="overview" class="main_title">
            <p>""" + translate["overview"] + """</p>
        </div>
        <div>
    """
    
    return html

def overview_data_collection():
    
    translate = st.session_state.translate
    
    chronolife_data                 = data.get_duration_chronolife()
    chronolife_duration             = chronolife_data["duration"]
    chronolife_duration_day         = chronolife_data["duration_day"] 
    chronolife_duration_night       = chronolife_data["duration_night"] 
    chronolife_duration_rest        = chronolife_data["duration_rest"]  
    chronolife_duration_activity    = chronolife_data["duration_activity"]

    garmin_data                     = data.get_duration_garmin()
    garmin_duration                 = garmin_data["duration"] 
    garmin_duration_day             = garmin_data["duration_day"] 
    garmin_duration_night           = garmin_data["duration_night"] 
    garmin_duration_rest            = garmin_data["duration_rest"]  
    garmin_duration_activity        = garmin_data["duration_activity"]
    
    col_section     = "col-lg-6 col-sm-12"
    col_title       = "col-12"
    col_logo        = "col-4"
    col_data        = "col-8"
    col_duration    = "col-12"
    col_icon        = "col-2"
    col_key         = "col-5"
    col_val         = "col-5"
    class_val       = "indicator_value"
    
    html = """
        <div class="second_title">
            <p>""" + translate["data_collection"] + """</p>
        </div>
        <div class="row">
            <div class='""" + col_section + """'>
                <div class='overview_section'>
                    <div class="row">
                        <div class='""" + col_title + """'>
                            <p class='indicator_name'>""" + translate["smart_textile"] + """</p>
                        </div>
                    </div>
                    <div class="row overview_sub_section_smart_textile">
                        <div class='""" + col_logo + """'>
                            <img class=device_icon src='data:image/png;base64,""" + st.session_state.tshirt_right + """'/>
                        </div>
                        <div class='""" + col_data + """'>
                            <div class="row data_collection">
                                <div class='""" + col_duration + """'>
                                    <p>""" + translate["total_data"] + """ &ensp; <span class='collect_duration'>""" +\
                                        str(chronolife_duration) + " " + translate["hours"] + """</span></p> 
                                </div>
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.night + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>""" + translate["night"] + """</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(chronolife_duration_day) + " " + translate["hours"] + """</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.day + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>""" + translate["day"] + """</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(chronolife_duration_night) + " " + translate["hours"] + """</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.rest + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>""" + translate["rest"] + """</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(chronolife_duration_rest) + " " + translate["hours"] + """</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.activity + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>""" + translate["activity"] + """</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(chronolife_duration_activity) + " " + translate["hours"] + """</p>
                                </div> 
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class='""" + col_section + """'>
                <div class='overview_section'> 
                    <div class="row">
                        <div class='""" + col_title + """'>
                            <p class='indicator_name'>""" + translate["garmin_watch"] + """</p>
                        </div>
                    </div>
                    <div class="row overview_sub_section_garmin">
                        <div class='""" + col_logo + """'>
                            <img class=device_icon src='data:image/png;base64,""" + st.session_state.garrmin + """'/>
                        </div>
                        <div class='""" + col_data + """'>
                            <div class="row data_collection">
                                <div class='""" + col_duration + """'>
                                    <p>""" + translate["total_data"] + """ &ensp; <span class='collect_duration'>""" +\
                                        str(garmin_duration) + " " + translate["hours"] + """</span></p> 
                                </div>
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.night + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>""" + translate["night"] + """</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(garmin_duration_day) + " " + translate["hours"] + """</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.day + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>""" + translate["day"] + """</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(garmin_duration_night) + " " + translate["hours"] + """</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.rest + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>""" + translate["rest"] + """</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(garmin_duration_rest) + " " + translate["hours"] + """</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.activity + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>""" + translate["activity"] + """</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(garmin_duration_activity) + " " + translate["hours"] + """</p>
                                </div> 
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """
    return html

def overview_health_indicators():
    
    translate = st.session_state.translate
    
    # Heart bpm
    bpm         = data.get_bpm()
    bpm_high    = bpm["high"]
    bpm_rest    = bpm["rest"]
    
    # Heart hrv
    hrv         = data.get_hrv()
    hrv_rest    = hrv["rest"]
    
    # breath brpm
    brpm        = data.get_brpm()
    brpm_high   = brpm["high"]
    brpm_rest   = brpm["rest"]
    
    # breath brv
    brv         = data.get_brv()
    brv_rest    = brpm["rest"]
    
    # ----- Steps
    steps           = data.get_steps()
    steps_number    = steps["number"]
    goal            = steps["goal"]
    distance        = steps["distance"]
    chart.steps_donut()
    
    # Sleep
    sleep = data.get_sleep()
    sleep_duration_deep     = sleep["duration_deep"]
    sleep_duration_light    = sleep["duration_light"]
    sleep_duration_rem      = sleep["duration_rem"]
    sleep_duration_awake    = sleep["duration_awake"]

    sleep_percentage_deep   = sleep["percentage_deep"]
    sleep_percentage_light  = sleep["percentage_light"]
    sleep_percentage_rem    = sleep["percentage_rem"]
    sleep_percentage_awake  = sleep["percentage_awake"]    

    chart.sleep_donut()
    
    # Stress
    stress = data.get_stress()
    stress_duration_rest        = stress["duration_rest"]
    stress_duration_low         = stress["duration_low"]
    stress_duration_medium      = stress["duration_medium"]
    stress_duration_high        = stress["duration_high"]
    
    stress_percentage_rest      = stress["percentage_rest"]
    stress_percentage_low       = stress["percentage_low"]
    stress_percentage_medium    = stress["percentage_medium"]
    stress_percentage_high      = stress["percentage_high"]
    
    chart.stress_donut()
    
    # Pulse Ox
    chart.spo2_donut() 
    
    # Calories
    calories        = data.get_calories()
    calories_total  = calories["total"] 
    calories_rest   = calories["rest"] 
    calories_active = calories["active"] 
    
    # Intensity
    intensity           = data.get_intensity()
    intensity_total     = intensity["total"] 
    intensity_moderate  = intensity["moderate"]
    intensity_vigurous  = intensity["vigurous"]
    
    # Body Battery
    overview_bodybattery = data.get_bodybattery()
    body_bat_high = overview_bodybattery["high"]
    body_bat_low = overview_bodybattery["low"]
    col_section = "col-xl-4 col-lg-6 col-md-6 col-sm-12"
    col_title   = "col-12"
    col_key     = "col-6"
    col_val     = "col-6"
    class_val   = "indicator_value"
    
    html = """
    <div class="second_title">
        <p>""" + translate["health_indicators_overview"] + """</p>
    </div>
    <div class="row">
        <div class='""" + col_section + """'>
            <div class='overview_health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.heart_icon + """'/> 
                        <p class='indicator_name'>""" + translate["cardiology"] + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["tachycardia"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p><img class=miniicon src='data:image/png;base64,""" + st.session_state.tachycardia_alert_icon + """'/></p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["bradycardia"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p><img class=miniicon src='data:image/png;base64,""" + st.session_state.bradycardia_alert_icon + """'/> </p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["qt_anomaly"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p><img class=miniicon src='data:image/png;base64,""" + st.session_state.qt_alert_icon + """'/> </p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["hr_high"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(bpm_high) + """ bpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["hr_resting"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(bpm_rest) + """ bpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["hrv_resting"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(hrv_rest) + """ ms</p>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='overview_health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.breath_icon + """'/> 
                        <p class='indicator_name'>""" + translate["respiratory"] + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["tachypnea"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p><img class=miniicon src='data:image/png;base64,""" + st.session_state.tachypnea_alert_icon + """'/> </p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["bradypnea"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p><img class=miniicon src='data:image/png;base64,""" + st.session_state.bradypnea_alert_icon + """'/> </p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["br_high"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brpm_high) + """ brpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["br_resting"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brpm_rest) + """ brpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["brv_resting"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brv_rest) + """ s</p>
                        <br>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='overview_health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.pulseox_icon + """'/> 
                        <p class='indicator_name'>""" + translate["pulseox"] + """</p>
                    </div>
                    <div class="col-6">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.spo2_green + """'/>
                            <p>90 - 100 %</p>
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.spo2_yellow + """'/>
                            <p>80 - 89 %</p>
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.spo2_orange + """'/>
                            <p>70 - 79 %</p>
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.spo2_red + """'/>
                            <p>< 70 %</p>
                    </div>
                    <div class="col-6">
                        <img class=donut src='data:image/png;base64,""" + st.session_state.spo2_donut + """'/> 
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='overview_health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.steps_icon + """'/> 
                        <p class='indicator_name'>""" + translate["steps"] + """</p>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>""" + translate["number"] + """</p>
                            </div>    
                            <div class="col-12">
                                <p class='steps_number'>""" + str(steps_number) + """</p>
                            </div>
                            <div class="col-12">
                                <p>""" + translate["goal"] + """</p>
                            </div>
                            <div class="col-12">
                                <p><b>""" + str(goal) + """</b></p>
                            </div>
                            <div class="col-12">
                                <p>""" + translate["distance"] + """</p>
                            </div>
                            <div class="col-12">
                                <p><b>""" + str(distance) + """ km</b></p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <center>
                            <img class=donut src='data:image/png;base64,""" + st.session_state.steps_donut + """'/> 
                        </center>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='overview_health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.stress_icon + """'/> 
                        <p class='indicator_name'>""" + translate["stress"] + """</p>
                    </div>
                    <div class="col-7">
                        <div class="row">
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_rest + """'/> 
                                <p>
                                    """ + translate["rest"] + """ <br>
                                    <span class='""" + class_val + """'>""" + str(stress_duration_rest) + """ min (""" + str(stress_percentage_rest) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_low + """'/>
                                <p>
                                    """ + translate["low"] + """ <br>
                                    <span class='""" + class_val + """'>""" + str(stress_duration_low) + """ min (""" + str(stress_percentage_low) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_medium + """'/>
                                <p>
                                    """ + translate["medium"] + """ <br>
                                    <span class='""" + class_val + """'>""" + str(stress_duration_medium) + """ min (""" + str(stress_percentage_medium) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_high + """'/>
                                <p>
                                    """ + translate["high"] + """ <br>
                                    <span class='""" + class_val + """'>""" + str(stress_duration_high) + """ min (""" + str(stress_percentage_high) + """%)</span>
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-5">
                        <center>
                            <img class=donut src='data:image/png;base64,""" + st.session_state.stress_donut + """'/> 
                        </center>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='overview_health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.sleep_icon + """'/> 
                        <p class='indicator_name'>""" + translate["sleep"] + """</p>
                    </div>
                    <div class="col-7">
                        <div class="row">
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_deep + """'/>
                                <p>
                                    """ + translate["deep"] + """ <br>
                                    <span class='""" + class_val + """'>""" + str(sleep_duration_deep) + """ min (""" + str(sleep_percentage_deep) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_light + """'/>
                                <p>
                                    """ + translate["light"] + """ <br>
                                    <span class='""" + class_val + """'>""" + str(sleep_duration_light) + """ min (""" + str(sleep_percentage_light) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_rem + """'/>
                                <p>
                                    """ + translate["rem"] + """ <br>
                                    <span class='""" + class_val + """'>""" + str(sleep_duration_rem) + """ min (""" + str(sleep_percentage_rem) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_awake + """'/>
                                <p>
                                    """ + translate["awake"] + """ <br>
                                    <span class='""" + class_val + """'>""" + str(sleep_duration_awake) + """ min (""" + str(sleep_percentage_awake) + """%)</span>  
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="col-5">
                        <center>
                            <img class=donut src='data:image/png;base64,""" + st.session_state.sleep_donut + """'/> 
                        </center>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='overview_health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.calories_icon + """'/> 
                        <p class='indicator_name'>""" + translate["calories"] + """</p>
                    </div>
                    <div class="col-12">
                        <div class="row">
                            <div class="col-12">
                                <p>""" + translate["calories_total"] + """</p>
                            </div>
                            <div class="col-12">
                                <p class='total_calories'>""" + str(calories_total) + """ kcals</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>""" + translate["calories_active"] + """</p>
                            </div>
                            <div class="col-12">
                                <p class='""" + class_val + """'>""" + str(calories_rest) + """ kcals</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>""" + translate["calories_resting"] + """</p>
                            </div>
                            <div class="col-12">
                                <p class='""" + class_val + """'>""" + str(calories_active) + """ kcals</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='overview_health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.intensity_icon + """'/> 
                        <p class='indicator_name'>""" + translate["intensity"] + """</p>
                    </div>
                    <div class="col-12">
                        <div class="row">
                            <div class="col-12">
                                <p>""" + translate["intensity_total"] + """</p>
                            </div>
                            <div class="col-12">
                                <p class='total_intensity_minutes'>""" + str(intensity_total) + """ min</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>""" + translate["intensity_moderate"] + """</p>
                            </div>
                            <div class="col-12">
                                <p class='""" + class_val + """'>""" + str(intensity_moderate) + """ min</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>""" + translate["intensity_vigurous"] + """</p>
                            </div>
                            <div class="col-12">
                                <p class='""" + class_val + """'>""" + str(intensity_vigurous) + """ min</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='overview_health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.bodybattery_icon + """'/> 
                        <p class='indicator_name'>""" + translate["bodybattery"] + """</p>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>""" + translate["high"] + """</p>
                            </div>
                            <div class="col-12">
                                <p class='body_battery_scores'>""" + str(body_bat_high) + """%</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>""" + translate["low"] + """</p>
                            </div>
                            <div class="col-12">
                                <p class='body_battery_scores'>""" + str(body_bat_low) + """%</p>
                                <br>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
        """
    
    return html

    
def smart_textile_raw_data_title():
    
    translate = st.session_state.translate
    
    html = """
    <div id="smart_textile_raw_data" class="main_title">
        <p>""" + translate["smart_textile_raw_data_title"] + """</p>
    </div>
    """
    
    return html

def smart_textile_raw_data_download():
    
    translate = st.session_state.translate
    
    html = """
    <div>
        <p>""" + translate["smart_textile_raw_data_download"] + """</p> 
    </div>
    """

    return html

def health_indicators_title():
    
    translate = st.session_state.translate
    
    html = """
    <div id="health_indicators" class="main_title">
        <p>""" + translate["health_indicators"] + """</p>
    </div>
    """
    
    return html

def health_indicators_download():
    
    translate = st.session_state.translate
    
    html = """
    <div>
        <p>""" + translate["health_indicators_download"] + """</p>
    </div>
    """
    
    return html
    

def health_indicators_heart_bpm_title():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.heart_icon + """'/> 
        <p>""" + translate["health_indicators_heart_bpm_title"] + """</p>
    </div>
    """
    
    return html

def health_indicators_heart_bpm_results():
    
    translate = st.session_state.translate
    
    bpm         = data.get_bpm()
    bpm_mean    = bpm["mean"]
    bpm_min     = bpm["min"]
    bpm_max     = bpm["max"]
    
    html = """
    <div class=col1_indicators>
        <p>""" + translate["median"] + """</p>
        <p class="indicator_main_value">""" + str(bpm_mean) + """ bpm</p>
        <p>""" + translate["min"] + """</p>
        <p class="indicator_value">""" + str(bpm_min) + """ bpm</p>
        <p>""" + translate["max"] + """</p>
        <p class="indicator_value">""" + str(bpm_max) + """ bpm</p>
    </div>
    """
    
    return html

def health_indicators_heart_hrv_title():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.heart_icon + """'/> 
        <p>""" + translate["health_indicators_heart_hrv_title"] + """</p>
    </div>
    """
    
    return html

def health_indicators_heart_hrv_results():
    
    translate = st.session_state.translate
    
    hrv         = data.get_hrv()
    hrv_mean    = hrv["mean"]
    hrv_min     = hrv["min"]
    hrv_max     = hrv["max"]
    
    html = """
    <div class=col1_indicators>
        <p>""" + translate["median"] + """</p>
        <p class="indicator_main_value">""" + str(hrv_mean) + """ bpm</p>
        <p>""" + translate["min"] + """</p>
        <p class="indicator_value">""" + str(hrv_min) + """ bpm</p>
        <p>""" + translate["max"] + """</p>
        <p class="indicator_value">""" + str(hrv_max) + """ bpm</p>
    </div>
    """
    
    return html

def health_indicators_heart_tachy_brady_qt():
    
    translate = st.session_state.translate
    
    tachycardia         = data.get_tachycardia()
    tachy_mean          = tachycardia["mean"]
    tachy_duration      = tachycardia["duration"]
    tachy_percentage    = tachycardia["percentage"]
    
    bradycardia         = data.get_bradycardia()
    brady_mean          = bradycardia["mean"]
    brady_duration      = bradycardia["duration"]
    brady_percentage    = bradycardia["percentage"]
    
    qt = data.get_qt()
    qt_mean             = qt["mean"]
    qt_min              = qt["min"]
    qt_max              = qt["max"]
    
    col_section = "col-lg-4 col-md-6 col-sm-12"
    col_title   = "col-12"
    col_key     = "col-4"
    col_val     = "col-8"
    class_val   = "indicator_value"
    
    html = """
    <div class="row">
        <div class='""" + col_section + """'>
            <div class='health_section'>
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.tachycardia_alert_icon + """'/> 
                        <p class='indicator_name'>""" + translate["tachycardia"] + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["hr"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(tachy_mean) + """ bpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["duration"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(tachy_duration) + """ min</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["proportion"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(tachy_percentage) + """ %</p>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.tachycardia_alert_icon + """'/> 
                        <p class='indicator_name'>""" + translate["bradycardia"] + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["hr"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brady_mean) + """ bpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["duration"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brady_duration) + """ min</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["proportion"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brady_percentage) + """ %</p>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.qt_alert_icon + """'/> 
                        <p class='indicator_name'>""" + translate["qt_length"] + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["median"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(qt_mean) + """ ms</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["min"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(qt_min) + """ ms</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>""" + translate["max"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(qt_max) + """ ms</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def health_indicators_breath_brpm_title():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.breath_icon + """'/> 
        <p>""" +  translate["health_indicators_breath_brpm_title"] + """</p>
    </div>
    """
    
    return html

def health_indicators_breath_brpm_results():
    
    translate = st.session_state.translate
    
    brpm         = data.get_brpm()
    brpm_mean    = brpm["mean"]
    brpm_min     = brpm["min"]
    brpm_max     = brpm["max"]
    
    html = """
    <div class=col1_indicators>
        <p>""" + translate["median"] + """</p>
        <p class="indicator_main_value">""" + str(brpm_mean) + """ brpm</p>
        <p>""" + translate["min"] + """</p>
        <p class="indicator_value">""" + str(brpm_min) + """ brpm</p>
        <p>""" + translate["max"] + """</p>
        <p class="indicator_value">""" + str(brpm_max) + """ brpm</p>
    </div>
    """
    
    return html

def health_indicators_breath_brv_title():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.breath_icon + """'/> 
        <p>""" + translate["health_indicators_breath_brv_title"] + """</p>
    </div>
    """
    
    return html

def health_indicators_breath_brv_results():
    
    translate = st.session_state.translate
    
    brv         = data.get_brv()
    brv_mean    = brv["mean"]
    brv_min     = brv["min"]
    brv_max     = brv["max"]
    
    html = """
    <div class=col1_indicators>
        <p>""" + translate["median"] + """</p>
        <p class="indicator_main_value">""" + str(brv_mean) + """ s</p>
        <p>""" + translate["min"] + """</p>
        <p class="indicator_value">""" + str(brv_min) + """ s</p>
        <p>""" + translate["max"] + """</p>
        <p class="indicator_value">""" + str(brv_max) + """ s</p>
    </div>
    """
    
    return html

def health_indicators_breath_tachy_brady_inexratio():
    
    translate = st.session_state.translate
    
    tachypnea = data.get_tachypnea()
    tachy_mean          = tachypnea["mean"]
    tachy_duration      = tachypnea["duration"]
    tachy_percentage    = tachypnea["percentage"]
    
    bradypnea = data.get_bradypnea()
    brady_mean          = bradypnea["mean"]
    brady_duration      = bradypnea["duration"]
    brady_percentage    = bradypnea["percentage"]
    
    inexratio           = data.get_inexratio()
    inexratio_mean      = inexratio["mean"]
    inexratio_min       = inexratio["min"]
    inexratio_max       = inexratio["max"]
    
    col_section = "col-lg-4 col-md-6 col-sm-12"
    col_title   = "col-12"
    col_key     = "col-4"
    col_val     = "col-8"
    class_val   = "indicator_value"
    
    html = """
    <div class="row">
        <div class='""" + col_section + """'>
            <div class='health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.tachypnea_alert_icon + """'/> 
                        <p class='indicator_name'>"""+ translate["tachypnea"] + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>"""+ translate["br"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(tachy_mean) + """ brpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>"""+ translate["duration"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(tachy_duration) + """ min</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>"""+ translate["proportion"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(tachy_percentage) + """ %</p>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.tachypnea_alert_icon + """'/> 
                        <p class='indicator_name'>"""+ translate["bradypnea"] + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>"""+ translate["br"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brady_mean) + """ brpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>"""+ translate["duration"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brady_duration) + """ min</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>"""+ translate["proportion"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brady_percentage) + """ %</p>
                    </div>
                </div>
            </div>
        </div>
        <div class='""" + col_section + """'>
            <div class='health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.qt_alert_icon + """'/> 
                        <p class='indicator_name'>"""+ translate["inout_length_ratio"] + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>"""+ translate["median"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(inexratio_mean) + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>"""+ translate["min"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(inexratio_min) + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>"""+ translate["max"] + """</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(inexratio_max) + """</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def health_indicators_stress_title():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.stress_icon + """'/> 
        <p>""" + translate["stress"] + """</p>
    </div>
    """
    
    return html

def health_indicators_stress_results():
    
    translate = st.session_state.translate
    
    stress         = data.get_stress()
    stress_duration_rest        = stress["duration_rest"]
    stress_duration_low         = stress["duration_low"]
    stress_duration_medium      = stress["duration_medium"]
    stress_duration_high        = stress["duration_high"]
    
    stress_percentage_rest      = stress["percentage_rest"]
    stress_percentage_low       = stress["percentage_low"]
    stress_percentage_medium    = stress["percentage_medium"]
    stress_percentage_high      = stress["percentage_high"]
    
    class_val   = "indicator_value"
    
    html = """
    <div class='col-12'>
        <div class='health_section'> 
            <div class="row">
                <div class="col-7">
                    <div class="row">
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_rest + """'/> 
                            <p>
                                """ + translate["rest"] + """ <br>
                                <span class='""" + class_val + """'>""" + str(stress_duration_rest) + """ min (""" + str(stress_percentage_rest) + """%)</span>
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_low + """'/>
                            <p>
                                """ + translate["low"] + """ <br>
                                <span class='""" + class_val + """'>""" + str(stress_duration_low) + """ min (""" + str(stress_percentage_low) + """%)</span>
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_medium + """'/>
                            <p>
                                """ + translate["medium"] + """ <br>
                                <span class='""" + class_val + """'>""" + str(stress_duration_medium) + """ min (""" + str(stress_percentage_medium) + """%)</span>
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_high + """'/>
                            <p>
                                """ + translate["high"] + """ <br>
                                <span class='""" + class_val + """'>""" + str(stress_duration_high) + """ min (""" + str(stress_percentage_high) + """%)</span>
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-5">
                    <center>
                        <img class=donut src='data:image/png;base64,""" + st.session_state.stress_donut + """'/> 
                    </center>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def health_indicators_pulseox_title():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.pulseox_icon + """'/> 
        <p>""" + translate["pulseox"] + """</p>
    </div>
    """
    
    return html

def health_indicators_pulseox_results():
    
    html = """
    <div class='col-12'>
        <div class='health_section'> 
            <div class="row">
                <div class="col-6">
                        <img class=coloricon src='data:image/png;base64,""" + st.session_state.spo2_green + """'/>
                        <p>90 - 100 %</p>
                        <img class=coloricon src='data:image/png;base64,""" + st.session_state.spo2_yellow + """'/>
                        <p>80 - 89 %</p>
                        <img class=coloricon src='data:image/png;base64,""" + st.session_state.spo2_orange + """'/>
                        <p>70 - 79 %</p>
                        <img class=coloricon src='data:image/png;base64,""" + st.session_state.spo2_red + """'/>
                        <p>< 70 %</p>
                </div>
                <div class="col-6">
                    <img class=donut src='data:image/png;base64,""" + st.session_state.spo2_donut + """'/> 
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def health_indicators_bodybattery_title():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.bodybattery_icon + """'/> 
        <p>""" + translate["bodybattery"] + """</p>
    </div>
    """
    
    return html

def health_indicators_bodybattery_results():
    
    translate = st.session_state.translate
    
    bodybattery         = data.get_bodybattery()
    bodybattery_high    = bodybattery["high"]
    bodybattery_low     = bodybattery["low"]
    
    html = """
    <div class=col1_indicators>
        <p>""" + translate["high"] + """</p>
        <p class="indicator_main_value">""" + str(bodybattery_high) + """ </p>
        <p>""" + translate["low"] + """</p>
        <p class="indicator_value">""" + str(bodybattery_low) + """</p>
    </div>
    """
    
    return html

def health_indicators_sleep_title():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.sleep_icon + """'/> 
        <p>""" + translate["sleep"] + """</p>
    </div>
    """
    
    return html

def health_indicators_sleep_results():
    
    translate = st.session_state.translate
    
    sleep         = data.get_sleep()
    sleep_duration_deep     = sleep["duration_deep"]
    sleep_duration_light    = sleep["duration_light"]
    sleep_duration_rem      = sleep["duration_rem"]
    sleep_duration_awake    = sleep["duration_awake"]

    sleep_percentage_deep   = sleep["percentage_deep"]
    sleep_percentage_light  = sleep["percentage_light"]
    sleep_percentage_rem    = sleep["percentage_rem"]
    sleep_percentage_awake  = sleep["percentage_awake"]    
    
    class_val               = "indicator_value"
    
    html = """
    <div class='col-12'>
        <div class='health_section'> 
            <div class="row">
                <div class="col-7">
                    <div class="row">
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_deep + """'/>
                            <p>
                                """ + translate["deep"] + """ <br>
                                <span class='""" + class_val + """'>""" + str(sleep_duration_deep) + """ min (""" + str(sleep_percentage_deep) + """%)</span> 
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_light + """'/>
                            <p>
                                """ + translate["light"] + """ <br>
                                <span class='""" + class_val + """'>""" + str(sleep_duration_light) + """ min (""" + str(sleep_percentage_light) + """%)</span>
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_rem + """'/>
                            <p>
                                """ + translate["rem"] + """ <br>
                                <span class='""" + class_val + """'>""" + str(sleep_duration_rem) + """ min (""" + str(sleep_percentage_rem) + """%)</span>
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_awake + """'/>
                            <p>
                                """ + translate["awake"] + """ <br>
                                <span class='""" + class_val + """'>""" + str(sleep_duration_awake) + """ min (""" + str(sleep_percentage_awake) + """%)</span> 
                            </p>
                        </div>
                    </div>
                </div>
                <div class="col-5">
                    <center>
                        <img class=donut src='data:image/png;base64,""" + st.session_state.sleep_donut + """'/> 
                    </center>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def health_indicators_temperature_title():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.temperature_icon + """'/> 
        <p>""" + translate["health_indicators_temperature_title"] + """</p>
    </div>
    """
    
    return html

def health_indicators_temperature_results():
    
    translate = st.session_state.translate
    
    temperature         = data.get_temperature()
    temperature_mean    = temperature["mean"]
    temperature_min     = temperature["min"]
    temperature_max     = temperature["max"]
    
    html = """
    <div class=col1_indicators>
        <p>""" + translate["median"] + """</p>
        <p class="indicator_main_value">""" + str(temperature_mean) + """ °C</p>
        <p>""" + translate["min"] + """</p>
        <p class="indicator_value">""" + str(temperature_min) + """ °C</p>
        <p>""" + translate["max"] + """</p>
        <p class="indicator_value">""" + str(temperature_max) + """ °C</p>
    </div>
    """
    
    return html

def data_report_title():
    
    translate = st.session_state.translate
    
    html = """
    <div id="data_report" class="main_title">
        <p>""" + translate["data_report"] + """</p>
    </div>
    """
    
    return html


def data_report_download():
    
    translate = st.session_state.translate
    
    html = """
    <div>
        <p>""" + translate["data_report_download"] + """</p>
    </div>
    """
    
    return html

def definitions_title():
    
    translate = st.session_state.translate
    
    html = """
    <div id="definitions" class="main_title">
        <p>""" + translate["definitions"] + """</p>
    </div>
    """
    
    return html

def definitions_period_and_activity():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <p>""" + translate["period_and_activity"] + """</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-5">
                <div class="col-lg-12">
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.night + """'/> 
                    <p><b>""" + translate["night"] + """</b>: """ + translate["definition_activity_night"] + """</p>
                </div>
                <div class='col-lg-12'>
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.day + """'/> 
                    <p><b>""" + translate["day"] + """</b>: """ + translate["definition_activity_day"] + """</p>
                </div>
            </div>
            <div class="col-lg-7">
                <div class="col-lg-12">
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.rest + """'/> 
                    <p><b>""" + translate["rest"] + """</b>: """ + translate["definition_activity_rest"] + """</p>
                </div>
                <div class="col-lg-12">
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.activity + """'/> 
                    <p><b>""" + translate["activity"] + """</b>: """ + translate["definition_activity_activity"] + """</p>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html
   
def definitions_alert():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <p>""" + translate["alert"] + """</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <div class="col-lg-12">
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.alert + """'/> 
                    <p>""" + translate["definition_alert_red"] + """</p>
                </div>
                <div class='col-lg-12'>
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.alert_no + """'/> 
                    <p>""" + translate["definition_alert_green"] + """</p>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_heart():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <p>""" + translate["cardiology"] + """</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>""" + translate["health_indicators_heart_bpm_title"] + """</b>
                    <br>
                    """ + translate["definition_bpm"] + """
                </p>
                <p>
                    <b>""" + translate["hr_resting"] + """</b>
                    <br>
                    """ + translate["definition_hr_resting"] + """
                </p>
                <p>
                    <b>""" + translate["hr_high"] + """</b>
                    <br>
                    """ + translate["definition_hr_high"] + """
                </p>
                <p>
                    <b>""" + translate["health_indicators_heart_hrv_title"] + """</b>
                    <br>
                    """ + translate["definition_hrv"] + """
                </p>
                <p>
                    <b>""" + translate["hrv_resting"] + """</b>
                    <br>
                    """ + translate["definition_hrv_resting"] + """
                </p>
                <p>
                    <b>""" + translate["qt_length"] + """</b>
                    <br>
                    """ + translate["definition_qt_length"] + """
                </p>
                <p>
                    <b>""" + translate["tachycardia"] + """</b>
                    <br>
                    """ + translate["definition_tachycardia"] + """
                </p>
                <p>
                    <b>""" + translate["bradycardia"] + """</b>
                    <br>
                    """ + translate["definition_bradycardia"] + """
                </p>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_breath():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <p>Respiratory Indicators</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>""" + translate["health_indicators_breath_brpm_title"] + """</b>
                    <br>
                    """ + translate["definition_brpm"] + """
                </p>
                <p>
                    <b>""" + translate["br_resting"] + """</b>
                    <br>
                    """ + translate["definition_br_resting"] + """
                </p>
                <p>
                    <b>""" + translate["br_high"] + """</b>
                    <br>
                    """ + translate["definition_br_high"] + """
                </p>
                <p>
                    <b>""" + translate["health_indicators_breath_brv_title"] + """</b>
                    <br>
                    """ + translate["definition_brv"] + """
                </p>
                <p>
                    <b>""" + translate["brv_resting"] + """</b>
                    <br>
                    """ + translate["definition_brv_resting"] + """
                </p>
                <p>
                    <b>""" + translate["tachypnea"] + """</b>
                    <br>
                    """ + translate["definition_tachypnea"] + """
                </p>
                <p>
                    <b>""" + translate["bradypnea"] + """</b>
                    <br>
                    """ + translate["definition_bradypnea"] + """
                </p>
                <p>
                    <b>""" + translate["inout_length_ratio"] + """</b>
                    <br>
                    """ + translate["definition_inout_length_ratio"] + """
                </p>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_stress():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <p>""" + translate["stress"] + """</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>""" + translate["stress_score"] + """</b>
                    <br>
                    """ + translate["definition_stress_score"] + """
                </p>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_pulseox():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <p>""" + translate["pulseox"] + """</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>""" + translate["spo2"] + """</b>
                    <br>
                    """ + translate["definition_spo2"] + """
                </p>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_bodybattery():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <p>""" + translate["bodybattery"] + """</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>""" + translate["bodybattery"] + """</b>
                    <br>
                    """ + translate["definition_bodybattery"] + """
                </p>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_sleep():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <p>""" + translate["sleep"] + """</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>""" + translate["sleep_quality"] + """</b>
                    <br>
                    """ + translate["definition_sleep_quality"] + """
                </p>
            </div>
        </div>
    </div>
    """
    
    return html
    
def definitions_temp():
    
    translate = st.session_state.translate
    
    html = """
    <div class="second_title">
        <p>""" + translate["temperature"] + """</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>""" + translate["health_indicators_temperature_title"] + """</b>
                    <br>
                    """ + translate["definition_skin_temperature"] + """
                </p>
            </div>
        </div>
    </div>
    """
    
    return html