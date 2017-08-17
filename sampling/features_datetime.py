#!/usr/bin/env python
import numpy as np
import pandas as pd

class feature_datetime:

    def __init__( self, df, dtVarName ):
        self.datetime = pd.to_datetime( df[dtVarName] )

    def get_year(self):
        return self.datetime.dt.year.astype(int)

    def get_month(self):
        return self.datetime.dt.month.astype(int)

    def get_day(self):
        return self.datetime.dt.day.astype(int)
    
    def get_hour(self):
        return self.datetime.dt.hour.astype(int)
    
    def get_minute(self):
        return self.datetime.dt.minute.astype(int)
    
    def get_second(self):
        return self.datetime.dt.second.astype(int)
    
    def get_daytime(self):
        return self.get_hour() + self.get_minute()/60. + self.get_second()/60./60.
    
    def get_weekday(self):
        return self.datetime.dt.weekday.astype(int) + 1
    
    def get_time_delta(self):
        return (self.datetime - self.datetime.min()).dt.total_seconds().astype(int)
    
    def get_weektime(self):
        return self.datetime.dt.weekday + (( self.datetime.dt.hour + ( self.datetime.dt.minute/60. ))/24. )
    
    def get_weekofyear(self):
        return self.datetime.dt.weekofyear.astype(int)
    
    def get_sin_weektime(self):
        return np.sin( (self.get_weektime()/7.)*np.pi )**2
    
    def get_sin_daytime(self):
        return np.sin( (self.get_daytime()/24.)*np.pi )**2
    
