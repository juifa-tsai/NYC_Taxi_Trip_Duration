#!/usr/bin/env python
import numpy as np
import pandas as pd
from features_helper import *

class feature_distance:

    def __init__( self, lng1=None, lat1=None, 
                        lng2=None, lat2=None ):
        self.avg_earth_radius = 6371 #km
        self.lng1 = lng1
        self.lat1 = lat1
        self.lng2 = lng2
        self.lat2 = lat2
        self.covert_radians()

    def covert_radians( self ):
        self.lat1_r, self.lng1_r, self.lat2_r, self.lng2_r = map( np.radians, (self.lat1, self.lng1, self.lat2, self.lng2))

    def get_distance( self, lng1_r=None, lat1_r=None, 
                            lng2_r=None, lat2_r=None  ):
        lat = lat2_r - lat1_r
        lng = lng2_r - lng1_r
        d = np.sin(lat * 0.5) ** 2 + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(lng * 0.5) ** 2
        h = 2 * self.avg_earth_radius * np.arcsin(np.sqrt(d))
        return h  # km

    def get_distance_haversine( self ):
        self.covert_radians()
        return self.get_distance( self.lng1_r, self.lat1_r, self.lng2_r, self.lat2_r )
    
    def get_distance_manhattan( self ):
        self.covert_radians()
        a = self.get_distance( self.lng1_r, self.lat1_r, self.lng2_r, self.lat1_r )
        b = self.get_distance( self.lng1_r, self.lat1_r, self.lng1_r, self.lat2_r )
        return a + b # km

    def get_direction( self ):
        self.covert_radians()
        delta_lng_r = np.radians(self.lng2 - self.lng1)
        y = np.sin(delta_lng_r) * np.cos(self.lat2_r)
        x = np.cos(self.lat1_r) * np.sin(self.lat2_r) - np.sin(self.lat1_r) * np.cos(self.lat2_r) * np.cos(delta_lng_r)
        return np.degrees(np.arctan2(y, x)) # theta
