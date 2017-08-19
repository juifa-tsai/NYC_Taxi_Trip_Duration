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
train.varGenerator.get_datetime_dropoff = False
train.generate_all_variables('train')
train.delete_variable('Id')
train.delete_variable('id')
train.save_csv('tmp/test.csv', overwrite=True)

print train.df.head()
print train.variables, len(train.variables)
print list(train.df)


### Use sampling.variables
#
#df = pd.read_csv(csvfile_path)
#N = len(df)
#print '>> [INFO] Loaded %s with %d data'%( csvfile_path, N )
#print '>> [INFO] Getting train sample\'s variables.... %s '
#
#start_time = time.time()
##train_variable_creater = variables( debug=True )
#train_variable_creater = variables()
#train_variable_creater.show_pars_all()
#train_variable_creater.reset_pars( 'datetime', 'year', False )
#train_variable_creater.show_pars('datetime')
#train_variable_creater.get_datetime_dropoff = False
#train_variable_creater.create_all_variables( df, datatype='train' )
#train_variable_creater.delete_variable(df, 'Id')
#train_variable_creater.delete_variable(df, 'id')
#print '>> [INFO] Done, used %s sec.'% str(time.time() - start_time)
#
#print df.head()
#print list(df)
#print df['store_and_fwd_flag'].unique()
#
