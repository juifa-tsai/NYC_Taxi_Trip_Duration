#!/usr/bin/env python
import numpy as np
import pandas as pd
import pickle, re, os
from sklearn.cluster import *
from variables_helper import *

#class variables_cluster(object):
class cluster_kmeans:

    def __init__(self, df, var_names, debug=False):

        if not is_exist( df, var_names ): return

        self.DEBUG = debug

        self.df      = df
        self.cluster = MiniBatchKMeans()

        self.var_names    = var_names
        self.random_state = random_state

        self.X = self.df[[self.var_names]].values
        self.n_data = self.X.shape[0]
        self.n_vars = self.X.shape[1]


    def init_cluster(self, load_path='', use_sample=500000, batch_size=10000, n_zone=100, random_state=1 ):
        if os.path.isfile(load_path):
            self.cluster = pickle.load( open(load_path, 'rb'))
            if self.DEBUG: 
                print '>> [INFO] cluster_kmeans::init_cluster : loaded cluster file: %s'% load_path
        else:
            self.cluster = MiniBatchKMeans( n_clusters   = n_zone,
                                            batch_size   = batch_size,
                                            random_state = random_state)
            if self.DEBUG: 
                print '>> [INFO] cluster_kmeans::init_cluster : create new kMeans cluster %s'% load_path


    def shuffel(self, use_sample=None, random_state=1):
        np.random.seed(random_state)
        return self.df.reindex(np.random.permutation(self.df.index)).values[:use_sample]


    def fit( self, use_sample=-1, random_state=1 ):
        start_time = time.time()
        self.cluster.fit( self.shuffel( use_sample   = self.n_data if use_sample is -1 else use_sample,
                                        random_state = random_state))
        if self.DEBUG:
            print '>> [DEBUG] cluster_kmeans::fit : used %.2f sec.'%(time.time() - start_time)


    def predict( self ):
        return self.cluster.predict( self.X )


    def predict_to_df( self, df_predict ):
        return pd.DataFrame(self.predict(df_predict.values))


    def save_cluster( self, save_path='./kmeans.pkl', overwrite=False, protocol=3 ):
        is_writable_ = is_writable( save_path, overwrite )
        if not is_writable_[0]: 
            return False
        if is_writable_[1] : print '>> [INFO] Overwriting to %s...'% save_path
        else:                print '>> [INFO] Saving to %s...'% save_path
        pickle.dump( self.cluster, open( save_path, 'wb' ), protocol=protocol )
        print '>> [INFO] Done'
        return True

