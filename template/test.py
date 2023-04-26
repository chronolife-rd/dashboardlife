import numpy as np
import requests 

def authentication(api_key, url, userId):
    
    status_code = None
    message     = None
    
    reply = requests.get(url, headers={"X-API-Key": api_key})
    message, status_code = api_status(reply)

    return message, status_code

def api_status(reply, user_text='Username'):
    
    status_code = reply.status_code
    
    if status_code == 200:
        message = 'Connected'
    elif status_code == 400:
        message = 'Part of the request could not be parsed or is incorrect'
    elif status_code == 401:
        message = 'Incorrect API key'
    elif status_code == 403:
        message = 'Not authorized'
    elif status_code == 404:
        message = 'Incorrect url'
    elif status_code == 500:
        message = 'Incorrect ' + user_text
    elif status_code == 0:
        message = "You are disconnect"
        
    return message, status_code

def string(string, name, layout):
    
    error = False
    message = False
    if len(string) > 0:
        string = string.replace(" ", "")
    else:
        message = "Please fill in " + name + ' field'
        layout.error(message)
        error = True
        return string, message, error
        
    return string, message, error
    
def end_user(end_user, layout):
    
    error = False
    message = False
    if end_user == "":
        message = "End User ID is empty"
        error = True
        return message, error
    
    if len(end_user) != 6:
        message = "End User ID should contain 6 characters"
        error = True
        return message, error

    return message, error
    
def time(date, start_time, end_time, data_form):
    error = False
    message = False
    
    if start_time == "":
        message = "Start time format is empty. Please use hh:mm format"
        data_form.error(message)
        error = True
        return error
        
    if end_time == "":
        message = "End time format is empty. Please use hh : mm format"
        data_form.error(message)
        error = True
        return error
        
    if ":" not in start_time:
        message = "Start time format is incorrect. Missing ':'"
        data_form.error(message)
        error = True
        return error
        
    if ":" not in end_time:
        message = "End time format is incorrect. Missing ':'"
        data_form.error(message)
        error = True
        return error
    
    if len(start_time) != 5:
        message = "Start time format is incorrect. Length error"
        data_form.error(message)
        error = True
        return error
        
    if len(end_time) != 5:
        message = "End time format is incorrect. Length error"
        data_form.error(message)
        error = True
        return error
        
    try:
        tmp = int(start_time[:2])
        del tmp
        tmp = int(start_time[3:])
        del tmp
    except:
        message = "Start time format is incorrect. Hours or minutes seem incorrect"
        data_form.error(message)
        error = True
        return error
        
    try:
        tmp = int(end_time[:2])
        del tmp
        tmp = int(end_time[3:])
        del tmp
    except:
        message = "End time format is incorrect. Hours or minutes seem incorrect"
        data_form.error(message)
        error = True
        return error
        
        
    if int(start_time[:2]) < 0 or int(start_time[:2]) > 24:
        message = "Start time hours must be between 00 and 24"
        data_form.error(message)
        error = True
        return error
        
    if int(end_time[:2]) < 0 or int(end_time[:2]) > 24:
        message = "End time hours must be between 00 and 24"
        data_form.error(message)
        error = True
        return error
        
    if int(start_time[3:]) < 0 or int(start_time[3:]) > 59:
        message = "Start time minutes must be between 00 and 59"
        data_form.error(message)
        error = True
        return error
        
    if int(end_time[3:]) < 0 or int(end_time[3:]) > 59:
        message = "End time minutes must be between 00 and 59"
        data_form.error(message)
        error = True
        return error
        
    if int(end_time[:2]) < int(start_time[:2]):
        message = "End time must be greater than Start time"
        data_form.error(message)
        error = True
        return error
        
    if int(end_time[:2]) == int(start_time[:2]) and int(end_time[3:]) < int(start_time[3:]):
        message = "End time must be greater than Start time"
        data_form.error(message)
        error = True
        return error
        
    if end_time == start_time:
        message = "End time must be greater than Start time"
        data_form.error(message)
        error = True
        return error
        
    tmax = 30 # minutes
    start_datetime = np.datetime64(str(date) + 'T' + start_time)
    end_datetime = np.datetime64(str(date) + 'T' + end_time)
    
    delta = (end_datetime-start_datetime)/np.timedelta64(1, 'm')
    
    if delta > tmax:
        message = "Time interval may not exceed "+ str(tmax) + " minutes"
        data_form.error(message)
        error = True
        return error
        
    return message, error