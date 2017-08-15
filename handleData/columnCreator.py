#!/usr/bin/env python
import numpy as np
import pandas as pd
import string

def create_feature_by_column( df, applyColName, func, **kwds ):
    return df[applyColName].apply( func, **kwds )
        
def add_column( df, newColName, column ):
    df[newColName] = column
    return df
