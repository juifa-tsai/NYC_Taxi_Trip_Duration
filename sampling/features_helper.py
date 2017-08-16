#!/usr/bin/env python
import numpy as np
import pandas as pd

def create_variabel_column( df, applyVarName, func, **kwds ):
    return df[applyVarName].apply( func, **kwds )
        
def add_variabel( df, addVarName, addVarColumn ):
    df[addVarName] = addVarColumn 
    return df
