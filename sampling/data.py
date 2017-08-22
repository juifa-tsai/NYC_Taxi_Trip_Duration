#!/usr/bin/env python
import os, sys, re, time 
import numpy as np
import pandas as pd

from selectors import *
from variables import *

class data:

    def __init__( self, csv_path, debug=False ):
        self.DEBUG  = debug
        self.df     = None
        self.N0     = 0
        self.N      = 0
        self.X_names = []
        self.y_names = []
        self.X = None 
        self.y = None 
        self.loaded       = self.load_csv( csv_path=csv_path )
        self.varGenerator = variables( debug=self.DEBUG )
        self.selector     = selectors( debug=self.DEBUG )
        self.selections   = pd.DataFrame( columns=self.selector.columns )
        self.effs         = self.selector.effs.copy()


    def load_csv( self, csv_path ):
        if not os.path.isfile(csv_path):
            print ">> [ERROR] Can't find %s, or may be not a file..."% csv_path
            return False 
        else: 
            print '>> [INFO] Loading %s...'% csv_path 
            self.df        = pd.read_csv(csv_path)
            self.csv_path  = csv_path
            self.N0        = len(self.df)
            self.N         = len(self.df)
            self.variables = list(self.df)
            print '>> [INFO] Done, %d data loaded'% self.N  
            return True


    def is_loaded( self ):
        if not self.loaded : 
            print '>> [ERROR] No loaeded data, please do data::load_csv( csv_path ) first.'
            return False
        else:
            return True


    def generate_variables( self, datatype = 'train', 
                                  X_names  = None, 
                                  y_names  = None, 
                                  get_datetime_pickup  = True, 
                                  get_datetime_dropoff = False,
                                  get_distance         = True,
                                  get_speed            = True,
                                  get_cluster_kmeans   = False,
                                  get_cluster_density  = False,
                                  get_store_and_fwd_flag = True,
                                  ):
        if not self.is_loaded() : return False

        self.varGenerator.get_datetime_pickup    = get_datetime_pickup
        self.varGenerator.get_datetime_dropoff   = get_datetime_dropoff
        self.varGenerator.get_distance           = get_distance
        self.varGenerator.get_speed              = get_speed
        self.varGenerator.get_cluster_kmeans     = get_cluster_kmeans
        self.varGenerator.get_cluster_density    = get_cluster_density
        self.varGenerator.get_store_and_fwd_flag = get_store_and_fwd_flag

        print '>> [INFO] Generating variables...'
        start_time = time.time()
        self.varGenerator.create_all_variables( self.df, datatype )
        self.variables = list(self.df)
        print '>> [INFO] Done, used %s sec.'% str(time.time() - start_time)

        if X_names and y_names:
            self.get_Xy( X_names, y_names)


    def load_selection( self, cut_csv_path ):
        self.selector.load_cuts_csv( cut_csv_path )
        self.selections = self.selections.append( self.selector.cuts, ignore_index=True )


    def apply_selection( self ):
        self.df   = self.selector.apply_cuts( self.df )
        self.effs = self.effs.append( self.selector.effs, ignore_index=True )
        self.N    = len(self.df)


    def delete_variable( self, variable_name ):
        self.varGenerator.delete_variable( self.df, variable_name  )
        self.variables = list(self.df)


    def get_Xy( X_names, y_names ):   
        self.X = []
        self.y = []
        return 

    def save_csv( self, save_path, overwrite=False ):
        csv_exist = False
        if os.path.isfile(save_path): 
            if not overwrite:
                print '>> [ERROR] Can not overwrite %s, unless overwrite=True'
                return
            csv_exist = True

        dir_ = re.sub(r'(.*)/.*', r'\1', save_path)
        if not os.path.isfile(dir_) and not os.path.isdir(dir_):
            os.mkdir(dir_)
            print '>> [INFO] Created %s'% dir_

        if csv_exist: print '>> [INFO] Overwriting to %s...'% save_path
        else:         print '>> [INFO] Saving to %s...'% save_path
        self.df.to_csv(save_path, index=False)
        print '>> [INFO] Done'



    
