#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""This is the main code used at the MULTINETLAB for multilayer network analyses.
   It uses a supra-adjacency matrix (generated in MATLAB) as input, and creates a 
   multilayer network object - similar to the ones in Networkx.
   For privacy reasons, we provide a random MST file.
"""

__author__ = "Fernando Nobrega"
__contact__ = "f.nobregasantos@amsterdamumc.nl"
__date__ = "2019/10/15"
__status__ = "Production"


####################
# Review History   #
####################

# Reviewed by Eduarda Centeno 20200909
# Reviewed by Lucas Breedt 20201125
# Reviewed by Sebastien Dam 20251229: a file to be removed


####################
# Libraries        #
####################

# Standard imports
import itertools #no attribute version
from multiprocessing import Pool #no attribute version
import time as time #no attribute version

# Third party imports
import matplotlib.pyplot as plt # version '3.1.1'
import multinetx as mx #no attribute version
import networkx as nx#version 2.3
import numpy as np#version '1.19.0'
import pandas as pd# version '0.25.1'
from pylab import pcolor, show, colorbar, xticks, yticks
import pyreadstat #version '0.2.9'
import scipy as sio  #version '1.3.1'
import scipy.io
from sklearn import preprocessing #version 0.21.3
from sklearn.preprocessing import MinMaxScaler

import multilayer.config as config

################################################################################################################################

#######################
# SANITY CHECK        #
#######################

# ATTENTION: CHECK THE OUTPUT OF THESE LINES OF CODE TO ENSURE DATA IS LOADED CORRECTLY
# Check that this is in fact a dicionary
# print(type(supra_mst))
# Check that the keys are correct
# print(supra_mst.keys())
