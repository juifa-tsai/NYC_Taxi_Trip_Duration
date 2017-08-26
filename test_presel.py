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
train.generate_variables( 'train',
                          get_datetime_pickup=True, 
                          get_distance=True, 
                          get_speed=True, 
                          get_store_and_fwd_flag=True )
train.delete_variable('id')
#train.save_csv('tmp/test.csv', overwrite=True)
print train.df.head()
print list(train.df)


train.load_selection('data/precuts_train.csv')
train.apply_selection()
print train.selections
print train.effs


train.varGenerator.args_cluster_kmeans['overwrite']=True
train.generate_variables('train', get_cluster_kmeans=True )
train.save_csv('tmp/test_presel_cluster.csv', overwrite=True)

print train.df.head()
print list(train.df)
print len(train.df)

