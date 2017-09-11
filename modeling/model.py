#!/usr/bin/env python
import os, sys, re, time
import numpy as np

from sklearn.model_selection import cross_val_score, train_test_split, ShuffleSplit

class model:

    def __init__( self, model, name='' ):
        self.model = model
        self.name  = name
        self.scores = { 'cv':None, 'model':None, 'resml':None }
        self.is_fitted = False


    def fit( self, X, y ):
        self.model.fit( X, y )
        self.is_fitted = True
        return self


    def predict( self, X ):
        return self.model.predict( X )


    def get_scores( self, X_train, y_train, X_test, y_test, k=4  ):
        cv = ShuffleSplit( n_splits=k, test_size=0.3, random_state=0 )
        self.scores['cv']    = cross_val_score( model, X, Y, cv=cv )
        self.scores['model'] = model.score( X_test, y_test ))
   
        sum=0.0
        prediction = self.model.predict(X_test)
        for i in range(len(prediction)):
            p = np.log(prediction[i]+1)
            r = np.log(y_test[i]+1)
            sum = sum + (p - r)**2
        self.scores['rmsle'] = (sum/len(prediction))**0.5 


