import streamlit as st
import datetime
import template.html as html 
import template.chart as chart 
import template.session as session 
import template.test as test
import template.data as data
import template.chronolife_data as chronolife_data
import template.garmin_data as garmin_data

def run():
    """
    Main function of the layer display
    """
    
    # Call translate global variable
    translate = st.session_state.translate
    
    # Language
    form_language()
    
    # Head (html balise)
    head()
    
    # Header: image, logo
    header()
    
    # Display login form by default
    if not st.session_state.is_logged:
        login()
    
    # Display dashboard if session is logged in
    if st.session_state.is_logged:
        
        profile()
        
        # My end users form
        myendusers()
        
        # Enduser sessions form
        form_enduser_sessions()
        
        # Indicators form
        form_indicators()
        
        if st.session_state.is_data:
            with st.spinner(translate["spinner_loading"]):
                
                # Main menu
                menu()
                
                # Overview section
                overview()
                
                # Smart Textile Raw Data section
                smart_textile_raw_data()
                
                # Health Indicators section
                health_indicators()
                
                # Definitions section
                data_report()
                
                # Definitions section
                definitions()
            
        # Logout button
        logout()
        
        # Restart session logout button is clicked
        if st.session_state.logout_submit:
            session.restart()
            
        # # Button scroll to top
        # button_scroll_to_top()
        
    footer()

def head():
    st.markdown(html.head(), unsafe_allow_html=True)
    
def header():
    st.markdown(html.header(), unsafe_allow_html=True)
    
def footer():
    st.markdown(html.footer(), unsafe_allow_html=True)

def form_language():
    
    # Create layout for the label of the selectbox
    language_label_layout = st.sidebar.empty()
    
    # Create selectbox language
    language = st.sidebar.selectbox("", ("FR", "EN"))
    
    # Don't update language if the same language is selected
    if language != st.session_state.language:
        # update language
        st.session_state.language = language
        # translate
        session.set_translation()
    
    # update the label of the selectbox
    language = st.session_state.language
    language_label_layout.markdown(html.language_label(), unsafe_allow_html=True)
    
    # Add an horizontal line
    st.sidebar.markdown("---")
        
        
def profile():
    
    st.sidebar.markdown(html.profile(), unsafe_allow_html=True)
    # Add an horizontal line
    st.sidebar.markdown("---")
    
# def button_scroll_to_top():
#     st.markdown(html.button_scroll_to_top(), unsafe_allow_html=True)
    
def login():
    
    translate = st.session_state.translate
    
    # Create form
    _,col_login,_=st.columns([2,3,2])
    layout_login = col_login.empty()
    login_form  = layout_login.form('login')
    
    env             = login_form.selectbox("Env", ("preprod", "prod"))
    username        = login_form.text_input(translate["username"], "Michel", placeholder="Ex: Chronnolife")
    api_key         = login_form.text_input(translate["password"], "a8LeZpzQ9ck61ITF_8lBkw", placeholder="Ex: f9VBqQoTiU0mnAKoXK1lky", type="password")
    button_login    = login_form.form_submit_button(translate["login"])
    
    if button_login:
        
        # !!! Debug code !!! 
        if env == "preprod":
            st.session_state.prod = False
    
        # Set urls for API requests
        session.set_url()
        
        # Test inputs
        username, message, error    = test.string(username, name="Username", layout=login_form)
        api_key, message, error     = test.string(api_key, name="Password", layout=login_form)
        
        if not error:
            st.session_state.username = username
            st.session_state.api_key = api_key
        
        # User Authentication
        message, status_code_apikey = test.authentication2()
        
        if not error:
            if status_code_apikey == 200:
                # Get the list of end users 
                message, status_code_username = data.get_myendusers()
                
                if status_code_username == 200:
                    st.session_state.is_logged = True
            
            if st.session_state.is_logged:
                layout_login.empty()
            else:
                login_form.error(message)
                
def logout():
    
    translate = st.session_state.translate
    
    layout_logout = st.sidebar.empty()
    logout_submit = layout_logout.button(translate["logout"])
    
    st.session_state.logout_submit = logout_submit

