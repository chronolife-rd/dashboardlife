# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:39:32 2023

@author: aterman
"""
from datetime import datetime, timedelta
import pandas as pd 

ts = 1662707400.0
time = datetime.fromtimestamp(ts)
print(time, type(time))

def get_timestamp(id_:str):
    timestamp = id_[:id_.index(".")]
    timestamp_int = int(timestamp)

    output = datetime.fromtimestamp(timestamp_int) 
    return  output
# %%
times = "1662707402.0"
times = get_timestamp(ts)

times_list = []
times_list.append(times)
print('Type of value of the list', type(times_list[0]), times_list[0])

df = pd.DataFrame({'times':times_list})
print('Type of value of the df', type(df['times'][0]), df['times'][0])

# df["times_2"] = df["times"].apply(lambda x: x.to_pydatetime())
# print('Type of value of the df changed', type(df['times_2'][0]), df['times_2'][0])

df["times_2"] = df["times"].apply(lambda x: x.strftime('%Y-%m-%d %H:%M'))
print('Type of value of the df changed', type(df['times_2'][0]), df['times_2'][0])


# %% 

# df.times = df.times.apply(lambda x: x.to_pydatetime()) # round("min")  date()

t = df["times_2"][0]

df["minute_datetime"] = df["minute_datetime"].to_pydatetime()


stamp = pd.Timestamp('2021-01-01 00:00:00')

#convert timestamp to datetime
stamp = stamp.to_pydatetime()

r = datetime(2021, 1, 1, 0, 0)

#%%

def change_date(date:str, sign = -1) -> str:
    date_today = datetime.strptime(date, "%Y-%m-%d")
    new_date = date_today + sign*timedelta(days=1)
    new_date =  datetime.strftime(new_date, "%Y-%m-%d")
    return new_date

date = '2023-05-01'
date_after = change_date(date, sign = +1)
date_before = change_date(date, sign = -1)
print('Date +1:', date_after)
print('Date:   ', date)
print('Date -1:', date_before)