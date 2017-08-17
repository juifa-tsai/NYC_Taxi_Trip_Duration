#!/usr/bin/env python
import numpy as np
import pandas as pd

from features_datetime import *
from features_cluster  import *
from features_distance import *
from features_helper   import *

class features:

    def __init__( self, debug=False ):
        self.DEBUG = debug

        self.do_datetime           = True
        self.do_distance           = True
        self.do_cluster_kmeans     = True
        self.do_cluster_density    = True
        self.do_store_and_fwd_flag = True

        self.pars_datetime = { 'do_get_year'        : True, 
                               'do_get_month'       : True,
                               'do_get_day'         : True,
                               'do_get_hour'        : True,
                               'do_get_minute'      : True,
                               'do_get_second'      : True,
                               'do_get_daytime'     : True,
                               'do_get_weekday'     : True,
                               'do_get_time_delta'  : True,
                               'do_get_weektime'    : True,
                               'do_get_weekofyear'  : True,
                               'do_get_sin_weektime': True,
                               'do_get_sin_daytime' : True}

        self.pars_distance = { 'do_get_haversine'   : True, 
                               'do_get_manhattan'   : True}

        self.pars_cluster_kmeans  = { 'do_get_zones': True} 

        self.pars_cluster_density = { 'do_get_D'    : True,
                                      'do_get_Dstd' : True}


    def show_all_pars( self ):
        self.show_pars( self.pars_datetime,        'datetime'       )
        self.show_pars( self.pars_distance,        'distance'       )
        self.show_pars( self.pars_cluster_kmeans,  'cluster_kmeans' )
        self.show_pars( self.pars_cluster_density, 'cluster_density')


    def show_pars( self, pars_dict, title='' ):
        print '>> [INFO] %s has %d pars '%( title, len(pars_dict) )
        for par in pars_dict:
            print '>         %-20s : %r'%(par, pars_dict[par])


    def reset_pars( self, partype, parName, value ):
        if   partype == 'datetime':        self.reset_pars_dict(  self.pars_datetime,        parName, value, partype )
        elif partype == 'distance':        self.reset_pars_dict(  self.pars_distance,        parName, value, partype )
        elif partype == 'cluster_kmeans':  self.reset_pars_dict(  self.pars_cluster_kmeans,  parName, value, partype )
        elif partype == 'cluster_density': self.reset_pars_dict(  self.pars_cluster_density, parName, value, partype )
        else: print '>> [ERROR] unknown partype called %s, must be either datetime, distance, cluster_kmeans or cluster_density'


    def reset_pars_dict( self, pars_dict, parName, value, title='' ):
        if self.DEBUG:
            print '>> [DEBUG] %s %s: %r -> %r'%( title, parName, pars_dict[parName], value )
        pars_dict[parName] = value


    def create_all_features( self, df, datatype='train', get_dropoff_datetime=True ):
        if datatype != 'train': 
            get_dropoff_datetime = False

        if self.DEBUG:
            print '>> [DEBUG] do_datetime           = %r'% self.do_datetime 
            print '>> [DEBUG] do_distance           = %r'% self.do_distance 
            print '>> [DEBUG] do_cluster_kmeans     = %r'% self.do_cluster_kmeans
            print '>> [DEBUG] do_cluster_density    = %r'% self.do_cluster_density
            print '>> [DEBUG] do_store_and_fwd_flag = %r'% self.do_store_and_fwd_flag 

        if self.do_datetime: 
            self.create_datetime( df, 'pickup_datetime', 'pickup_' )
            if get_dropoff_datetime:
                self.create_datetime( df, 'dropoff_datetime', 'dropoff_' )

        if self.do_distance:
            self.create_distance( df, 'pickup_longitude',  'pickup_latitude', 
                                      'dropoff_longitude', 'dropoff_latitude' )

        if self.do_store_and_fwd_flag:
            newcol = create_variabel_column( df, 'store_and_fwd_flag', make_ny2bool )
            df.__delitem__('store_and_fwd_flag')
            df = add_variabel( df, 'store_and_fwd_flag', newcol )
            del newcol

        return df


    def create_datetime( self, df, dtVarName, name='' ):
        if is_exist(df, dtVarName):
            dt = feature_datetime(df, dtVarName)
            if self.pars_datetime['do_get_year']:         df[name+'year']         = dt.get_year()
            if self.pars_datetime['do_get_month']:        df[name+'month']        = dt.get_month()
            if self.pars_datetime['do_get_day']:          df[name+'day']          = dt.get_day()
            if self.pars_datetime['do_get_hour']:         df[name+'hour']         = dt.get_hour()
            if self.pars_datetime['do_get_minute']:       df[name+'minute']       = dt.get_minute()
            if self.pars_datetime['do_get_second']:       df[name+'second']       = dt.get_second()
            if self.pars_datetime['do_get_daytime']:      df[name+'daytime']      = dt.get_daytime()
            if self.pars_datetime['do_get_weekday']:      df[name+'weekday']      = dt.get_weekday()
            if self.pars_datetime['do_get_time_delta']:   df[name+'time_delta']   = dt.get_time_delta()
            if self.pars_datetime['do_get_weektime']:     df[name+'weektime']     = dt.get_weektime()
            if self.pars_datetime['do_get_weekofyear']:   df[name+'weekofyear']   = dt.get_weekofyear()
            if self.pars_datetime['do_get_sin_weektime']: df[name+'sin_weektime'] = dt.get_sin_weektime()
            if self.pars_datetime['do_get_sin_daytime']:  df[name+'sin_daytime']  = dt.get_sin_daytime()
            del dt
        return df


    def create_distance( self, df, lng_name1, lat_name1, lng_name2, lat_name2 ):
        if not is_exist( df, lng_name1 ): return False 
        if not is_exist( df, lat_name1 ): return False
        if not is_exist( df, lng_name2 ): return False
        if not is_exist( df, lat_name2 ): return False
        distances = feature_distance( df[lng_name1].values, df[lat_name1].values,
                                      df[lng_name2].values, df[lat_name2].values )
        if self.pars_distance['do_get_haversine']: 
            df['distance_haversine'] = pd.DataFrame( distances.get_distance_haversine() )
        if self.pars_distance['do_get_manhattan']: 
            df['distance_manhattan'] = pd.DataFrame( distances.get_distance_manhattan() )  
        del distances
        return df


    def delete_feature( self, df, feature_name ):
        if feature_name in list(df):
            df.__delitem__(feature_name)
            if self.DEBUG:
                print '>> [DEBUG] %s is dropped from dataframe'% feature_name
        else:
            print '>> [ERROR] No %s in dataframe for delete'% feature_name
        return df

