#!/usr/bin/env python

import numpy as np
import pandas as pd
import string

from handleData import *
from handleData.featrueExtractor import *

csvfile_path  = 'data/train.csv'

df = pd.read_csv(csvfile_path)
print df.head()

