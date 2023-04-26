import streamlit as st
import datetime
from template.constant import URL_ROOT
import template.html as html 
import template.chart as chart 
import template.session as session 
import template.test as test
import template.data as data

def run():
    """
    Main function of the layer display
    """
    # Head (html balise)
    head()
    
    # Header: image, logo
    header()
    
    # Display login form by default
    if not st.session_state.is_logged:
        login()
        
    # Display dashboard if session is logged in
    if st.session_state.is_logged:
        # Logout button
        logout_submit = logout()
        
        # Indicators form
        form_indicators()
        
        # My end users form
        form_myendusers()
        
        if st.session_state.is_data:
            with st.spinner("Wait for it..."):
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
        
        # show_historical_data(form_indicators_layout, form_indicators_submit)
        
        # Restart session logout button is clicked
        if logout_submit:
            session.restart()
            
        button_scroll_to_top()
        
    footer()

def head():
    st.markdown(html.head(), unsafe_allow_html=True)
    
def header():
    st.markdown(html.header(), unsafe_allow_html=True)
    
def footer():
    st.markdown(html.footer(), unsafe_allow_html=True)

def button_scroll_to_top():
    st.markdown(html.button_scroll_to_top(), unsafe_allow_html=True)
    
def login():
    
    _,col_login,_=st.columns(3)
    layout_login = col_login.empty()
    login_form  = layout_login.form('login')
    
    username    = login_form.text_input("Username", st.session_state['username'], placeholder="Ex: Chronnolife")
    api_key     = login_form.text_input("Password", st.session_state['api_key'], placeholder="Ex: f9VBqQoTiU0mnAKoXK1lky", type="password")

    if api_key:
        st.session_state.api_key = api_key

    button_login = login_form.form_submit_button("Login")

    if button_login:
        
        username, message, error    = test.string(username, name="Username", layout=login_form)
        api_key, message, error     = test.string(api_key, name="Password", layout=login_form)
        
        if not error:
            st.session_state.username = username
            st.session_state.api_key = api_key
        
        # % GET: Retrieve relevant properties of the specified user.
        url = URL_ROOT + "/user/{userId}".format(userId=username)
        message, status_code = test.authentication(api_key, url, username)
        
        if not error:
            if status_code == 200:
                st.session_state.is_logged = True
            else:
                st.session_state.is_logged = False
                
            if st.session_state.is_logged:
                layout_login.empty()
            else:
                login_form.error(message)
                
def logout():
    _,col_logout = st.columns([11,1])
    
    layout_logout = col_logout.empty()
    logout_submit = layout_logout.button('Logout')
    
    return logout_submit

def form_myendusers():
    # ----- Parameters selection -----
    _, col_form, _= st.columns(3)
    form_myendusers_layout = col_form.form("myendusers_form")
    form_myendusers_layout.markdown("<b>My end users ID</b>", unsafe_allow_html=True) 
    form_myendusers_onclick = form_myendusers_layout.form_submit_button("Show")
    
    if form_myendusers_onclick:
        data.get_myendusers()
        # st.write("Please find the list of the end-users'ID related to your Smart Textile account")
        c1,c2,c3 = form_myendusers_layout.columns(3)
        cnt=1
        for end_user_id in st.session_state.myendusers:
            if cnt==1:
                col=c1
            elif cnt==2:
                col=c2
            elif cnt==3:
                col=c3
                cnt=0
            col.markdown("""
                          <span class="modal_enduser">""" + end_user_id + """</span>
                          """, unsafe_allow_html=True)
            
            cnt+=1
                

