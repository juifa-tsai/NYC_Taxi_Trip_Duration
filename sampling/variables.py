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

        self.pars_cluster_kmeans  = { 'mix' : True,
                                      'std' : True} 

        self.pars_cluster_density = { 'D'    : True,
                                      'Dstd' : True}

        self.args_cluster_kmeans = { 'load_path_mix'        : '', 
                                     'load_path_std_pickup' : '', 
                                     'load_path_std_dropoff': '',
                                     'save_path_mix'        : './kmeans_mix.pkl',
                                     'save_path_std_pickup' : './kmeans_pickup.pkl', 
                                     'save_path_std_dropoff': './kmeans_dropoff.pkl',
                                     'overwrite'            : False,
                                     'use_sample'           : None,
                                     'batch_size'           : 10000,
                                     'n_zone'               : 100}


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
        else: print '>> [ERROR] variables::show_pars : unknown partype called %s, must be either datetime, distance, cluster_kmeans or cluster_density'


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
        else: print '>> [ERROR] variables::reset_pars : unknown partype called %s, must be either datetime, distance, cluster_kmeans or cluster_density'


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
            self.create_datetime( df, dtVarName = 'pickup_datetime', 
                                           name = 'pickup_')

        if self.get_datetime_dropoff and datatype == 'train': 
            self.create_datetime( df, dtVarName = 'dropoff_datetime', 
                                           name = 'dropoff_')

        if self.get_distance:
            self.create_distance( df, lng_name1 = 'pickup_longitude',  
                                      lat_name1 = 'pickup_latitude', 
                                      lng_name2 = 'dropoff_longitude', 
                                      lat_name2 = 'dropoff_latitude')

        if self.get_speed and datatype == 'train':
            self.create_speed( df, name_haversine = 'distance_haversine', 
                                   name_manhattan = 'distance_manhattan',
                                           t_name = 'trip_duration') 

        if self.get_cluster_kmeans:
            self.create_cluster_kmeans( df,  pickup_lng = 'pickup_longitude',  
                                             pickup_lat = 'pickup_latitude',
                                            dropoff_lng = 'dropoff_longitude', 
                                            dropoff_lat = 'dropoff_latitude',
                                        load_path_mix         = self.args_cluster_kmeans['load_path_mix'], 
                                        load_path_std_pickup  = self.args_cluster_kmeans['load_path_std_pickup'], 
                                        load_path_std_dropoff = self.args_cluster_kmeans['load_path_std_dropoff'],
                                        save_path_mix         = self.args_cluster_kmeans['save_path_mix'],
                                        save_path_std_pickup  = self.args_cluster_kmeans['save_path_std_pickup'], 
                                        save_path_std_dropoff = self.args_cluster_kmeans['save_path_std_dropoff'],
                                        overwrite             = self.args_cluster_kmeans['overwrite'],
                                        use_sample            = self.args_cluster_kmeans['use_sample'],
                                        batch_size            = self.args_cluster_kmeans['batch_size'],
                                        n_zone                = self.args_cluster_kmeans['n_zone'])

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
        if not is_exist( df, lng_name1 ): return df 
        if not is_exist( df, lat_name1 ): return df
        if not is_exist( df, lng_name2 ): return df
        if not is_exist( df, lat_name2 ): return df
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


    def create_speed( self, df, t_name, name_haversine, name_manhattan ):
        if not is_exist( df, t_name ): return df

        if self.pars_speed['haversine'] and is_exist( df, name_haversine ):
            df['speed_haversine'] = df[name_haversine]/df[t_name]*60*60
        if self.pars_speed['manhattan'] and is_exist( df, name_manhattan ):
            df['speed_manhattan'] = df[name_manhattan]/df[t_name]*60*60
        return df


    def create_cluster_kmeans( self, df, 
                               pickup_lng,   
                               pickup_lat, 
                               dropoff_lng, 
                               dropoff_lat,
                               load_path_mix='', 
                               load_path_std_pickup='', 
                               load_path_std_dropoff='',
                               save_path_mix='./kmeans_mix.pkl',
                               save_path_std_pickup='./kmeans_pickup.pkl', 
                               save_path_std_dropoff='./kmeans_dropoff.pkl',
                               overwrite =False,
                               use_sample=None,
                               batch_size=10000,
                               n_zone=100 ):
        if not is_exist( df, pickup_lng ):  return df
        if not is_exist( df, pickup_lat ):  return df
        if not is_exist( df, dropoff_lng ): return df
        if not is_exist( df, dropoff_lat ): return df

        df_pickup  = df[[ pickup_lng,  pickup_lat ]]
        df_dropoff = df[[ dropoff_lng, dropoff_lat]]

        if self.pars_cluster_kmeans['mix']:
            if os.path.isfile(load_path_mix):
                print '>> [INFO] variables::create_cluster_kmeans : loaded the input cluster with mix case....'
                kmeans = cluster_kmeans().init_cluster( load_path = load_path_mix )

            else:
                print '>> [INFO] variables::create_cluster_kmeans : fitting the cluster with mix case....'
                df_mix = pd.DataFrame( np.vstack((df_pickup.values, df_dropoff.values)), columns=['longitude','latitude'])
                kmeans = cluster_kmeans( df_mix, ['longitude','latitude'], self.DEBUG )
                kmeans.init_cluster( batch_size = batch_size, n_zone = n_zone )
                kmeans.fit( use_sample )
                kmeans.save_cluster( save_path_mix, overwrite )

            df['zone_kmeans_mix_pickup' ] = pd.DataFrame( kmeans.predict( df_pickup.values  ))
            df['zone_kmeans_mix_dropoff'] = pd.DataFrame( kmeans.predict( df_dropoff.values ))

        if self.pars_cluster_kmeans['std']:
            if os.path.isfile(load_path_std_pickup) and os.path.isfile(load_path_std_dropoff):
                print '>> [INFO] variables::create_cluster_kmeans : loaded the input cluster with std case....'
                kmeans_pickup  = cluster_kmeans().init_cluster( load_path = load_path_std_pickup )
                kmeans_dropoff = cluster_kmeans().init_cluster( load_path = load_path_std_dropoff )

            else:
                print '>> [INFO] variables::create_cluster_kmeans : fitting the cluster with std case....'
                kmeans_pickup  = cluster_kmeans( df_pickup,  [ pickup_lng,  pickup_lat], self.DEBUG )
                kmeans_pickup.init_cluster(  batch_size = batch_size, n_zone = n_zone )
                kmeans_pickup.fit( use_sample )
                kmeans_pickup.save_cluster( save_path_std_pickup, overwrite )

                kmeans_dropoff = cluster_kmeans( df_dropoff, [dropoff_lng, dropoff_lat], self.DEBUG )
                kmeans_dropoff.init_cluster( batch_size = batch_size, n_zone = n_zone )
                kmeans_dropoff.fit( use_sample )
                kmeans_dropoff.save_cluster( save_path_std_dropoff, overwrite )

            df['zone_kmeans_std_pickup' ] = pd.DataFrame( kmeans_pickup.predict(  df_pickup.values  ))
            df['zone_kmeans_std_dropoff'] = pd.DataFrame( kmeans_dropoff.predict( df_dropoff.values ))


    #def create_expacted_duration( self, df ):




    def delete_variable( self, df, variable_name ):
        if variable_name in list(df):
            df.__delitem__(variable_name)
            if self.DEBUG:
                print '>> [DEBUG] %s is dropped from dataframe'% variable_name
        else:
            print '>> [ERROR] No %s in dataframe for delete'% variable_name
        return df