def myendusers():
    
    translate = st.session_state.translate
    
    # ----- Parameters selection -----
    _, col_form, _= st.columns([1,4,1])
    expander_endusers = col_form.expander(translate["my_endusers_title"], expanded=False)
    c1,c2,c3 = expander_endusers.columns(3)
    cnt=1
    if len(st.session_state.myendusers) > 0:
        for end_user_id in st.session_state.myendusers:
            if cnt==1:
                col=c1
            elif cnt==2:
                col=c2
            elif cnt==3:
                col=c3
                cnt=0
            col.markdown("""
                          <span class="enduser">""" + end_user_id + """</span>
                          """, unsafe_allow_html=True)
            
            cnt+=1
    else:
        expander_endusers.info("No end user found")
                
def form_enduser_sessions():
    
    translate = st.session_state.translate
    
    _, col_form, _= st.columns([1,4,1])
    title = translate["form_sessions_title"]  
    sessions_exp = col_form.expander(title, expanded=False)
    form_sessions = sessions_exp.form("form_sessions")
    c1, c2, c3 = form_sessions.columns(3)
    
    today = datetime.datetime.now()
    year0 = 2020
    years = range(year0, today.year+1)
    year = c1.selectbox(translate["year"], years, index=years.index(today.year))
    
    months                  = translate["months"] 
    month                   = c2.selectbox(translate["month"], months, index=today.month-1)
    end_user                = c3.text_input(translate["enduser_id"])
    form_sessions_submit    = form_sessions.form_submit_button(translate["search"])
    
    if form_sessions_submit:
        with st.spinner((translate["spinner_getting_sessions"])):
            message, error = test.end_user(end_user, form_sessions)
            if error:
                form_sessions.error(message)
                return
            month_index = translate["months"].index(month)+1
            enduser_sessions = data.get_sessions(year=year, month=month_index, end_user=end_user)
            enduser_sessions = enduser_sessions.set_axis(range(1, 1+len(enduser_sessions)), axis='index') # begin index at 1
            st.session_state.enduser_sessions = enduser_sessions 
    
        if enduser_sessions is not None:
            if len(enduser_sessions) > 0:
                sessions_exp.write(enduser_sessions)
            else:
                sessions_exp.info(translate["message_no_session"])


def form_indicators():
    
    translate = st.session_state.translate
    
    # ----- Parameters selection -----
    _, col_form, _= st.columns([1,4,1])
    title = translate["form_indicator_title"] 
    sessions_exp = col_form.expander(title, expanded=False)
    form_indicators_layout = sessions_exp.form("data_form")
    
    c1, c2 = form_indicators_layout.columns(2)
    
    # Date picker
    date = c1.date_input(translate["date"], max_value=datetime.datetime.now(), key="ksd")
    # User ID input
    end_user = c2.text_input(translate["enduser_id"],"6o2Fzp") #5P4svk, 6o2Fzp
    
    # Show button
    form_indicators_submit = form_indicators_layout.form_submit_button(translate["submit"])
    
    if form_indicators_submit:
        
        message, error = test.end_user(end_user, form_indicators_layout)
        if error:
            form_indicators_layout.error(message)
            return

        st.session_state.date                   = date.strftime("%Y-%m-%d")
        st.session_state.end_user               = end_user
        st.session_state.form_indicators_layout = form_indicators_layout
        st.session_state.form_indicators_submit = form_indicators_submit
        
        chronolife_data.get_smart_textile_indicators()
        garmin_data.get_garmin_data()
        
        # if len(st.session_state.smart_textile_indicators) > 0 or len(st.session_state.garmin_data) > 0:
        if len(st.session_state.smart_textile_indicators) > 0:
            st.session_state.is_data = True
        else:
            st.session_state.is_data = False
            form_indicators_layout.warning(translate["message_no_data"])

def menu():
    st.sidebar.markdown(html.menu_overview(), unsafe_allow_html=True)
    st.sidebar.markdown(html.menu_smart_textile_raw_data(), unsafe_allow_html=True)
    st.sidebar.markdown(html.menu_health_indicators(), unsafe_allow_html=True)
    st.sidebar.markdown(html.menu_data_report(), unsafe_allow_html=True)
    st.sidebar.markdown(html.menu_definitions(), unsafe_allow_html=True)

