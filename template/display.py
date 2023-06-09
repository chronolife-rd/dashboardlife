import streamlit as st
import datetime
import template.html as html 
import template.chart as chart 
import template.session as session 
import template.test as test
import data.data as data
import template.download as download
# import template.data.chronolife_data as chronolife_data
# import template.data.garmin_data as garmin_data

def run():
    """ Main function of the layer display """
    
    # Call translate global variable
    translate = st.session_state.translate
    
    # Language
    set_language()
    
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
        form_sessions()
        
        # Indicators form
        form_data()
        
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
    """ Call CSS head """
    st.markdown(html.head(), unsafe_allow_html=True)
    
def header():
    """ Display header """
    st.markdown(html.header(), unsafe_allow_html=True)
    
def footer():
    """ Display footer """
    st.markdown(html.footer(), unsafe_allow_html=True)

def set_language():
    """ Manage language """
    
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
    """ Display profile in sidebar """
    
    st.sidebar.markdown(html.profile(), unsafe_allow_html=True)
    # Add an horizontal line
    st.sidebar.markdown("---")
    
def login():
    """ Display profile in sidebar """
    
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
        
        # !!! TO BE UPDATED !!!
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
            
            # Hide login form after connection or display error message
            if st.session_state.is_logged:
                layout_login.empty()
            else:
                login_form.error(message)
                
def logout():
    """ Display logout button """
    translate = st.session_state.translate
    
    # Display logout button
    layout_logout = st.sidebar.empty()
    logout_submit = layout_logout.button(translate["logout"])
    st.session_state.logout_submit = logout_submit

def myendusers():
    """ Display endusers """
    
    translate = st.session_state.translate
    
    # Create expander
    _, col_form, _= st.columns([1,4,1])
    expander_endusers = col_form.expander(translate["my_endusers_title"], expanded=False)
    
    # Display endusers on 3 columns
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
            col.markdown("""<span class="enduser">""" + end_user_id + """</span>""", unsafe_allow_html=True)
            cnt+=1
    else:
        expander_endusers.info(translate["no_enduser"])
                
def form_sessions():
    """ Display and process sessions """
    
    translate = st.session_state.translate
    
    # Create expander
    _, col_form, _  = st.columns([1,4,1])
    title           = translate["form_sessions_title"]  
    sessions_exp    = col_form.expander(title, expanded=False)
    form_sessions   = sessions_exp.form("form_sessions")
    
    # ----- Create Session form ----- 
    c1, c2, c3 = form_sessions.columns(3)
    
    # Current Date 
    today   = datetime.datetime.now()
    # Minimum year in selectbox
    year0   = 2020
    # Years in selectbox
    years   = range(year0, today.year+1)
    year    = c1.selectbox(translate["year"], years, index=years.index(today.year))
    # Selectbox for months
    month                   = c2.selectbox(translate["month"], translate["months"], index=today.month-1)
    # End user input
    end_user                = c3.text_input(translate["enduser_id"])
    # Submit button
    form_sessions_submit    = form_sessions.form_submit_button(translate["search"])
    
    if form_sessions_submit:
        with st.spinner((translate["spinner_getting_sessions"])):
            # Test end user input
            message, error = test.end_user(end_user, form_sessions)
            if error:
                form_sessions.error(message)
                return
            
            # Get selected month index for datetime conversion
            month_index         = translate["months"].index(month)+1
            # Get sessions
            enduser_sessions    = data.get_sessions(year=year, month=month_index, end_user=end_user)
            # Reset table indexes beginning to 1 instead of 0
            enduser_sessions    = enduser_sessions.set_axis(range(1, 1+len(enduser_sessions)), axis='index') # begin index at 1
            # Save enduser sessions
            st.session_state.enduser_sessions = enduser_sessions 
            
        # Display enduser sessions or error message
        if enduser_sessions is not None:
            if len(enduser_sessions) > 0:
                sessions_exp.write(enduser_sessions)
            else:
                sessions_exp.info(translate["message_no_session"])

