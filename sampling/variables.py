#!/usr/bin/env python
import numpy as np
import pandas as pd

from variables_datetime import *
from variables_cluster  import *
from variables_distance import *
from variables_helper   import *

class variables:

    def __init__( self, debug=False ):
        self.DEBUG = debug

        #self.add_variables = { 'datetime'           : { 'pickup' : True, 'dropoff': True }, 
        #                      'distance'           : True,
        #                      'cluster'            : { 'kmeans' : True, 'density': True },
        #                      'store_and_fwd_flag' : True }

        self.get_datetime_pickup    = True
        self.get_datetime_dropoff   = True
        self.get_distance           = True
        self.get_speed              = True
        self.get_cluster_kmeans     = True
        self.get_cluster_density    = True
        self.get_store_and_fwd_flag = True

        self.pars_datetime = { 'year'        : True, 
                               'month'       : True,
                               'day'         : True,
                               'hour'        : True,
                               'minute'      : True,
                               'second'      : True,
                               'daytime'     : True,
                               'weekday'     : True,
                               'digit_date'  : True,
                               'time_delta'  : True,
                               'weektime'    : True,
                               'weekofyear'  : True,
                               'sin_weektime': True,
                               'sin_daytime' : True}

        self.pars_distance = { 'haversine'   : True, 
                               'manhattan'   : True,
                               'direction'   : True}

        self.pars_speed    = { 'haversine'   : True, 
                               'manhattan'   : True}

        self.pars_cluster_kmeans  = { 'zones': True} 

        self.pars_cluster_density = { 'D'    : True,
                                      'Dstd' : True}


    #### For parameters setting ----------------------------

    def show_pars_all( self ):
        self.show_pars('datetime'       )
        self.show_pars('distance'       )
        self.show_pars('speed'          )
        self.show_pars('cluster_kmeans' )
        self.show_pars('cluster_density')


    def show_pars( self, partype ):
        if   partype == 'datetime':        self.show_pars_dict( self.pars_datetime,        'datetime'       )
        elif partype == 'distance':        self.show_pars_dict( self.pars_distance,        'distance'       )
        elif partype == 'speed':           self.show_pars_dict( self.pars_speed,           'speed'          )
        elif partype == 'cluster_kmeans':  self.show_pars_dict( self.pars_cluster_kmeans,  'cluster_kmeans' )
        elif partype == 'cluster_density': self.show_pars_dict( self.pars_cluster_density, 'cluster_density')
        else: print '>> [ERROR] unknown partype called %s, must be either datetime, distance, cluster_kmeans or cluster_density'


    def show_pars_dict( self, pars_dict, title='' ):
        print '>> [INFO] %s has %d pars '%( title, len(pars_dict) )
        for par in pars_dict:
            print '>         %-20s : %r'%(par, pars_dict[par])


    def reset_pars( self, partype, parName, value ):
        if   partype == 'datetime':        self.reset_pars_dict(  self.pars_datetime,        parName, value, partype )
        elif partype == 'distance':        self.reset_pars_dict(  self.pars_distance,        parName, value, partype )
        elif partype == 'speed':           self.reset_pars_dict(  self.pars_speed,           parName, value, partype )
        elif partype == 'cluster_kmeans':  self.reset_pars_dict(  self.pars_cluster_kmeans,  parName, value, partype )
        elif partype == 'cluster_density': self.reset_pars_dict(  self.pars_cluster_density, parName, value, partype )
        else: print '>> [ERROR] unknown partype called %s, must be either datetime, distance, cluster_kmeans or cluster_density'


    def reset_pars_dict( self, pars_dict, parName, value, title='' ):
        if not is_exist( pars_dict, parName): return
        if self.DEBUG:
            print '>> [DEBUG] %s %s: %r -> %r'%( title, parName, pars_dict[parName], value )
        pars_dict[parName] = value


    #### Feature column creation ----------------------------
    
    def create_all_variables( self, df, datatype='train' ):
        if self.DEBUG:
            print '>> [DEBUG] get_datetime_pickup    = %r'% self.get_datetime_pickup 
            print '>> [DEBUG] get_datetime_dropoff   = %r'% self.get_datetime_dropoff 
            print '>> [DEBUG] get_distance           = %r'% self.get_distance 
            print '>> [DEBUG] get_speed              = %r'% self.get_speed
            print '>> [DEBUG] get_cluster_kmeans     = %r'% self.get_cluster_kmeans
            print '>> [DEBUG] get_cluster_density    = %r'% self.get_cluster_density
            print '>> [DEBUG] get_store_and_fwd_flag = %r'% self.get_store_and_fwd_flag 

        if self.get_datetime_pickup: 
            self.create_datetime( df, 'pickup_datetime', 'pickup_' )

        if self.get_datetime_dropoff and datatype == 'train': 
            self.create_datetime( df, 'dropoff_datetime', 'dropoff_' )

        if self.get_distance:
            self.create_distance( df, 'pickup_longitude',  'pickup_latitude', 
                                      'dropoff_longitude', 'dropoff_latitude' )

        if self.get_speed and datatype == 'train':
            self.create_speed( df )

        if self.get_store_and_fwd_flag:
            newcol = create_variabel_column( df, 'store_and_fwd_flag', make_ny2bool )
            df.__delitem__('store_and_fwd_flag')
            df = add_variabel( df, 'store_and_fwd_flag', newcol )
            del newcol

        return df


    def create_datetime( self, df, dtVarName, name='' ):
        if is_exist(df, dtVarName):
            dt = variables_datetime(df, dtVarName)
            if self.pars_datetime['year']:         df[name+'year']         = dt.get_year()
            if self.pars_datetime['month']:        df[name+'month']        = dt.get_month()
            if self.pars_datetime['day']:          df[name+'day']          = dt.get_day()
            if self.pars_datetime['hour']:         df[name+'hour']         = dt.get_hour()
            if self.pars_datetime['minute']:       df[name+'minute']       = dt.get_minute()
            if self.pars_datetime['second']:       df[name+'second']       = dt.get_second()
            if self.pars_datetime['daytime']:      df[name+'daytime']      = dt.get_daytime()
            if self.pars_datetime['weekday']:      df[name+'weekday']      = dt.get_weekday()
            if self.pars_datetime['digit_date']:   df[name+'digit_date']   = dt.get_digit_date()
            if self.pars_datetime['time_delta']:   df[name+'time_delta']   = dt.get_time_delta()
            if self.pars_datetime['weektime']:     df[name+'weektime']     = dt.get_weektime()
            if self.pars_datetime['weekofyear']:   df[name+'weekofyear']   = dt.get_weekofyear()
            if self.pars_datetime['sin_weektime']: df[name+'sin_weektime'] = dt.get_sin_weektime()
            if self.pars_datetime['sin_daytime']:  df[name+'sin_daytime']  = dt.get_sin_daytime()
            del dt
        return df


    def create_distance( self, df, lng_name1, lat_name1, lng_name2, lat_name2 ):
        if not is_exist( df, lng_name1 ): return False 
        if not is_exist( df, lat_name1 ): return False
        if not is_exist( df, lng_name2 ): return False
        if not is_exist( df, lat_name2 ): return False
        distances = variables_distance( df[lng_name1].values, df[lat_name1].values,
                                        df[lng_name2].values, df[lat_name2].values )
        if self.pars_distance['haversine']: 
            df['distance_haversine'] = pd.DataFrame( distances.get_distance_haversine() )
        if self.pars_distance['manhattan']: 
            df['distance_manhattan'] = pd.DataFrame( distances.get_distance_manhattan() )  
        if self.pars_distance['direction']: 
            df['trip_direction']     = pd.DataFrame( distances.get_direction()          )  
        del distances
        return df


    def create_speed( self, df, t_name='trip_duration', name_haversine='distance_haversine', name_manhattan='distance_manhattan' ):
        if not is_exist( df, t_name ): return False

        if self.pars_speed['haversine'] and is_exist( df, name_haversine ):
            df['speed_haversine'] = df[name_haversine]/df[t_name]*60*60
        if self.pars_speed['manhattan'] and is_exist( df, name_manhattan ):
            df['speed_manhattan'] = df[name_manhattan]/df[t_name]*60*60
        return df



    def delete_variable( self, df, variable_name ):
        if variable_name in list(df):
            df.__delitem__(variable_name)
            if self.DEBUG:
                print '>> [DEBUG] %s is dropped from dataframe'% variable_name
        else:
            print '>> [ERROR] No %s in dataframe for delete'% variable_name
        return df
