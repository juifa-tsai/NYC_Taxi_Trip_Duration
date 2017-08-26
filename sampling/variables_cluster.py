#!/usr/bin/env python
import numpy as np
import pandas as pd
import pickle, re, os, time
from sklearn.cluster import *
from variables_helper import *

#class variables_cluster(object):
class cluster_kmeans:

    def __init__( self, df=None, var_names=[], debug=False):

        self.DEBUG = debug
        self.df        = df
        self.cluster   = MiniBatchKMeans()
        self.var_names = var_names
        self.X      = None 
        self.n_data = 0
        self.n_vars = 0

        if self.df is not None and self.var_names is not []:
            print '>> [INFO] cluster_kmeans::__init__ : loading dataframe and variabels...'
            if not is_exist( df, var_names ): return 
            else:
                self.var_names = var_names
                self.X      = self.df[self.var_names].values
                self.n_data = self.X.shape[0]
                self.n_vars = self.X.shape[1]


    def init_cluster( self, load_path='', batch_size=10000, n_zone=100, random_state=1, **kwd ):
        if os.path.isfile(load_path):
            self.cluster = pickle.load( open(load_path, 'rb'))
            if self.DEBUG:
                print '>> [INFO] cluster_kmeans::init_cluster : loaded cluster file: %s'% load_path
        else:
            self.cluster = MiniBatchKMeans( n_clusters   = n_zone,
                                            batch_size   = batch_size,
                                            random_state = random_state,
                                            **kwd )
            if self.DEBUG:
                print '>> [INFO] cluster_kmeans::init_cluster : create new kMeans cluster %s'% load_path

        return self


    def shuffel(self, use_sample=None, random_state=1):
        np.random.seed(random_state)
        return self.df.reindex(np.random.permutation(self.df.index)).values[:self.n_data if not use_sample else use_sample]


    def fit( self, use_sample=None, random_state=1 ):
        start_time = time.time()
        self.cluster.fit( self.shuffel( use_sample, random_state))
        if self.DEBUG:
            print '>> [DEBUG] cluster_kmeans::fit : used %.2f sec.'%(time.time() - start_time)
        return self


    def predict( self, X=None ):
        return self.cluster.predict( self.X if not X.any() else X )


    def save_cluster( self, save_path='./kmeans.pkl', overwrite=False, protocol=2 ):
        is_writable_ = is_writable( save_path, overwrite )
        if not is_writable_[0]:
            return False
        if is_writable_[1] : print '>> [INFO] Overwriting to %s...'% save_path
        else:                print '>> [INFO] Saving to %s...'% save_path
        pickle.dump( self.cluster, open( save_path, 'wb' ), protocol=protocol )
        print '>> [INFO] Done'
        return True