def form_indicators():
    
    # ----- Parameters selection -----
    _, col_form, _= st.columns(3)
    form_indicators_layout = col_form.form("data_form")
    
    # Date picker
    date = form_indicators_layout.date_input("🗓️ Select date", max_value=datetime.datetime.now(), key="ksd")
    # User ID input
    end_user = form_indicators_layout.text_input("🏃🏼‍♂️ End-user ID","5P4svk")
    
    # Show button
    form_indicators_submit = form_indicators_layout.form_submit_button("Submit")
    
    if form_indicators_submit:
        
        message, error = test.end_user(end_user, form_indicators_layout)
        if error:
            form_indicators_layout.error(message)
            return

        st.session_state.date                   = date
        st.session_state.end_user               = end_user
        st.session_state.form_indicators_layout = form_indicators_layout
        st.session_state.form_indicators_submit = form_indicators_submit
        
        data.get_smart_textile_indicators()
        
        if len(st.session_state.smart_textile_indicators) > 0:
            st.session_state.is_data = True
            form_indicators_layout.info("Data has been successfully requested")
        else:
            st.session_state.is_data = False
            form_indicators_layout.warning("No data found")

def menu():
    st.markdown(html.menu(), unsafe_allow_html=True)

def overview():
    st.markdown(html.overview_title(), unsafe_allow_html=True)
    st.markdown(html.overview_data_collection(), unsafe_allow_html=True)
    st.markdown(html.overview_duration_title(), unsafe_allow_html=True)
    
    fig = chart.duration()
    config = {'displayModeBar': False}
    st.plotly_chart(fig, config=config, use_container_width=True)
    
    st.markdown(html.overview_health_indicators(), unsafe_allow_html=True)
    st.markdown("---")
    
def smart_textile_raw_data():
    
    st.markdown(html.smart_textile_raw_data_title(), unsafe_allow_html=True)
    download_text_layout = st.empty()
    download_button_layout = st.empty()
    form_smart_textile_raw_data()
    
    if st.session_state.form_raw_submit:
        with st.spinner("Getting Smart Textile Raw Data"):
            error = chart.smart_textile_raw_data()
            if error:
                st.session_state.form_raw_layout.warning("No data found")
            else:    
                download_text_layout.markdown(html.smart_textile_raw_data_download(), unsafe_allow_html=True)
                smart_textile_raw_data_download_button = download_button_layout.button('Download Smart Textile Raw Data', key="download_smart_textile_raw_data")
                # st.session_state.form_raw_layout.success("Smart Textile Data has been successfully requested")
                
    st.markdown("---")
                
def form_smart_textile_raw_data():
    
    date = st.session_state.date
    form_raw_layout = st.empty()
    form_raw_layout = st.form("raw_form")
    form_raw_layout.write("Select the time from which you wish to display the data (5 min display time):")
    col1, col2, col3, col4 = form_raw_layout.columns([1,1,1,6])
    # start_time = form_raw_layout.time_input('Start Time (UTC)', datetime.time(9, 20))
    
    form_hour = col1.selectbox(
    'Hour',
    ('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'))
    form_time = col2.selectbox(
    'Time',
    ('00', '05', '10', '15', '20', '25', 
     '30', '35', '40', '45', '50', '55'))
    form_period = col3.selectbox(
    'Period',
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
    
    form_raw_submit = form_raw_layout.form_submit_button("Submit")
    
    timezone = 'GMT'
    st.session_state.start_time      = start_time
    st.session_state.end_time        = end_time
    st.session_state.timezone        = timezone
    st.session_state.form_raw_layout = form_raw_layout
    st.session_state.form_raw_submit = form_raw_submit
    
def health_indicators():
    
    st.markdown(html.health_indicators_title(), unsafe_allow_html=True)
    st.markdown(html.health_indicators_download(), unsafe_allow_html=True)
    health_indicator_download_button = st.button('Download Health Indicators', key="download_health_indicators")
    tab_heart, tab_breath, tab_stress, tab_pulseox, tab_bodybattery, tab_sleep, tab_temp = st.tabs(["Heart", 
                                                                                                  "Breath", 
                                                                                                  "Stress",
                                                                                                  "Pulse Ox",
                                                                                                  "Body Battery",
                                                                                                  "Sleep",
                                                                                                  "Temperature",
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
        
    # download_col,_ = st.columns([2,6])
    # download_layout = st.empty()
    # data.download(download_layout)
    
    st.markdown("---")

def health_indicators_heart_bpm():
    st.markdown(html.health_indicators_heart_bpm_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,4])
    col1.markdown(html.health_indicators_heart_bpm_results(), unsafe_allow_html=True)
    
    fig = chart.heart_bpm()
    config = {'displayModeBar': False}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def health_indicators_heart_hrv():
    st.markdown(html.health_indicators_heart_hrv_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,4])
    col1.markdown(html.health_indicators_heart_hrv_results(), unsafe_allow_html=True)
    
    fig = chart.heart_hrv()
    config = {'displayModeBar': False}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_heart_tachy_brady_qt():
    
    st.markdown(html.health_indicators_heart_tachy_brady_qt(), unsafe_allow_html=True)
    
def health_indicators_breath_brpm():
    st.markdown(html.health_indicators_breath_brpm_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,4])
    col1.markdown(html.health_indicators_breath_brpm_results(), unsafe_allow_html=True)
    
    fig = chart.breath_brpm()
    config = {'displayModeBar': False}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def health_indicators_breath_brv():
    st.markdown(html.health_indicators_breath_brv_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,4])
    col1.markdown(html.health_indicators_breath_brv_results(), unsafe_allow_html=True)
    
    fig = chart.breath_brv()
    config = {'displayModeBar': False}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_breath_tachy_brady_inexratio():
    
    st.markdown(html.health_indicators_breath_tachy_brady_inexratio(), unsafe_allow_html=True)
    
