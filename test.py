#!/usr/bin/env python

import re, calendar, time, datetime
import numpy as np
import pandas as pd
import string

from sampling import *
from sampling.features import *

csvfile_path  = 'data/train.csv'
df = pd.read_csv(csvfile_path)
N = len(df)
print '>> [INFO] Loaded %s with %d data'%( csvfile_path, N )
print '>> [INFO] Getting train sample\'s features.... %s '

start_time = time.time()
train_feature_creater = features( debug=True )
train_feature_creater.show_all_pars()
train_feature_creater.reset_pars( 'datetime', 'do_get_year', False )
train_feature_creater.show_all_pars()
train_feature_creater.create_all_features( df, datatype='train', get_dropoff_datetime=False )
train_feature_creater.drop_feature(df, 'Id')
train_feature_creater.drop_feature(df, 'id')
print '>> [INFO] Done, used %s sec.'% str(time.time() - start_time)

print df.head()
print list(df)

