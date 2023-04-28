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
    
    html = """
    <div id="top" class='intro_section'>
        <p><img class='intro_logo' src='data:image/png;base64,""" + st.session_state.logo_clife_white + """'/></p>
        <center>
        <p class='intro_style'><b>Smart Textile Dashboard</b></p>
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
    html = """
    <div class="menu">
        <p>
            <a href="#overview">
                <span>Overview</span>
            </a>
        </p>
    </div>
    """
            
    return html

def menu_smart_textile_raw_data():
    html = """
    <div class="menu">
        <p>
            <a href="#smart_textile_raw_data">
                <span>Smart Textile Raw Data</span>
            </a>
        </p>
    </div>
    """
    
    return html

def menu_health_indicators():
    html = """
    <div class="menu">
        <p>
            <a href="#health_indicators">
                <span>Health Indicators</span>
            </a>
        </p>
    </div>
    """
    
    return html

def menu_data_report():
    html = """
    <div class="menu">
        <p>
            <a href="#data_report">
                <span>Data Report</span>
            </a>
        </p>
    </div>
    """
    
    return html

def menu_definitions():
    html = """
    <div class="menu">
        <p>
            <a href="#definitions">
                <span>Definitions</span>
            </a>
        </p>
    </div>
    """
    
    return html

def overview_title():
    
    html = """
        <div id="overview" class="main_title">
            <p>Overview</p>
        </div>
        <div>
    """
    
    return html

def overview_data_collection():
    
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
            <p>Data Collection</p>
        </div>
        <div class="row">
            <div class='""" + col_section + """'>
                <div class='overview_section'>
                    <div class="row">
                        <div class='""" + col_title + """'>
                            <p class='indicator_name'>Smart Textile</p>
                        </div>
                    </div>
                    <div class="row overview_sub_section_smart_textile">
                        <div class='""" + col_logo + """'>
                            <img class=device_icon src='data:image/png;base64,""" + st.session_state.tshirt_right + """'/>
                        </div>
                        <div class='""" + col_data + """'>
                            <div class="row data_collection">
                                <div class='""" + col_duration + """'>
                                    <p>Total data &ensp; <span class='collect_duration'>""" + str(chronolife_duration) + """ hours</span></p> 
                                </div>
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.night + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>Night</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(chronolife_duration_day) + """ hours</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.day + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>Day</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(chronolife_duration_night) + """ hours</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.rest + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>Rest</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(chronolife_duration_rest) + """ hours</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.activity + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>Activity</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(chronolife_duration_activity) + """ hours</p>
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
                            <p class='indicator_name'>Garmin watch</p>
                        </div>
                    </div>
                    <div class="row overview_sub_section_garmin">
                        <div class='""" + col_logo + """'>
                            <img class=device_icon src='data:image/png;base64,""" + st.session_state.garrmin + """'/>
                        </div>
                        <div class='""" + col_data + """'>
                            <div class="row data_collection">
                                <div class='""" + col_duration + """'>
                                    <p>Total data &ensp; <span class='collect_duration'>""" + str(garmin_duration) + """ hours</span></p> 
                                </div>
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.night + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>Night</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(garmin_duration_day) + """ hours</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.day + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>Day</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(garmin_duration_night) + """ hours</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.rest + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>Rest</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(garmin_duration_rest) + """ hours</p>
                                </div> 
                                <div class='""" + col_icon + """'>
                                    <img class=miniicon src='data:image/png;base64,""" + st.session_state.activity + """'/> 
                                </div>
                                <div class='""" + col_key + """'>
                                    <p>Activity</p>
                                </div> 
                                <div class='""" + col_val + """'>
                                    <p class='""" + class_val + """'>""" + str(garmin_duration_activity) + """ hours</p>
                                </div> 
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """
    return html

def overview_duration_title():
    
    html = """
    <div class="second_title">
        <p>Duration Of Data Collection</p>
    </div>
    """
    
    return html

def overview_health_indicators():
    
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
    intensity_vigorous  = intensity["vigorous"]
    
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
        <p>Health Indicators Overview</p>
    </div>
    <div class="row">
        <div class='""" + col_section + """'>
            <div class='overview_health_section'> 
                <div class="row">
                    <div class='""" + col_title + """'>
                        <img class=icon src='data:image/png;base64,""" + st.session_state.heart_icon + """'/> 
                        <p class='indicator_name'>Cardiology</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Tachycardia</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p><img class=miniicon src='data:image/png;base64,""" + st.session_state.tachycardia_alert_icon + """'/></p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Bradycardia</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p><img class=miniicon src='data:image/png;base64,""" + st.session_state.bradycardia_alert_icon + """'/> </p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>QT Length anomaly </p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p><img class=miniicon src='data:image/png;base64,""" + st.session_state.qt_alert_icon + """'/> </p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>HR high</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(bpm_high) + """ bpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>HR resting</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(bpm_rest) + """ bpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>HRV resting</p>
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
                        <p class='indicator_name'>Respiratory</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Tachypnea</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p><img class=miniicon src='data:image/png;base64,""" + st.session_state.tachypnea_alert_icon + """'/> </p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Bradypnea</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p><img class=miniicon src='data:image/png;base64,""" + st.session_state.bradypnea_alert_icon + """'/> </p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>BR high</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brpm_high) + """ brpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>BR resting</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brpm_rest) + """ brpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>BRV resting</p>
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
                        <p class='indicator_name'>Pulse Ox</p>
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
                        <p class='indicator_name'>Steps</p>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>Number</p>
                            </div>    
                            <div class="col-12">
                                <p class='steps_number'>""" + str(steps_number) + """</p>
                            </div>
                            <div class="col-12">
                                <p>Goal</p>
                            </div>
                            <div class="col-12">
                                <p><b>""" + str(goal) + """</b></p>
                            </div>
                            <div class="col-12">
                                <p>Distance</p>
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
                        <p class='indicator_name'>Stress</p>
                    </div>
                    <div class="col-7">
                        <div class="row">
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_rest + """'/> 
                                <p>
                                    Rest <br>
                                    <span class='""" + class_val + """'>""" + str(stress_duration_rest) + """ min (""" + str(stress_percentage_rest) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_low + """'/>
                                <p>
                                    Low <br>
                                    <span class='""" + class_val + """'>""" + str(stress_duration_low) + """ min (""" + str(stress_percentage_low) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_medium + """'/>
                                <p>
                                    Medium <br>
                                    <span class='""" + class_val + """'>""" + str(stress_duration_medium) + """ min (""" + str(stress_percentage_medium) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_high + """'/>
                                <p>
                                    High <br>
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
                        <p class='indicator_name'>Sleep</p>
                    </div>
                    <div class="col-7">
                        <div class="row">
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_deep + """'/>
                                <p>
                                    Deep <br>
                                    <span class='""" + class_val + """'>""" + str(sleep_duration_deep) + """ min (""" + str(sleep_percentage_deep) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_light + """'/>
                                <p>
                                    Light <br>
                                    <span class='""" + class_val + """'>""" + str(sleep_duration_light) + """ min (""" + str(sleep_percentage_light) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_rem + """'/>
                                <p>
                                    REM <br>
                                    <span class='""" + class_val + """'>""" + str(sleep_duration_rem) + """ min (""" + str(sleep_percentage_rem) + """%)</span>
                                </p>
                            </div>
                            <div class="col-12">
                                <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_awake + """'/>
                                <p>
                                    Awake <br>
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
                        <p class='indicator_name'>Calories</p>
                    </div>
                    <div class="col-12">
                        <div class="row">
                            <div class="col-12">
                                <p>Number of total calories</p>
                            </div>
                            <div class="col-12">
                                <p class='total_calories'>""" + str(calories_total) + """ kcals</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>Active</p>
                            </div>
                            <div class="col-12">
                                <p class='""" + class_val + """'>""" + str(calories_rest) + """ kcals</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>Resting</p>
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
                        <p class='indicator_name'>Intensity Minutes</p>
                    </div>
                    <div class="col-12">
                        <div class="row">
                            <div class="col-12">
                                <p>Total Intensity Minutes</p>
                            </div>
                            <div class="col-12">
                                <p class='total_intensity_minutes'>""" + str(intensity_total) + """ min</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>Moderate</p>
                            </div>
                            <div class="col-12">
                                <p class='""" + class_val + """'>""" + str(intensity_moderate) + """ min</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>Vigorous</p>
                            </div>
                            <div class="col-12">
                                <p class='""" + class_val + """'>""" + str(intensity_vigorous) + """ min</p>
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
                        <p class='indicator_name'>Body Battery</p>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>High</p>
                            </div>
                            <div class="col-12">
                                <p class='body_battery_scores'>""" + str(body_bat_high) + """%</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="row">
                            <div class="col-12">
                                <p>Low</p>
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
    
    html = """
    <div id="smart_textile_raw_data" class="main_title">
        <p>Smart <span class="orange_text">Textile</span> Raw Data</p>
    </div>
    """
    
    return html

def smart_textile_raw_data_download():
    
    html = """
    <div>
        <p>Download the Smart Textile Raw Data (XLS)</p>
    </div>
    """

    return html

def health_indicators_title():
    
    html = """
    <div id="health_indicators" class="main_title">
        <p>Health Indicators</p>
    </div>
    """
    
    return html

def health_indicators_download():
    
    html = """
    <div>
        <p>Download the daily health indicators (XLS)</p>
    </div>
    """
    
    return html
    

def health_indicators_heart_bpm_title():
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.heart_icon + """'/> 
        <p>Heart Beat Per Minute (BPM)</p>
    </div>
    """
    
    return html

def health_indicators_heart_bpm_results():
    
    bpm         = data.get_bpm()
    bpm_mean    = bpm["mean"]
    bpm_min     = bpm["min"]
    bpm_max     = bpm["max"]
    
    html = """
    <div class=col1_indicators>
        <p>Median</p>
        <p class="indicator_main_value">""" + str(bpm_mean) + """ bpm</p>
        <p>Min</p>
        <p class="indicator_value">""" + str(bpm_min) + """ bpm</p>
        <p>Max</p>
        <p class="indicator_value">""" + str(bpm_max) + """ bpm</p>
    </div>
    """
    
    return html

def health_indicators_heart_hrv_title():
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.heart_icon + """'/> 
        <p>Heart Rate Variability (HRV)</p>
    </div>
    """
    
    return html

def health_indicators_heart_hrv_results():
    
    hrv         = data.get_hrv()
    hrv_mean    = hrv["mean"]
    hrv_min     = hrv["min"]
    hrv_max     = hrv["max"]
    
    html = """
    <div class=col1_indicators>
        <p>Median</p>
        <p class="indicator_main_value">""" + str(hrv_mean) + """ bpm</p>
        <p>Min</p>
        <p class="indicator_value">""" + str(hrv_min) + """ bpm</p>
        <p>Max</p>
        <p class="indicator_value">""" + str(hrv_max) + """ bpm</p>
    </div>
    """
    
    return html

def health_indicators_heart_tachy_brady_qt():
    
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
                        <p class='indicator_name'>Tachycardia</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>HR</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(tachy_mean) + """ bpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Duration</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(tachy_duration) + """ min</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Proportion</p>
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
                        <p class='indicator_name'>Bradycardia</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>HR</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brady_mean) + """ bpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Duration</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brady_duration) + """ min</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Proportion</p>
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
                        <p class='indicator_name'>QT length</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Median</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(qt_mean) + """ ms</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Min</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(qt_min) + """ ms</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Max</p>
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
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.breath_icon + """'/> 
        <p>Breath Rate Per Minute (BRPM)</p>
    </div>
    """
    
    return html

def health_indicators_breath_brpm_results():
    
    brpm         = data.get_brpm()
    brpm_mean    = brpm["mean"]
    brpm_min     = brpm["min"]
    brpm_max     = brpm["max"]
    
    html = """
    <div class=col1_indicators>
        <p>Median</p>
        <p class="indicator_main_value">""" + str(brpm_mean) + """ brpm</p>
        <p>Min</p>
        <p class="indicator_value">""" + str(brpm_min) + """ brpm</p>
        <p>Max</p>
        <p class="indicator_value">""" + str(brpm_max) + """ brpm</p>
    </div>
    """
    
    return html

def health_indicators_breath_brv_title():
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.breath_icon + """'/> 
        <p>Breath Rate Variability (BRV)</p>
    </div>
    """
    
    return html

def health_indicators_breath_brv_results():
    
    brv         = data.get_brv()
    brv_mean    = brv["mean"]
    brv_min     = brv["min"]
    brv_max     = brv["max"]
    
    html = """
    <div class=col1_indicators>
        <p>Median</p>
        <p class="indicator_main_value">""" + str(brv_mean) + """ s</p>
        <p>Min</p>
        <p class="indicator_value">""" + str(brv_min) + """ s</p>
        <p>Max</p>
        <p class="indicator_value">""" + str(brv_max) + """ s</p>
    </div>
    """
    
    return html

def health_indicators_breath_tachy_brady_inexratio():
    
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
                        <p class='indicator_name'>Tachypnea</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>BR</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(tachy_mean) + """ brpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Duration</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(tachy_duration) + """ min</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Proportion</p>
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
                        <p class='indicator_name'>Bradypnea</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>BR</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brady_mean) + """ brpm</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Duration</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(brady_duration) + """ min</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Proportion</p>
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
                        <p class='indicator_name'>In/Out Length Ratio </p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Median</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(inexratio_mean) + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Min</p>
                    </div>
                    <div class='""" + col_val + """'>
                        <p class='""" + class_val + """'>""" + str(inexratio_min) + """</p>
                    </div>
                    <div class='""" + col_key + """'>
                        <p>Max</p>
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
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.stress_icon + """'/> 
        <p>Stress</p>
    </div>
    """
    
    return html

def health_indicators_stress_results():
    
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
                                Rest <br>
                                <span class='""" + class_val + """'>""" + str(stress_duration_rest) + """ min (""" + str(stress_percentage_rest) + """%)</span>
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_low + """'/>
                            <p>
                                Low <br>
                                <span class='""" + class_val + """'>""" + str(stress_duration_low) + """ min (""" + str(stress_percentage_low) + """%)</span>
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_medium + """'/>
                            <p>
                                Medium <br>
                                <span class='""" + class_val + """'>""" + str(stress_duration_medium) + """ min (""" + str(stress_percentage_medium) + """%)</span>
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.stress_high + """'/>
                            <p>
                                High <br>
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
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.pulseox_icon + """'/> 
        <p>Pulse Oxygen</p>
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
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.bodybattery_icon + """'/> 
        <p>Body Battery</p>
    </div>
    """
    
    return html

def health_indicators_bodybattery_results():
    
    bodybattery         = data.get_bodybattery()
    bodybattery_high    = bodybattery["high"]
    bodybattery_low     = bodybattery["low"]
    
    html = """
    <div class=col1_indicators>
        <p>High</p>
        <p class="indicator_main_value">""" + str(bodybattery_high) + """ </p>
        <p>Low</p>
        <p class="indicator_value">""" + str(bodybattery_low) + """</p>
    </div>
    """
    
    return html

def health_indicators_sleep_title():
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.sleep_icon + """'/> 
        <p>Sleep</p>
    </div>
    """
    
    return html

def health_indicators_sleep_results():
    
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
                                Deep <br>
                                <span class='""" + class_val + """'>""" + str(sleep_duration_deep) + """ min (""" + str(sleep_percentage_deep) + """%)</span> 
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_light + """'/>
                            <p>
                                Light <br>
                                <span class='""" + class_val + """'>""" + str(sleep_duration_light) + """ min (""" + str(sleep_percentage_light) + """%)</span>
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_rem + """'/>
                            <p>
                                REM <br>
                                <span class='""" + class_val + """'>""" + str(sleep_duration_rem) + """ min (""" + str(sleep_percentage_rem) + """%)</span>
                            </p>
                        </div>
                        <div class="col-12">
                            <img class=coloricon src='data:image/png;base64,""" + st.session_state.sleep_awake + """'/>
                            <p>
                                Awake <br>
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
    
    html = """
    <div class="second_title">
        <img class=icon src='data:image/png;base64,""" + st.session_state.temperature_icon + """'/> 
        <p>Skin Temperature (T°C)</p>
    </div>
    """
    
    return html

def health_indicators_temperature_results():
    
    temperature         = data.get_temperature()
    temperature_mean    = temperature["mean"]
    temperature_min     = temperature["min"]
    temperature_max     = temperature["max"]
    
    html = """
    <div class=col1_indicators>
        <p>Median</p>
        <p class="indicator_main_value">""" + str(temperature_mean) + """ °C</p>
        <p>Min</p>
        <p class="indicator_value">""" + str(temperature_min) + """ °C</p>
        <p>Max</p>
        <p class="indicator_value">""" + str(temperature_max) + """ °C</p>
    </div>
    """
    
    return html

def data_report_title():
    
    html = """
    <div id="data_report" class="main_title">
        <p>Data Report</p>
    </div>
    """
    
    return html


def data_report_download():
    
    html = """
    <div>
        <p>Download the daily data report (PDF):</p>
    </div>
    """
    
    return html

def definitions_title():
    
    html = """
    <div id="definitions" class="main_title">
        <p>Definitions</p>
    </div>
    """
    
    return html

def definitions_period_and_activity():
    
    html = """
    <div class="second_title">
        <p>Period & Activity</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-5">
                <div class="col-lg-12">
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.night + """'/> 
                    <p><b>Night</b>: From 0am to 6am</p>
                </div>
                <div class='col-lg-12'>
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.day + """'/> 
                    <p><b>Day</b>: From 6am to 0pm</p>
                </div>
            </div>
            <div class="col-lg-7">
                <div class="col-lg-12">
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.rest + """'/> 
                    <p><b>Rest</b>: Resting or low activity during the day</p>
                </div>
                <div class="col-lg-12">
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.activity + """'/> 
                    <p><b>Activity</b>: Moderate or high motion detection</p>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html
   
def definitions_alert():
    
    html = """
    <div class="second_title">
        <p>Alert Notification</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <div class="col-lg-12">
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.alert + """'/> 
                    <p>A red check box is used to notify at least one alerts</p>
                </div>
                <div class='col-lg-12'>
                    <img class=definitions_miniicon src='data:image/png;base64,""" + st.session_state.alert_no + """'/> 
                    <p>A green check box is used to specify that no alerts were identified</p>
                </div>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_heart():
    html = """
    <div class="second_title">
        <p>Cardiac Indicators</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>Heart Rate (HR)</b>
                    <br>
                    Number of Heart Beats Per Minute
                </p>
                <p>
                    <b>HR Resting</b>
                    <br>
                    ................
                </p>
                <p>
                    <b>HR High</b>
                    <br>
                    ................
                </p>
                <p>
                    <b>Heart Rate Variability (HRV)</b>
                    <br>
                    Standard deviation of RR intervals on 5min segments
                </p>
                <p>
                    <b>HRV Resting</b>
                    <br>
                    ................
                </p>
                <p>
                    <b>QT Length</b>
                    <br>
                    Time between Q and T waves in milliseconds, normalised by Framingham formula:
                    1000* (QT/1000 + 0.154*(1-RR))
                </p>
                <p>
                    <b>Tachycardia</b>
                    <br>
                    ................
                </p>
                <p>
                    <b>Bradycardia</b>
                    <br>
                    ................
                </p>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_breath():
    html = """
    <div class="second_title">
        <p>Respiratory Indicators</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>Breath Rate (BR)</b>
                    <br>
                    Number of Respiratory Cycles Per Minute
                </p>
                <p>
                    <b>BR Resting</b>
                    <br>
                    ................
                </p>
                <p>
                    <b>BR High</b>
                    <br>
                    ................
                </p>
                <p>
                    <b>Breath Rate Variability (BRV)</b>
                    <br>
                    Breath Rate Variability. Standard deviation of breath rate
                </p>
                <p>
                    <b>BRV Resting</b>
                    <br>
                    ................
                </p>
                <p>
                    <b>Tachypnea</b>
                    <br>
                    ................
                </p>
                <p>
                    <b>Bradypnea</b>
                    <br>
                    ................
                </p>
                <p>
                    <b>Breath In / Out Ratio</b>
                    <br>
                    ................
                </p>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_stress():
    html = """
    <div class="second_title">
        <p>Stress</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>bleble</b>
                    <br>
                    ...
                </p>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_pulseox():
    html = """
    <div class="second_title">
        <p>Pulse Ox</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>bleble</b>
                    <br>
                    ...
                </p>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_bodybattery():
    html = """
    <div class="second_title">
        <p>Body Battery</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>bleble</b>
                    <br>
                    ...
                </p>
            </div>
        </div>
    </div>
    """
    
    return html

def definitions_sleep():
    html = """
    <div class="second_title">
        <p>Sleep</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>bleble</b>
                    <br>
                    ...
                </p>
            </div>
        </div>
    </div>
    """
    
    return html
    
def definitions_temp():
    html = """
    <div class="second_title">
        <p>Skin Temperature</p>
    </div>
    <div class='definitions_section'>
        <div class="row">
            <div class="col-lg-12">
                <p>
                    <b>bleble</b>
                    <br>
                    ...
                </p>
            </div>
        </div>
    </div>
    """
    
    return html