def health_indicators_temperature():
    st.markdown(html.health_indicators_temperature_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,4])
    col1.markdown(html.health_indicators_temperature_results(), unsafe_allow_html=True)
    
    fig = chart.temperature_mean()
    config = {'displayModeBar': False}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_stress():
    st.markdown(html.health_indicators_stress_title(), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown(html.health_indicators_stress_results(), unsafe_allow_html=True)
    
    fig = chart.stress()
    config = {'displayModeBar': False}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_pulseox():
    st.markdown(html.health_indicators_pulseox_title(), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown(html.health_indicators_pulseox_results(), unsafe_allow_html=True)
    
    fig = chart.pulseox()
    config = {'displayModeBar': False}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def health_indicators_bodybattery():
    st.markdown(html.health_indicators_bodybattery_title(), unsafe_allow_html=True)
    col1, col2 = st.columns([1,4])
    col1.markdown(html.health_indicators_bodybattery_results(), unsafe_allow_html=True)
    
    fig = chart.bodybattery()
    config = {'displayModeBar': False}
    col2.plotly_chart(fig, config=config, use_container_width=True)
    
def health_indicators_sleep():
    st.markdown(html.health_indicators_sleep_title(), unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    col1.markdown(html.health_indicators_sleep_results(), unsafe_allow_html=True)
    
    fig = chart.sleep()
    config = {'displayModeBar': False}
    col2.plotly_chart(fig, config=config, use_container_width=True)

def data_report():
    st.markdown(html.data_report_title(), unsafe_allow_html=True)
    st.markdown(html.data_report_download(), unsafe_allow_html=True)
    data_report_download_button = st.button('Download Data Report', key="download_data_report")
    
    st.markdown("---")
    
def definitions():
    st.markdown(html.definitions_title(), unsafe_allow_html=True)
    
    tab_alert, tab_period_and_activity, tab_heart, tab_breath, tab_stress,\
        tab_pulseox, tab_bodybattery, tab_sleep, tab_temp = st.tabs(["Alert", 
                                                                     "Period and Activity", 
                                                                     "Heart",
                                                                     "Breath", 
                                                                     "Stress",
                                                                     "Pulse Ox",
                                                                     "Body Battery",
                                                                     "Sleep",
                                                                     "Temperature",
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
