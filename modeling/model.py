#!/usr/bin/env python
import os, sys, re, time
import numpy as np

#from sklearn.cross_validation import cross_val_score 
from sklearn.model_selection import cross_val_score

class model:

    def __init__( self, model, name='' ):
        self.model = model
        self.name  = name
        self.prediction = None
        self.scores = { 'cv':None, 'model':None, 'resml':None }
        self.is_fitted = False


    def fit( self, X, y ):
        self.model.fit( X, y )
        self.is_fitted = True
        return self


    def predict( self, X ):
        self.prediction = self.model.predict( X )
        return self.prediction


    def get_scores( self, X_train, y_train, X_test, y_test, cv=4  ):
        self.scores['cv']    = cross_val_score( estimator=model, X=X_train, y=y_train, cv=cv )
        self.scores['model'] = model.score( X_test, y_test ))
   
        sum=0.0
        prediction = self.model.predict(X_test)
        for i in range(len(prediction)):
            p = np.log(prediction[i]+1)
            r = np.log(y_test[i]+1)
            sum = sum + (p - r)**2
        self.scores['rmsle'] = (sum/len(prediction))**0.5
        return self