def form_data():
    """ Display and process data """
    
    translate = st.session_state.translate
    
    # Create expander
    _, col_form, _= st.columns([1,4,1])
    title = translate["form_indicator_title"] 
    sessions_exp = col_form.expander(title, expanded=False)
    
    # Create data form
    form_data_layout = sessions_exp.form("data_form")
    c1, c2 = form_data_layout.columns(2)
    # Date picker
    date = c1.date_input(translate["date"], max_value=datetime.datetime.now(), key="ksd")
    # User ID input
    end_user = c2.text_input(translate["enduser_id"],"6o2Fzp")     
    # Submit button
    form_data_submit = form_data_layout.form_submit_button(translate["submit"])
    
    if form_data_submit:
        # Test end user
        message, error = test.end_user(end_user, form_data_layout)
        
        # Display error
        if error:
            form_data_layout.error(message)
            return
        
        # Save variables
        st.session_state.date                   = date.strftime("%Y-%m-%d")
        st.session_state.end_user               = end_user
        st.session_state.form_data_layout       = form_data_layout
        st.session_state.form_data_submit       = form_data_submit
        
        
        # !!! TO BE UPDATED !!!
        # ---- Manage is_data flag -----
        # chronolife_data.get_chronolife_indicators()
        # garmin_data.get_garmin_indicators()
        data.get_health_indicators()
        
        # if len(st.session_state.chronolife_indicators) > 0 or len(st.session_state.garmin_indicators) > 0:
        if len(st.session_state.chronolife_indicators) > 0:
            st.session_state.is_data = True
        else:
            st.session_state.is_data = False
            form_data_layout.warning(translate["message_no_data"])

def menu():
    """ Display vertical menu """
    
    st.sidebar.markdown(html.menu_overview(), unsafe_allow_html=True)
    st.sidebar.markdown(html.menu_smart_textile_raw_data(), unsafe_allow_html=True)
    st.sidebar.markdown(html.menu_health_indicators(), unsafe_allow_html=True)
    st.sidebar.markdown(html.menu_data_report(), unsafe_allow_html=True)
    st.sidebar.markdown(html.menu_definitions(), unsafe_allow_html=True)

def overview():
    """ Display overview section """
    
    # Display title
    st.markdown(html.overview_title(), unsafe_allow_html=True)
    
    # Display data collection sub section
    st.markdown(html.overview_data_collection(), unsafe_allow_html=True)
    
    # Display duration chart
    fig = chart.duration()
    config = {'displayModeBar': True}
    st.plotly_chart(fig, config=config, use_container_width=True)
    
    # Display health indicators overview sub section
    st.markdown(html.overview_health_indicators(), unsafe_allow_html=True)
    
    st.markdown("---")
    
def smart_textile_raw_data():
    """ Display smart textile raw data section """
    
    translate = st.session_state.translate
    
    # Display title
    st.markdown(html.smart_textile_raw_data_title(), unsafe_allow_html=True)
    
    # Display form
    form_smart_textile_raw_data()
    
    # Display raw data
    if st.session_state.form_raw_submit:
        with st.spinner(translate["spinner_smart_textile_raw_data"]):
            # Display raw data charts
            error = chart.smart_textile_raw_data()
            
            # Display download button or warning message
            if error:
                st.session_state.form_raw_layout.warning(translate["message_no_data"])
            
            else:    
                
                st.markdown(html.smart_textile_raw_data_download(), unsafe_allow_html=True)
                
                # Convert raw data to excel 
                data = download.raw_data_to_excel()
                
                # Download Health indicators data
                st.download_button(label=translate["download"],
                                   data=data,
                                   file_name=('Smart_Textile_Raw_Data.xlsx'),
                                   ) 
    st.markdown("---")
                
