#!/usr/bin/env python
import numpy as np
import pandas as pd

def create_variabel_column( df, applyVarName, func, **kwds ):
    return df[applyVarName].apply( func, **kwds )
        
def add_variabel( df, addVarName, addVarColumn ):
    df[addVarName] = addVarColumn 
    return df

def is_exist( df, name ):
    if name not in list(df):
        print '>> [ERROR] No %s exist, do nothing'% name
        return False
    else:
        return True

def make_ny2bool( ny_str ):
    return 1 if ny_str.upper() == 'Y' else 0

def relace_none( var, value ):
    if var is None:
        if value is None:
            print '>> [ERROR] Input None value'
            return False
        else:
            return value
