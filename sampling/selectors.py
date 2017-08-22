#!/usr/bin/env python
import os, sys, re
import numpy as np
import pandas as pd

from variables_helper import *

infmin = -float('Inf')
infmax =  float('Inf')

class selectors:

    def __init__( self, csv_path=None, debug=False ):
        self.DEBUG  = debug
        self.cuts   = None
        self.loaded = False
        self.columns = [ 'name',     
                         'cut_min',  
                         'cut_max',  
                         'isBetween']
        self.columns_eff = [ 'name', 'N', 'eff' ]  
        self.effs = pd.DataFrame( columns=self.columns_eff )
        if not csv_path:
            self.cuts = pd.DataFrame( columns=self.columns )
        else:
            self.load_cuts_csv( csv_path )

    def load_cuts_csv( self, csv_path ):
        ## Format of cut csv:
        ## name, cut_min, cut_max, isBetween
        if not os.path.isfile(csv_path):
            print ">> [ERROR] Can't find %s, or may be not a file..."% csv_path
            return False 
        else: 
            self.cuts      = pd.read_csv(csv_path)
            self.csv_path  = csv_path
            self.loaded    = True
            if self.DEBUG:
                print '>> [DEBUG] cuts list: '
                self.showCuts()


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

        N0  = float(len(df))
        N_  = N0
        eff = N_/N0
        self.effs = pd.DataFrame( columns=['name', 'eff'] )
        for i in range(len(self.cuts)): 
            df = self.cutbase_selector( df,
                                        self.cuts.get_value( i, 'name'     ), 
                                        self.cuts.get_value( i, 'cut_min'  ),
                                        self.cuts.get_value( i, 'cut_max'  ),
                                        self.cuts.get_value( i, 'isBetween'))
            eff = len(df)/float(N_)
            N_  = len(df)
            self.effs = self.effs.append( pd.DataFrame([[self.cuts.get_value(i,'name'), N_, eff]], columns=self.columns_eff ) )
            self.effs = self.effs[self.columns_eff]
        print '>> [INFO] Cuts applied, %d date left, eff: %.2f'%( N_, N_/N0 )
        return df 


    def add_cut( self, name, cut_min, cut_max, isBetween ):
        df = pd.DataFrame( [[str(name), float(cut_min), float(cut_max), bool(isBetween)]], columns=self.columns )
        self.cuts = self.cuts.append( df, ignore_index=True )


    def change_cut( self, name_idx, label, value ):
        idx = [name_idx]
        if type(name_idx) is str:
            idx = self.cuts[ self.cuts['name'] == name_idx ].index.tolist()

        if len(idx) is not 1:
            print '>> [ERROR] selectors::change_cut() : multiple indexes found by named %s'% name_idx
            return

        #if type(self.cuts[label][idx].values[0]) != type(value):
        #    print self.cuts[label][idx].values[0]
        #    print '>> [ERROR] selectors::change_cut() : different type from %s to %s'% (type(self.cuts[label][idx].values[0]).__name__, type(value).__name__)
        #    return

        self.cuts.set_value( idx, label, value)



    def remove_cut( self, name_idx ):
        idx = [name_idx]
        if type(name_idx) is str:
            idx = self.cuts[ self.cuts['name'] == name_idx].index.tolist()

        self.cuts = self.cuts.drop( self.cuts.index[idx] )


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


    def showCuts( self ):
        print self.cuts

