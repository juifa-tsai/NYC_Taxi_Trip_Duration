#!/usr/bin/env python

import re, calendar, time, datetime
import numpy as np
import pandas as pd
import string

from sampling import *

csvfile_path  = 'data/train.csv'
df = pd.read_csv(csvfile_path)
N = len(df)
print '>> [INFO] Loaded %s with %d data'%( csvfile_path, N )
print '>> [INFO] Getting train sample\'s features.... %s '

start_time = time.time()
#train_feature_creater = features( debug=True )
train_feature_creater = features()
train_feature_creater.show_pars_all()
train_feature_creater.reset_pars( 'datetime', 'do_get_year', False )
train_feature_creater.show_pars('datetime')
train_feature_creater.do_datetime_dropoff = False
train_feature_creater.create_all_features( df, datatype='train' )
train_feature_creater.delete_feature(df, 'Id')
train_feature_creater.delete_feature(df, 'id')
print '>> [INFO] Done, used %s sec.'% str(time.time() - start_time)

print df.head()
print list(df)
print df['store_and_fwd_flag'].unique()

df.to_csv('../data/train_timefixed.csv', index=False)

