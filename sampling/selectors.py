#!/usr/bin/env python
import os, sys, re
import numpy as np
import pandas as pd

from variables_helper import *

infmin = -float('Inf')
infmax =  float('Inf')

class selectors:

    def __init__( self, csv_path=None, debug=False ):
        self.cuts   = None
        self.loaded = False
        self.columns = [ 'name',     
                         'cut_min',  
                         'cut_max',  
                         'isBetween',]
        if not csv_path:
            self.cuts = pd.DataFrame( { self.columns[0]: [],
                                        self.columns[1]: [],
                                        self.columns[2]: [],
                                        self.columns[3]: []})
        else:
            self.loaded = self.load_cuts_csv( csv_path )

    def load_cuts_csv( self, csv_path ):
        if not os.path.isfile(csv_path):
            print ">> [ERROR] Can't find %s, or may be not a file..."% csv_path
            return False 
        else: 
            self.cuts      = pd.read_csv(csv_path)
            self.csv_path  = csv_path
            return True

        ## Format of cut csv:
        ## name, cut_min, cut_max, isBetween


    def is_loaded( self ):
        if not self.loaded : 
            print '>> [ERROR] No loaeded data, please do selector::load_cuts_csv( csv_path ) first.'
            return False
        else:
            return True


    def cutbase_selector( self, df, name, cut_min=infmin, cut_max=infmax, isBetween=True ):
        if not is_exist( df, name ): return
        if isBetween:
            return df[ ( df[name] >= cut_min ) & ( df[name] < cut_max ) ]
        else:
            return df[ ( df[name] <= cut_min ) | ( df[name] > cut_max ) ]   


    def apply_cuts( self, df ):
        if not self.is_loaded() : return df

        N0 = len(df)
        for i in range(len(self.cuts)): 
            df = self.cutbase_selector( df,
                                        self.cuts.get_value( i, 'name'     ), 
                                        self.cuts.get_value( i, 'cut_min'  ),
                                        self.cuts.get_value( i, 'cut_max'  ),
                                        self.cuts.get_value( i, 'isBetween'))
        print '>> [INFO] Cuts applied, %d date left, eff: %.2f'%( len(df), float(len(df))/float(N0) )
        return df 


    def add_cut( self, name, cut_min, cut_max, isBetween ):
        df = pd.DataFrame( [[name, cut_min, cut_max, isBetween]], columns=self.columns )
        self.cuts = self.cuts.append( df, ignore_index=True )


    def save_csv( self, save_path, overwrite=False ):
        csv_exist = False
        if os.path.isfile(save_path): 
            if not overwrite:
                print '>> [ERROR] Can not overwrite %s, unless overwrite=True'
                return
            csv_exist = True

        dir_ = re.sub(r'(.*)/.*', r'\1', save_path)
        if not os.path.isfile(dir_) and not os.path.isdir(dir_):
            os.mkdir(dir_)
            print '>> [INFO] Created %s'% dir_

        if csv_exist: print '>> [INFO] Overwriting to %s...'% save_path
        else:         print '>> [INFO] Saving to %s...'% save_path
        self.cuts.to_csv(save_path, index=False)
        print '>> [INFO] Done'