def form_smart_textile_raw_data():
    """ Display raw data form """
    
    translate = st.session_state.translate
    
    date = st.session_state.date
    date = datetime.datetime.strptime(date, "%Y-%m-%d")
    form_raw_layout = st.empty()
    form_raw_layout = st.form("raw_form")
    form_raw_layout.write(translate["smart_textile_raw_data_select_time"])
    col1, col2, col3, col4 = form_raw_layout.columns([3,3,6,3])
    
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
    """ Display health indicators section """
    
    translate = st.session_state.translate
    
    st.markdown(html.health_indicators_title(), unsafe_allow_html=True)
    st.markdown(html.health_indicators_download(), unsafe_allow_html=True)
    
    # Convert health indicators dataframe to excel 
    data = download.health_indicators_to_excel()
    
    # Download Health indicators data
    st.download_button(
        label=translate["download"],
        data=data,
        file_name=('Health_indicators.xlsx'),
    ) 
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
        # Breath inspiration/ expiration ratio
        health_indicators_breath_inex()
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
    """ Display bpm in health indicators section """
    st.markdown(html.health_indicators_heart_bpm_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_heart_bpm_results(), unsafe_allow_html=True)
    
    fig = chart.heart_bpm()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def health_indicators_heart_hrv():
    """ Display hrv in health indicators section """
    st.markdown(html.health_indicators_heart_hrv_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_heart_hrv_results(), unsafe_allow_html=True)
    
    fig = chart.heart_hrv()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_heart_tachy_brady_qt():
    """ Display alerts and data for tachy/brady and QT in health indicators section """
    st.markdown(html.health_indicators_heart_tachy_brady_qt(), unsafe_allow_html=True)
    
def health_indicators_breath_brpm():
    """ Display brpm in health indicators section """
    st.markdown(html.health_indicators_breath_brpm_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_breath_brpm_results(), unsafe_allow_html=True)
    
    fig = chart.breath_brpm()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def health_indicators_breath_brv():
    """ Display brv in health indicators section """
    st.markdown(html.health_indicators_breath_brv_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_breath_brv_results(), unsafe_allow_html=True)
    
    fig = chart.breath_brv()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def health_indicators_breath_inex():
    """ Display in/ex ratio in health indicators section """
    st.markdown(html.health_indicators_breath_inex_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_breath_inex_results(), unsafe_allow_html=True)
    
    fig = chart.breath_inex()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)


def health_indicators_breath_tachy_brady_inexratio():
    """ Display alerts and data for tachy/brady and ratio breath in/out in health indicators section """
    st.markdown(html.health_indicators_breath_tachy_brady_inexratio(), unsafe_allow_html=True)
    
def health_indicators_temperature():
    """ Display temperature in health indicators section """
    st.markdown(html.health_indicators_temperature_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_temperature_results(), unsafe_allow_html=True)
    
    fig = chart.temperature_mean()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_stress():
    """ Display stress in health indicators section """
    st.markdown(html.health_indicators_stress_title(), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown(html.health_indicators_stress_results(), unsafe_allow_html=True)
    
    fig = chart.stress()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_pulseox():
    """ Display pulseox in health indicators section """
    st.markdown(html.health_indicators_pulseox_title(), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown(html.health_indicators_pulseox_results(), unsafe_allow_html=True)
    
    fig = chart.pulseox()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def health_indicators_bodybattery():
    """ Display body battery in health indicators section """
    st.markdown(html.health_indicators_bodybattery_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,2])
    col1.markdown(html.health_indicators_bodybattery_results(), unsafe_allow_html=True)
    
    fig = chart.bodybattery()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_sleep():
    """ Display sleep in health indicators section """
    st.markdown(html.health_indicators_sleep_title(), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown(html.health_indicators_sleep_results(), unsafe_allow_html=True)
    
    fig = chart.sleep()
    config = {'displayModeBar': True}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def data_report():
    """ Display data report section """
    translate = st.session_state.translate

    st.markdown(html.data_report_title(), unsafe_allow_html=True)
    st.markdown(html.data_report_download(), unsafe_allow_html=True)
    
    # Convert raw data to excel 
    data = download.data_report_pdf()
    # Download Health indicators data
    st.download_button(
        label=translate["download"],
        data=data,
        file_name=('Data_Report.pdf'),
    ) 
    
    st.markdown("---")
    
def definitions():
    """ Display definitions section """
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

