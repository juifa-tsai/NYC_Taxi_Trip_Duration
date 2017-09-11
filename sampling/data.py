#!/usr/bin/env python
import os, sys, re, time 
import numpy as np
import pandas as pd

from selectors import *
from variables import *
from sklearn.model_selection import cross_val_score, train_test_split, ShuffleSplit

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
        self.X_train = None 
        self.X_test  = None 
        self.y_train = None 
        self.y_test  = None
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
            return self 


    def is_loaded( self ):
        if not self.loaded : 
            print '>> [ERROR] No loaeded data, please do data::load_csv( csv_path ) first.'
            return False
        else:
            return True


    def varGenerator_run( self, datatype = 'train', 
                                X_names  = None, 
                                y_names  = None, 
                                get_datetime_pickup  = False, 
                                get_datetime_dropoff = False,
                                get_distance         = False,
                                get_speed            = False,
                                get_cluster_kmeans   = False,
                                get_cluster_density  = False,
                                get_store_and_fwd_flag = False,
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

        return self


    def load_selection( self, cut_csv_path ):
        self.selector.load_cuts_csv( cut_csv_path )
        self.selections = self.selections.append( self.selector.cuts, ignore_index=True )
        return self


    def apply_selection( self ):
        self.df   = self.selector.apply_cuts( self.df )
        self.effs = self.effs.append( self.selector.effs, ignore_index=True )
        self.N    = len(self.df)
        return self


    def summary( self ):
        df_sum = self.selections.copy()
        df_sum[['N', 'rel_eff']] = self.effs[['N', 'eff']]
        print '>> --------------------------------------------------------------------------'
        print '>> [INFO] data::summary() : summery of selections as following list'
        print df_sum
        print '>  Total selection efficiency : %.4f'% df_sum['rel_eff'].prod(0)
        print '>> --------------------------------------------------------------------------'


    def delete_variable( self, variable_name ):
        self.varGenerator.delete_variable( self.df, variable_name  )
        self.variables = list(self.df)
        return self


    def get_Xy( X_names, y_names ):  
        if not is_exist( self.df, X_names ): return self
        if not is_exist( self.df, y_names ): return self
        self.X = self.df[X_names].values
        self.y = self.df[y_names].values
        return self


    def Xy( test_size=.3, random_state=3 ):
        self.get_Xy( self.X_names, self.y_names )
        self.split_traintest( self.X, self.y, test_size, random_state )
        return self


    def split_traintest( X, y, test_size=.3, random_state=3 ):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split( X, y, test_size=test_size, random_state=random_state)
        return self


    def save_csv( self, save_path, overwrite=False ):
        is_writable_ = is_writable( save_path, overwrite )
        if not is_writable_[0]: 
            return False
        if is_writable_[1] : print '>> [INFO] Overwriting to %s...'% save_path
        else:                print '>> [INFO] Saving to %s...'% save_path
        self.df.to_csv(save_path, index=False)
        print '>> [INFO] Done'
        return True



    
