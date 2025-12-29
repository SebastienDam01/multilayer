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

# Algorithms import
from multilayer.algorithms.eigenvector_centrality import group_eigenvector_centrality
from multilayer.algorithms.degree_centrality import group_degree_centrality

import multilayer.config as config

################################################################################################################################

#############################################
# LOADING THE MATRICES                      #
############################################# 

# This is where the real data for computing all multilayer functions is loaded
# Every function defined from now on uses these data as input

# ATTENTION: THIS IS THE OBJECT THAT WILL BE USED FOR THE REMAINDER OF THE CODE!
supra_mst = scipy.io.loadmat(config.filename)

### IMPROVEMENT - INCLUDE VERBOSE FUNCTION TO MAKE CHECKS IN THE CODE


#######################
# SANITY CHECK        #
#######################

# ATTENTION: CHECK THE OUTPUT OF THESE LINES OF CODE TO ENSURE DATA IS LOADED CORRECTLY
# Check that this is in fact a dicionary
print(type(supra_mst))
# Check that the keys are correct
print(supra_mst.keys())


################################################################################################################################


# FROM THIS POINT FORWARD, NO FURTHER USER MODIFICATION/INPUT IS REQUIRED.
# This is where all of the functions are defined. None of these should require 
# modification or user input - only the last function, function_output, is needed
# for the user to calculate any multilayer network measure. Please also see the readme  

######################
# PLOTTING FUNCTIONS # 
######################

def plot_group_ec(data, list_of_single_layers):
    """Returns a histogram plot with the values of the Eigenvalue centrality for all nodes across all individuals."
    Parameters
    ----------
        
    data : A preloaded .mat  - Ex: supra_mst
    
    
    list_of_layers: a list of numbers corresponding to the Multilayer you want to create - 
    Ex: If you want a Multilayer with fmri, pli_delta and pli theta, using the tags: 0=fmri', '1=pli delta', '2= pli theta'
    list_of_layers = [0,1,2]
    
    Returns
    -------
    out : A histogram plot with EC for all nodes across all individuals
   
    """
    
    print('layers =',[layer_tags[i] for i in list_of_single_layers])

    temp = group_eigenvector_centrality(data,list_of_single_layers)
    plt.figure(figsize=(8,5))
    plt.hist(temp)
    # We can edit here the output if we have a vector with the name of the layers
    plt.xlabel('Eig. centr. - aggr- all nodes all individuals ', fontsize=20)
    #plt.xlim(-5,220)
    plt.ylabel("frequence", fontsize=20)
    #plt.xlim(40, 160)
    plt.ylim(0, 3500)
    #plt.title('individual '+str(individual))
    plt.show()


def plot_ec(individual, data, list_of_single_layers):
    """Returns a histogram with the values of the Eigenvalue centrality for all nodes for a chosen individual."
    Parameters
    ----------
    individual: an integer from [0, S-1], where S is the size of the cohort.
        
    data : A preloaded .mat  - Ex: supra_mst
    
    
    list_of_layers: a list of numbers corresponding to the Multilayer you want to create - 
    Ex: If you want a Multilayer with fmri, pli_delta and pli theta, using the tags: 0=fmri', '1=pli delta', '2= pli theta'
    list_of_layers = [0,1,2]
    
    Returns
    -------
    out: A histogram with EC for one individual
   
    """
    
    print('layers =',[layer_tags[i] for i in list_of_single_layers])
    #multilayer_g(individual,data,list_of_single_layers)
    m = mx.eigenvector_centrality_numpy(multilayer_g(individual,data,list_of_single_layers))
    #temp=multlayer3(i)
    temp1 = list(m.values())
    temp2 = muxviz_aggregate(temp1, len(list_of_single_layers)) 
    # This is the Mux Viz aggregate - We change the aggregate here if yo want later
    plt.hist((temp2))
    ###IMPROVEMENT: We can edit here the output if we have a vector with the name of the layers
    plt.xlabel('Eigenvector centrality - aggregate ', fontsize=20)
    #We may also want to choose the range for the plot.
    #plt.xlim(min,max)
    plt.ylabel("frequence", fontsize=20)
    plt.ylim(0, 100)
    plt.title('individual '+ str(individual))
    plt.show()
    return
             

###################
# OTHER FUNCTIONS #
###################
    
# This function extracts data from specific nodes - e.g. FPN or DMN
#### IMPROVEMENT: ALSO COMPUTE MEASURES WITHIN SPECIFIC SUBNETWORK IN THE FUTURE
def mask_subnetwork(result, target):
    """Returns a multilayer metric narrowed for a given list of nodes, which for our purposes are subnetworks""
    
    Parameters
    ----------
    result: A list with the results (output) of any of Multilayer functions in this code
    
    target : A list of target nodes of interest, e.g., nodes from DFN or FPN
    
    Returns
    -------
    out: A list for the results narrowed for the target nodes, i.e., If you say the target nodes for a given subnetwork, this function returns only the results of the list associated with the target nodes"
    """

    chunks = [result[x:x+config.layer_size] for x in range(0, len(result), config.layer_size)]
    mask = [chunk[x] for chunk in chunks for x in target]
    
    return mask


# This function saves data to a csv file
def save_csv(data, name, tag):
    """Returns a .csv file for further analysis using SPSS
    Parameters
    ----------
    data: The desired data you want to save
    name: The name of the file you want to save
    tag: The tag for the variable/column in your .csv file
    """
    # Obs: Notice that if you want to get results only for a subnetwork, we should first do:
    #data=mask_subnetwork(result,target)
    #before saving this file
    cols = [tag]
    df = pd.DataFrame(data, columns=cols)
    df.to_csv(name+'.csv')
    
    return

# ATTENTION: THIS IS THE ONLY FUNCTION THAT THE USER NEEDS TO CALCULATE ANY MULTILAYER
# NETWORK MEASURE
### IMPROVEMENT: create a boolean that does stuff when a mask is chosen or not
def function_output(function, data, filename, colname, layers, N=config.layer_size):
    """Returns the desired output for the MumoBrain database, or any other database organized similarly
    
    THIS IS PROBABLY THE MOST IMPORTANT FUNCTION FOR THE USER OF THIS CODE, SINCE EVERYTHING WAS BUILT TO REACH THIS STAGE HERE
    
    Parameters
    ----------
    function: One of the functions developed in this code for Multilayer Networks
    data: The data we want to use: e.g., supra_mst
    filename: The name of the file you want to save
    colname: the name of the column tag in your file
    layers: list of desired layers.

    """
    temp = function(data, layers)
    #You should include the desired subnetwork here. Now we have the whole Network.
    sub_net = list(range(0,N)) 
    # Ex: If you want FPN, sub_net=[16,17,18,19,20,21,28,29,30,31,93,94,123,124,133,134,163,164]
    
    temp_sub_net = mask_subnetwork(temp, sub_net)
    save_csv(temp_sub_net, filename, colname)
    
    return
