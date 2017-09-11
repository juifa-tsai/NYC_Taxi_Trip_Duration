#!/usr/bin/env python
import os, sys, re, time
import numpy as np
import pandas as pd

from sklearn.model_selection import cross_val_score, train_test_split, ShuffleSplit
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score, mean_absolute_error
from sklearn.ensemble import RandomForestRegressor

class regression:

    def __init__( self ):
        return