def overview():
    st.markdown(html.overview_title(), unsafe_allow_html=True)
    st.markdown(html.overview_data_collection(), unsafe_allow_html=True)
    
    fig = chart.duration()
    config = {'displayModeBar': True}
    st.plotly_chart(fig, config=config, use_container_width=True)
    
    st.markdown(html.overview_health_indicators(), unsafe_allow_html=True)
    st.markdown("---")
    
def smart_textile_raw_data():
    
    translate = st.session_state.translate
    
    st.markdown(html.smart_textile_raw_data_title(), unsafe_allow_html=True)
    form_smart_textile_raw_data()
    
    if st.session_state.form_raw_submit:
        with st.spinner(translate["spinner_smart_textile_raw_data"]):
            error = chart.smart_textile_raw_data()
            if error:
                st.session_state.form_raw_layout.warning(translate["message_no_data"])
            else:    
                download_text_layout = st.empty()
                download_button_layout = st.empty()
                download_text_layout.markdown(html.smart_textile_raw_data_download(), unsafe_allow_html=True)
                smart_textile_raw_data_download_button = download_button_layout.button(translate["download"], key="download_smart_textile_raw_data")
                
    st.markdown("---")
                
def form_smart_textile_raw_data():
    
    translate = st.session_state.translate
    
    date = st.session_state.date
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    form_raw_layout = st.empty()
    form_raw_layout = st.form("raw_form")
    form_raw_layout.write(translate["smart_textile_raw_data_select_time"])
    col1, col2, col3, col4 = form_raw_layout.columns([3,3,3,6])
    
    form_hour = col1.selectbox(
    translate["hour"],
    ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'))
    form_time = col2.selectbox(
    translate["minute"],
    ('00', '05', '10', '15', '20', '25', 
     '30', '35', '40', '45', '50', '55'))
    form_period = col3.selectbox(
    translate["period"],
    ('AM', 'PM'))
    
    if form_period == "PM":
        form_hour = int(form_hour)
        form_hour += 12
        form_hour = str(form_hour)
        if form_hour == "24":
            form_hour = "00"
            
    start_datetime = datetime.datetime(date.year, date.month, date.day, int(form_hour), int(form_time))
    end_datetime = start_datetime + datetime.timedelta(minutes=5)
    start_time = start_datetime.time().strftime("%H:%M")
    end_time = end_datetime.time().strftime("%H:%M")
    
    form_raw_submit = form_raw_layout.form_submit_button(translate["submit"])
    
    timezone = 'GMT'
    st.session_state.start_time      = start_time
    st.session_state.end_time        = end_time
    st.session_state.timezone        = timezone
    st.session_state.form_raw_layout = form_raw_layout
    st.session_state.form_raw_submit = form_raw_submit
    
def health_indicators():
    
    translate = st.session_state.translate
    
    st.markdown(html.health_indicators_title(), unsafe_allow_html=True)
    st.markdown(html.health_indicators_download(), unsafe_allow_html=True)
    health_indicator_download_button = st.button(translate["download"], key="download_health_indicators")
    tab_heart, tab_breath, tab_stress, tab_pulseox, tab_bodybattery, tab_sleep, tab_temp = st.tabs([translate["cardiology"], 
                                                                                                  translate["respiratory"], 
                                                                                                  translate["stress"],
                                                                                                  translate["pulseox"],
                                                                                                  translate["bodybattery"],
                                                                                                  translate["sleep"],
                                                                                                  translate["temperature"],
                                                                                                  ])
    
    with tab_heart:
        # Heart Beat Per Minute
        health_indicators_heart_bpm()
        # Heart Rate Variability
        health_indicators_heart_hrv()
        # Tachycardia, Bradycardia, QT length
        health_indicators_heart_tachy_brady_qt()
        
    with tab_breath:
        # Breath Rate Per Minute
        health_indicators_breath_brpm()
        # Breath Rate Variability
        health_indicators_breath_brv()
        # Tachypnea, Bradypnea, inspiration/expiration ration
        health_indicators_breath_tachy_brady_inexratio()
        
    
    with tab_stress:
        health_indicators_stress()
        
    with tab_pulseox:
        health_indicators_pulseox()
        
    with tab_bodybattery:
        health_indicators_bodybattery()
        
    with tab_sleep:
        health_indicators_sleep()
        
    with tab_temp:
        health_indicators_temperature()
        
    st.markdown("---")

def health_indicators_heart_bpm():
    st.markdown(html.health_indicators_heart_bpm_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_heart_bpm_results(), unsafe_allow_html=True)
    
    fig = chart.heart_bpm()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def health_indicators_heart_hrv():
    st.markdown(html.health_indicators_heart_hrv_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_heart_hrv_results(), unsafe_allow_html=True)
    
    fig = chart.heart_hrv()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_heart_tachy_brady_qt():
    st.markdown(html.health_indicators_heart_tachy_brady_qt(), unsafe_allow_html=True)
    
def health_indicators_breath_brpm():
    st.markdown(html.health_indicators_breath_brpm_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_breath_brpm_results(), unsafe_allow_html=True)
    
    fig = chart.breath_brpm()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def health_indicators_breath_brv():
    st.markdown(html.health_indicators_breath_brv_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_breath_brv_results(), unsafe_allow_html=True)
    
    fig = chart.breath_brv()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_breath_tachy_brady_inexratio():
    
    st.markdown(html.health_indicators_breath_tachy_brady_inexratio(), unsafe_allow_html=True)
    
def health_indicators_temperature():
    st.markdown(html.health_indicators_temperature_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_temperature_results(), unsafe_allow_html=True)
    
    fig = chart.temperature_mean()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_stress():
    st.markdown(html.health_indicators_stress_title(), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown(html.health_indicators_stress_results(), unsafe_allow_html=True)
    
    fig = chart.stress()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_pulseox():
    st.markdown(html.health_indicators_pulseox_title(), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown(html.health_indicators_pulseox_results(), unsafe_allow_html=True)
    
    fig = chart.pulseox()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def health_indicators_bodybattery():
    st.markdown(html.health_indicators_bodybattery_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_bodybattery_results(), unsafe_allow_html=True)
    
    fig = chart.bodybattery()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_sleep():
    st.markdown(html.health_indicators_sleep_title(), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown(html.health_indicators_sleep_results(), unsafe_allow_html=True)
    
    fig = chart.sleep()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def data_report():
    
    translate = st.session_state.translate

    st.markdown(html.data_report_title(), unsafe_allow_html=True)
    st.markdown(html.data_report_download(), unsafe_allow_html=True)
    data_report_download_button = st.button(translate['download'], key="download_data_report")
    
    st.markdown("---")
    
def definitions():
    
    translate = st.session_state.translate
    
    st.markdown(html.definitions_title(), unsafe_allow_html=True)
    
    tab_alert, tab_period_and_activity, tab_heart, tab_breath, tab_stress,\
        tab_pulseox, tab_bodybattery, tab_sleep, tab_temp = st.tabs([translate["alert"], 
                                                                     translate["period_and_activity"], 
                                                                     translate["cardiology"],
                                                                     translate["respiratory"], 
                                                                     translate["stress"],
                                                                     translate["pulseox"],
                                                                     translate["bodybattery"],
                                                                     translate["sleep"],
                                                                     translate["temperature"],
                                                                     ])
    with tab_alert:
        st.markdown(html.definitions_alert(), unsafe_allow_html=True)
    with tab_period_and_activity:
        st.markdown(html.definitions_period_and_activity(), unsafe_allow_html=True)
    with tab_heart:
        st.markdown(html.definitions_heart(), unsafe_allow_html=True)
    with tab_breath:
        st.markdown(html.definitions_breath(), unsafe_allow_html=True)
    with tab_stress:
        st.markdown(html.definitions_stress(), unsafe_allow_html=True)
    with tab_pulseox:
        st.markdown(html.definitions_pulseox(), unsafe_allow_html=True)
    with tab_bodybattery:
        st.markdown(html.definitions_bodybattery(), unsafe_allow_html=True)
    with tab_sleep:
        st.markdown(html.definitions_sleep(), unsafe_allow_html=True)
    with tab_temp:
        st.markdown(html.definitions_temp(), unsafe_allow_html=True)

