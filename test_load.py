#!/usr/bin/env python

import re, calendar, time, datetime
import numpy as np
import pandas as pd
import string

from sampling import *

csvfile_path  = 'data/train.csv'

### Use sampling.data

train = data( csvfile_path, debug=True )
train.varGenerator.show_pars_all()
train.varGenerator.reset_pars( 'datetime', 'year', False )
train.varGenerator.show_pars('datetime')
train.varGenerator.args_cluster_kmeans['load_path_mix']='./kmeans_mix.pkl'
train.varGenerator.args_cluster_kmeans['load_path_std_pickup'] ='./kmeans_pickup.pkl'
train.varGenerator.args_cluster_kmeans['load_path_std_dropoff']='./kmeans_dropoff.pkl'
train.varGenerator_run( 'train',
                         get_datetime_pickup=True, 
                         get_distance=True, 
                         get_speed=True, 
                         get_store_and_fwd_flag=True, 
                         get_cluster_kmeans=True )
train.delete_variable('id')
train.delete_variable('pickup_datetime')
train.delete_variable('dropoff_datetime')
train.save_csv('data/train_ext.csv', overwrite=True)
print train.df.head()
print list(train.df)

#train.load_selection('data/precuts_train.csv')
#train.apply_selection()
#print train.selections
#print train.effs

