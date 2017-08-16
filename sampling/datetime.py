#!/usr/bin/env python
import numpy as np
import pandas as pd

def get_year( df_datatime ):
    return df_datatime.dt.year.astype(int)

def get_month( df_datatime ):
    return df_datatime.dt.month.astype(int)

def get_day( df_datatime ):
    return df_datatime.dt.day.astype(int)

def get_hour( df_datatime ):
    return df_datatime.dt.hour.astype(int)

def get_minute( df_datatime ):
    return df_datatime.dt.minute.astype(int)

def get_second( df_datatime ):
    return df_datatime.dt.second.astype(int)

def get_daytime( df_datatime ):
    return get_hour( df_datatime ) + get_minute( df_datatime )/60. + get_second( df_datatime )/60./60.

def get_weekday( df_datatime ):
    return df_datatime.dt.weekday.astype(int) + 1

def get_time_delta( df_datatime ):
    return (df_datatime - df_datatime.min()).dt.total_seconds().astype(int)

def get_weektime( df_datatime ):
    return df_datatime.dt.weekday + (( df_datatime.dt.hour + ( df_datatime.dt.minute/60. ))/24. )

def get_weekofyear( df_datatime ):
    return df_datatime.dt.weekofyear.astype(int)

def get_sin_weektime( df_datatime ):
    return np.sin( (get_weektime(df_datatime)/7.)*np.pi )**2
    
def get_sin_daytime( df_datatime ):
    return np.sin( (get_daytime(df_datatime)/24.)*np.pi )**2

