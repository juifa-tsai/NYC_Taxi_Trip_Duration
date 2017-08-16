#!/usr/bin/env python
import numpy as np
import pandas as pd

from datetime import *
from clustering import *
from features_helper import *

class features:

    def __init__( self, debug=False ):
        self.DEBUG = debug
        self.do_datetime           = True
        self.do_cluster_kmeans  = True
        self.do_cluster_density = True
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
        self.pars_cluster_kmeans  = { 'do_get_zones': True}  
        self.pars_cluster_density = { 'do_get_D'   : True,
                                      'do_get_Dstd': True,}


    def show_all_pars( self ):
        self.show_pars( self.pars_datetime,        'datetime'       )
        self.show_pars( self.pars_cluster_kmeans,  'cluster_kmeans' )
        self.show_pars( self.pars_cluster_density, 'cluster_density')

    def show_pars( self, pars_dict, title='' ):
        print '>> [INFO] %s has %d pars '%( title, len(pars_dict) )
        for par in pars_dict:
            print '>         %-20s : %r'%(par, pars_dict[par])

    def reset_pars( self, partype, parName, value ):
        if   partype == 'datetime':        self.reset_pars_dict(  self.pars_datetime,        parName, value, partype )
        elif partype == 'cluster_kmeans':  self.reset_pars_dict(  self.pars_cluster_kmeans,  parName, value, partype )
        elif partype == 'cluster_density': self.reset_pars_dict(  self.pars_cluster_density, parName, value, partype )
        else: print '>> [ERROR] unknown partype called %s, must be either datetime, cluster_kmeans or cluster_density'

    def reset_pars_dict( self, pars_dict, parName, value, title='' ):
        if self.DEBUG:
            print '>> [DEBUG] %s %s: %r -> %r'%( title, parName, pars_dict[parName], value )
        pars_dict[parName] = value

    def create_all_features( self, df, datatype='train', get_dropoff_datetime=True ):
        if datatype != 'train': 
            get_dropoff_datetime = False

        if self.DEBUG:
            print '>> [DEBUG] do_datetime = %r'%        self.do_datetime 
            print '>> [DEBUG] do_cluster_kmeans = %r'%  self.do_cluster_kmeans
            print '>> [DEBUG] do_cluster_density = %r'% self.do_cluster_density

        if self.do_datetime: 
            self.create_datetime( df, 'pickup_datetime', 'pickup_' )
            if get_dropoff_datetime:
                self.create_datetime( df, 'dropoff_datetime', 'dropoff_' )

        return df

    def create_datetime( self, df, dtVarName, name='' ):
        if dtVarName in list(df): 
            df_dt = pd.to_datetime( df[dtVarName] )
            if self.pars_datetime['do_get_year']:         df[name+'year']         = get_year(         df_dt )
            if self.pars_datetime['do_get_month']:        df[name+'month']        = get_month(        df_dt )
            if self.pars_datetime['do_get_day']:          df[name+'day']          = get_day(          df_dt )
            if self.pars_datetime['do_get_hour']:         df[name+'hour']         = get_hour(         df_dt )
            if self.pars_datetime['do_get_minute']:       df[name+'minute']       = get_minute(       df_dt )
            if self.pars_datetime['do_get_second']:       df[name+'second']       = get_second(       df_dt )
            if self.pars_datetime['do_get_daytime']:      df[name+'daytime']      = get_daytime(      df_dt )
            if self.pars_datetime['do_get_weekday']:      df[name+'weekday']      = get_weekday(      df_dt )
            if self.pars_datetime['do_get_time_delta']:   df[name+'time_delta']   = get_time_delta(   df_dt )
            if self.pars_datetime['do_get_weektime']:     df[name+'weektime']     = get_weektime(     df_dt )
            if self.pars_datetime['do_get_weekofyear']:   df[name+'weekofyear']   = get_weekofyear(   df_dt )
            if self.pars_datetime['do_get_sin_weektime']: df[name+'sin_weektime'] = get_sin_weektime( df_dt )
            if self.pars_datetime['do_get_sin_daytime']:  df[name+'sin_daytime']  = get_sin_daytime(  df_dt )
        else:
            print '>> [ERROR] No %s exist, do nothing'% dtVarName
        return df


    def drop_feature( self, df, feature_name ):
        if feature_name in list(df):
            df.__delitem__(feature_name)
            if self.DEBUG:
                print '>> [DEBUG] %s is dropped from dataframe'% feature_name
        else:
            print '>> [ERROR] No %s in dataframe for delete'% feature_name
        return df


