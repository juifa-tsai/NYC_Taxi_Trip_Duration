#!/usr/bin/env python
import os, sys, re, time
import numpy as np
import pandas as pd

from model import *

from sklearn.model_selection import cross_val_score, train_test_split, ShuffleSplit
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

class regression:

    def __init__( self ):
        self.model={'RF'    : model(RandomForestRegressor(),         'Random Forest'           )],
                    'LR_p1' : model(linear_model.LinearRegression(), 'Linear Regression'       )],
                    'LR_p2' : model(linear_model.LinearRegression(), 'Linear Regression 2-Poly')],
                    'LR_pn' : model(linear_model.LinearRegression(), 'Linear Regression n-Poly')]}


    def regFitAll( self, X, 
                         y,
                         do_RF   =True,
                         do_LR_p1=True,
                         do_LR_p2=True,
                         do_LR_pn=False,
                         pn=None):

        if do_RF:    regFitRF( X, y, self.model['RF'])
        if do_LR_p1: regFitLR( X, y, self.model['LR_p1'], 1 )
        if do_LR_p2: regFitLR( X, y, self.model['LR_p2'], 2 )

        if do_LR_pn and pn > 2: 
            regFitLR( X, y, self.model['LR_pn'], pn)
            self.model['LR_pn'].name = 'Linear Regression %d-Poly'%( int(pn) )

        return self


    def regFitRF( self, X, y, estimator=None ):
        return estimator

    def regFitLR( self, X, y, estimator=None, n_poly=1 ):
        X_train = X
        y_train = y
        if int(n_poly) > 1:
            quadratic = PolynomialFeatures(degree=int(n_poly))
            X_train = quadratic.fit_transform(X)

        if not estimator:
            estimator = model(linear_model.LinearRegression())

        estimator.fit( X_train, y_train )
        return estimator 



