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
train.generate_variables('train')
train.delete_variable('Id')
train.delete_variable('id')
#train.save_csv('tmp/test.csv', overwrite=True)
print train.df.head()
print list(train.df)

train.load_selection('data/precuts_train.csv')
train.apply_selection()
print train.selections
print train.effs

